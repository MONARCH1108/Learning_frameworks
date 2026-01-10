import json
import os
import time
import asyncio
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging
from pathlib import Path

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

# Additional imports for agents
import google.generativeai as genai
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
import aiofiles
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentState(TypedDict):
    """State shared between all agents"""
    json_file_path: str
    data_status: str  # 'fresh', 'stale', 'missing'
    raw_data: Optional[Dict]
    processed_data: Optional[Dict]
    images_downloaded: bool
    tweets_generated: bool
    tweets_posted: bool
    error_message: Optional[str]
    last_check: datetime
    twitter_credentials: Dict[str, str]
    gemini_api_key: str

class MainCoordinatorAgent:
    """Main agent that coordinates the entire workflow"""
    
    def __init__(self):
        self.name = "MainCoordinator"
    
    def check_data_freshness(self, state: AgentState) -> AgentState:
        """Check if existing data is fresh (less than 12 hours old)"""
        logger.info(f"[{self.name}] Checking data freshness...")
        
        json_path = state.get('json_file_path', 'bbc_improved_data.json')
        
        try:
            if os.path.exists(json_path):
                # Check file modification time
                file_time = datetime.fromtimestamp(os.path.getmtime(json_path))
                time_diff = datetime.now() - file_time
                
                if time_diff < timedelta(hours=12):
                    # Check if file has valid content
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if data and data.get('categories') and len(data.get('categories', {})) > 0:
                        state['data_status'] = 'fresh'
                        state['raw_data'] = data
                        logger.info(f"[{self.name}] Data is fresh, skipping crawl")
                        return state
            
            state['data_status'] = 'stale'
            logger.info(f"[{self.name}] Data is stale or missing, need to crawl")
            
        except Exception as e:
            logger.error(f"[{self.name}] Error checking data: {e}")
            state['data_status'] = 'missing'
            state['error_message'] = str(e)
        
        state['last_check'] = datetime.now()
        return state
    
    def route_next_action(self, state: AgentState) -> str:
        """Determine which agent should run next"""
        if state['data_status'] in ['stale', 'missing']:
            return "crawler_agent"
        elif state['data_status'] == 'fresh' and not state.get('tweets_generated', False):
            return "processing_agent"
        elif state.get('tweets_generated', False) and not state.get('tweets_posted', False):
            return "twitter_agent"
        else:
            return END

class BBCCrawlerAgent:
    """Agent responsible for crawling BBC news"""
    
    def __init__(self):
        self.name = "BBCCrawler"
        self.base_url = "https://www.bbc.com"
        self.session = requests.Session()
        
        # Enhanced headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })
        
        self.url_patterns = {
            'news': [
                'https://www.bbc.com/news',
                'https://www.bbc.com/news/world',
                'https://www.bbc.com/news/uk',
                'https://www.bbc.com/news/business',
                'https://www.bbc.com/news/politics',
                'https://www.bbc.com/news/technology'
            ]
        }
    
    def crawl_bbc_content(self, state: AgentState) -> AgentState:
        """Main crawling function"""
        logger.info(f"[{self.name}] Starting BBC content crawl...")
        
        try:
            all_data = {
                'crawl_metadata': {
                    'started': datetime.now().isoformat(),
                    'method': 'LangGraph Multi-Agent Crawler',
                    'version': '4.0-LANGGRAPH'
                },
                'categories': {},
                'all_articles': []
            }
            
            total_articles = []
            
            for category, urls in self.url_patterns.items():
                logger.info(f"[{self.name}] Processing {category} category...")
                
                # Discover article URLs
                article_urls = self.discover_article_urls(urls, max_per_category=8)
                
                if article_urls:
                    # Extract content
                    articles = self.extract_content_from_urls(article_urls)
                    
                    if articles:
                        category_data = {
                            'category_name': category,
                            'total_articles': len(articles),
                            'articles': articles
                        }
                        
                        all_data['categories'][category] = category_data
                        total_articles.extend(articles)
            
            all_data['all_articles'] = total_articles
            all_data['crawl_metadata']['completed'] = datetime.now().isoformat()
            all_data['crawl_metadata']['total_articles'] = len(total_articles)
            
            # Save data
            json_path = state.get('json_file_path', 'bbc_improved_data.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            
            state['raw_data'] = all_data
            state['data_status'] = 'fresh'
            logger.info(f"[{self.name}] Crawl completed! Found {len(total_articles)} articles")
            
        except Exception as e:
            logger.error(f"[{self.name}] Crawling failed: {e}")
            state['error_message'] = str(e)
            state['data_status'] = 'error'
        
        return state
    
    def discover_article_urls(self, base_urls: List[str], max_per_category: int = 5) -> List[str]:
        """Discover article URLs from category pages"""
        all_articles = []
        
        for url in base_urls:
            try:
                logger.info(f"[{self.name}] Discovering from: {url}")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                link_selectors = [
                    'a[href*="/news/"]',
                    'a[data-testid="internal-link"]',
                    '.gs-c-promo-heading a',
                    'h2 a[href], h3 a[href]'
                ]
                
                found_links = set()
                for selector in link_selectors:
                    links = soup.select(selector)
                    for link in links:
                        href = link.get('href')
                        if href:
                            full_url = urljoin(url, href)
                            if self.is_valid_article_url(full_url):
                                found_links.add(full_url)
                
                category_articles = list(found_links)[:max_per_category]
                all_articles.extend(category_articles)
                
            except Exception as e:
                logger.error(f"[{self.name}] Error discovering from {url}: {e}")
                continue
        
        return list(set(all_articles))
    
    def is_valid_article_url(self, url: str) -> bool:
        """Check if URL is a valid BBC article"""
        if not url or not url.startswith('https://www.bbc.com'):
            return False
        
        exclude_patterns = ['/live/', '/topics/', '/programmes/', '.json', '.xml']
        for pattern in exclude_patterns:
            if pattern in url.lower():
                return False
        
        return '/news/' in url
    
    def extract_content_from_urls(self, urls: List[str]) -> List[Dict]:
        """Extract content from article URLs"""
        articles = []
        
        for url in urls:
            try:
                logger.info(f"[{self.name}] Extracting: {url}")
                response = self.session.get(url, timeout=20)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_elem = soup.select_one('h1[data-testid="headline"], h1')
                title = title_elem.get_text(strip=True) if title_elem else "No title found"
                
                # Extract content paragraphs
                content_parts = []
                for selector in ['[data-component="text-block"] p', '.story-body__inner p', 'p']:
                    elements = soup.select(selector)
                    for elem in elements:
                        text = elem.get_text(strip=True)
                        if len(text) > 20:
                            content_parts.append(text)
                    if len(content_parts) >= 5:
                        break
                
                content = ' '.join(content_parts[:5])  # Limit to first 5 paragraphs
                
                # Extract images
                images = []
                img_elements = soup.select('img[src]')
                for img in img_elements[:3]:  # Limit to 3 images per article
                    src = img.get('src')
                    if src and ('ichef.bbci.co.uk' in src or 'bbc.com' in src):
                        images.append({
                            'url': urljoin(url, src),
                            'alt': img.get('alt', ''),
                            'caption': img.get('title', '')
                        })
                
                if len(content) > 100:  # Only include articles with substantial content
                    article = {
                        'url': url,
                        'title': title,
                        'content': content[:2000],  # Limit content length
                        'images': images,
                        'extracted_at': datetime.now().isoformat(),
                        'word_count': len(content.split()),
                        'category': self.categorize_url(url)
                    }
                    articles.append(article)
                
            except Exception as e:
                logger.error(f"[{self.name}] Error extracting {url}: {e}")
                continue
        
        return articles
    
    def categorize_url(self, url: str) -> str:
        """Categorize URL based on path"""
        if '/business/' in url:
            return 'business'
        elif '/politics/' in url:
            return 'politics'
        elif '/technology/' in url:
            return 'technology'
        elif '/world/' in url:
            return 'world'
        elif '/uk/' in url:
            return 'uk'
        else:
            return 'news'

class ProcessingAgent:
    """Agent responsible for processing data and generating tweets"""
    
    def __init__(self):
        self.name = "ProcessingAgent"
    
    def process_and_generate_tweets(self, state: AgentState) -> AgentState:
        """Main processing function"""
        logger.info(f"[{self.name}] Starting data processing and tweet generation...")
        
        try:
            raw_data = state.get('raw_data', {})
            if not raw_data:
                raise ValueError("No raw data available for processing")
            
            # Download images first
            processed_articles = self.download_images(raw_data)
            
            # Generate tweets using Gemini
            tweets_data = self.generate_tweets_with_gemini(processed_articles, state.get('gemini_api_key'))
            
            # Save processed data
            processed_data = {
                'processed_at': datetime.now().isoformat(),
                'tweets': tweets_data,
                'total_tweets': len(tweets_data)
            }
            
            # Save to file
            with open('processed_tweets.json', 'w', encoding='utf-8') as f:
                json.dump(tweets_data, f, indent=2, ensure_ascii=False)
            
            state['processed_data'] = processed_data
            state['images_downloaded'] = True
            state['tweets_generated'] = True
            
            logger.info(f"[{self.name}] Processing completed! Generated {len(tweets_data)} tweets")
            
        except Exception as e:
            logger.error(f"[{self.name}] Processing failed: {e}")
            state['error_message'] = str(e)
        
        return state
    
    def download_images(self, raw_data: Dict) -> List[Dict]:
        """Download images from articles"""
        logger.info(f"[{self.name}] Downloading images...")
        
        # Create images directory
        images_dir = Path("downloaded_images")
        images_dir.mkdir(exist_ok=True)
        
        processed_articles = []
        
        for category_name, category_data in raw_data.get('categories', {}).items():
            for article in category_data.get('articles', []):
                processed_article = article.copy()
                downloaded_images = []
                
                for i, image_info in enumerate(article.get('images', [])):
                    try:
                        image_url = image_info.get('url')
                        if not image_url:
                            continue
                        
                        # Generate filename
                        url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
                        filename = f"article_{len(processed_articles)}_{i}_{url_hash}.jpg"
                        filepath = images_dir / filename
                        
                        # Download image
                        response = requests.get(image_url, timeout=10)
                        response.raise_for_status()
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        downloaded_images.append({
                            'original_url': image_url,
                            'local_path': str(filepath),
                            'alt': image_info.get('alt', ''),
                            'caption': image_info.get('caption', '')
                        })
                        
                    except Exception as e:
                        logger.warning(f"[{self.name}] Failed to download image {image_url}: {e}")
                        continue
                
                processed_article['downloaded_images'] = downloaded_images
                processed_articles.append(processed_article)
        
        return processed_articles
    
    def generate_tweets_with_gemini(self, articles: List[Dict], api_key: str) -> List[Dict]:
        """Generate tweets using Gemini API"""
        logger.info(f"[{self.name}] Generating tweets with Gemini...")
        
        if not api_key:
            raise ValueError("Gemini API key not provided")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        tweets_data = []
        
        for article in articles[:10]:  # Limit to 10 articles
            try:
                # Create comprehensive prompt
                prompt = f"""
                Create an engaging Twitter thread (2-3 tweets) based on this BBC news article.
                
                Title: {article.get('title', '')}
                Content: {article.get('content', '')[:800]}
                Category: {article.get('category', '')}
                
                Requirements:
                - First tweet: Hook/headline (under 250 characters)
                - Second tweet: Key details (under 250 characters) 
                - Third tweet (optional): Context/impact (under 250 characters)
                - Include relevant hashtags
                - Make it newsworthy and engaging
                - Maintain professional tone
                
                Return as JSON:
                {{
                    "thread": [
                        {{"text": "tweet 1 content", "hashtags": ["#hashtag1", "#hashtag2"]}},
                        {{"text": "tweet 2 content", "hashtags": ["#hashtag3"]}}
                    ],
                    "summary": "Brief summary of the news"
                }}
                """
                
                response = model.generate_content(prompt)
                
                if response.text:
                    # Try to parse JSON response
                    try:
                        tweet_json = json.loads(response.text)
                        
                        tweet_data = {
                            'article_url': article.get('url', ''),
                            'article_title': article.get('title', ''),
                            'thread': tweet_json.get('thread', []),
                            'summary': tweet_json.get('summary', ''),
                            'images': article.get('downloaded_images', []),
                            'generated_at': datetime.now().isoformat()
                        }
                        
                        tweets_data.append(tweet_data)
                        logger.info(f"[{self.name}] Generated tweet for: {article.get('title', '')[:50]}...")
                        
                    except json.JSONDecodeError:
                        # Fallback: create simple tweet
                        simple_tweet = {
                            'article_url': article.get('url', ''),
                            'article_title': article.get('title', ''),
                            'thread': [
                                {
                                    'text': f"{article.get('title', '')[:200]}... Read more:",
                                    'hashtags': ['#BBCNews', '#Breaking']
                                }
                            ],
                            'summary': article.get('content', '')[:200],
                            'images': article.get('downloaded_images', []),
                            'generated_at': datetime.now().isoformat()
                        }
                        tweets_data.append(simple_tweet)
                
                # Small delay to respect API limits
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"[{self.name}] Failed to generate tweet for article: {e}")
                continue
        
        return tweets_data

class TwitterAgent:
    """Agent responsible for posting tweets"""
    
    def __init__(self):
        self.name = "TwitterAgent"
    
    async def post_tweets(self, state: AgentState) -> AgentState:
        """Post tweets using Playwright"""
        logger.info(f"[{self.name}] Starting Twitter posting...")
        
        try:
            processed_data = state.get('processed_data', {})
            tweets_data = processed_data.get('tweets', [])
            
            if not tweets_data:
                raise ValueError("No tweets available for posting")
            
            credentials = state.get('twitter_credentials', {})
            username = credentials.get('username')
            password = credentials.get('password')
            
            if not username or not password:
                raise ValueError("Twitter credentials not provided")
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Login to Twitter
                await self.login_to_twitter(page, username, password)
                
                # Post tweets
                posted_count = 0
                for tweet_data in tweets_data[:5]:  # Limit to 5 tweet threads
                    try:
                        success = await self.post_tweet_thread(page, tweet_data)
                        if success:
                            posted_count += 1
                            logger.info(f"[{self.name}] Posted tweet thread {posted_count}")
                            
                            # Wait between posts
                            await asyncio.sleep(10)
                        
                    except Exception as e:
                        logger.error(f"[{self.name}] Failed to post tweet: {e}")
                        continue
                
                await browser.close()
                
                state['tweets_posted'] = True
                logger.info(f"[{self.name}] Posted {posted_count} tweet threads")
            
        except Exception as e:
            logger.error(f"[{self.name}] Twitter posting failed: {e}")
            state['error_message'] = str(e)
        
        return state
    
    async def login_to_twitter(self, page, username: str, password: str):
        """Login to Twitter using Playwright"""
        logger.info(f"[{self.name}] Logging into Twitter...")
        
        await page.goto("https://twitter.com/i/flow/login")
        await page.wait_for_load_state("networkidle")
        
        # Fill username
        await page.fill('input[autocomplete="username"]', username)
        await page.click('text=Next')
        await page.wait_for_timeout(2000)
        
        # Fill password
        await page.fill('input[name="password"]', password)
        await page.click('text=Log in')
        
        # Wait for login to complete
        await page.wait_for_selector('[data-testid="primaryColumn"]', timeout=30000)
        logger.info(f"[{self.name}] Successfully logged into Twitter")
    
    async def post_tweet_thread(self, page, tweet_data: Dict) -> bool:
        """Post a tweet thread with images"""
        try:
            thread = tweet_data.get('thread', [])
            images = tweet_data.get('images', [])
            
            for i, tweet_info in enumerate(thread):
                tweet_text = tweet_info.get('text', '')
                hashtags = tweet_info.get('hashtags', [])
                
                # Combine text and hashtags
                full_tweet = f"{tweet_text} {' '.join(hashtags)}"
                
                # Navigate to compose
                if i == 0:
                    await page.goto("https://twitter.com/compose/tweet")
                    await page.wait_for_load_state("networkidle")
                
                # Fill tweet text
                await page.fill('[data-testid="tweetTextarea_0"]', full_tweet)
                
                # Add image if available for first tweet
                if i == 0 and images:
                    try:
                        image_path = images[0].get('local_path')
                        if image_path and os.path.exists(image_path):
                            await page.set_input_files('input[type="file"]', image_path)
                            await page.wait_for_timeout(3000)  # Wait for image upload
                    except Exception as e:
                        logger.warning(f"[{self.name}] Failed to upload image: {e}")
                
                # Post tweet
                await page.click('[data-testid="tweetButtonInline"]')
                await page.wait_for_timeout(3000)
                
                # If this is part of a thread, continue
                if i < len(thread) - 1:
                    await page.wait_for_timeout(5000)  # Wait before next tweet
            
            return True
            
        except Exception as e:
            logger.error(f"[{self.name}] Failed to post thread: {e}")
            return False

# Main LangGraph Workflow
def create_workflow():
    """Create the LangGraph workflow"""
    
    # Initialize agents
    main_agent = MainCoordinatorAgent()
    crawler_agent = BBCCrawlerAgent()
    processing_agent = ProcessingAgent()
    twitter_agent = TwitterAgent()
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("main_coordinator", main_agent.check_data_freshness)
    workflow.add_node("crawler_agent", crawler_agent.crawl_bbc_content)
    workflow.add_node("processing_agent", processing_agent.process_and_generate_tweets)
    workflow.add_node("twitter_agent", lambda state: asyncio.run(twitter_agent.post_tweets(state)))
    
    # Add edges
    workflow.add_edge("main_coordinator", "router")
    workflow.add_conditional_edges(
        "router",
        main_agent.route_next_action,
        {
            "crawler_agent": "crawler_agent",
            "processing_agent": "processing_agent", 
            "twitter_agent": "twitter_agent",
            END: END
        }
    )
    workflow.add_edge("crawler_agent", "processing_agent")
    workflow.add_edge("processing_agent", "twitter_agent")
    workflow.add_edge("twitter_agent", END)
    
    # Set entry point
    workflow.set_entry_point("main_coordinator")
    
    # Add router node
    workflow.add_node("router", lambda state: state)
    
    return workflow.compile(checkpointer=MemorySaver())

# Main execution function
async def main():
    """Main function to run the multi-agent system"""
    
    # Configuration - UPDATE THESE VALUES
    CONFIG = {
        'json_file_path': 'bbc_improved_data.json',
        'twitter_credentials': {
            'username': 'your_twitter_username',
            'password': 'your_twitter_password'
        },
        'gemini_api_key': 'your_gemini_api_key'
    }
    
    # Validate configuration
    if CONFIG['twitter_credentials']['username'] == 'your_twitter_username':
        print("❌ Please update your Twitter credentials in the CONFIG section!")
        return
    
    if CONFIG['gemini_api_key'] == 'your_gemini_api_key':
        print("❌ Please update your Gemini API key in the CONFIG section!")
        return
    
    # Initialize state
    initial_state = {
        'json_file_path': CONFIG['json_file_path'],
        'data_status': 'unknown',
        'raw_data': None,
        'processed_data': None,
        'images_downloaded': False,
        'tweets_generated': False,
        'tweets_posted': False,
        'error_message': None,
        'last_check': datetime.now(),
        'twitter_credentials': CONFIG['twitter_credentials'],
        'gemini_api_key': CONFIG['gemini_api_key']
    }
    
    # Create and run workflow
    app = create_workflow()
    
    logger.info("🚀 Starting LangGraph Multi-Agent News Twitter Bot...")
    
    try:
        # Execute the workflow
        result = app.invoke(initial_state, config={"thread_id": "news_bot_session"})
        
        # Print final results
        print("\n" + "="*80)
        print("MULTI-AGENT WORKFLOW COMPLETED")
        print("="*80)
        print(f"Data Status: {result.get('data_status', 'Unknown')}")
        print(f"Images Downloaded: {result.get('images_downloaded', False)}")
        print(f"Tweets Generated: {result.get('tweets_generated', False)}")
        print(f"Tweets Posted: {result.get('tweets_posted', False)}")
        
        if result.get('error_message'):
            print(f"❌ Error: {result['error_message']}")
        else:
            print("✅ Workflow completed successfully!")
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        print(f"❌ Workflow failed: {e}")

if __name__ == "__main__":
    # Required dependencies (add to requirements.txt):
    """
    langgraph
    langsmith
    playwright
    google-generativeai
    beautifulsoup4
    requests
    aiofiles
    """
    
    print("📋 Make sure to install required dependencies:")
    print("pip install langgraph langsmith playwright google-generativeai beautifulsoup4 requests aiofiles")
    print("\nAnd run: playwright install")
    print("\n" + "="*80)
    
    asyncio.run(main())