from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os
import time
from datetime import datetime

# Rich library for beautiful CLI formatting
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.align import Align
    from rich.rule import Rule
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Installing rich for beautiful CLI...")
    os.system("pip install rich")
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        from rich.prompt import Prompt
        from rich.markdown import Markdown
        from rich.progress import Progress, SpinnerColumn, TextColumn
        from rich.table import Table
        from rich.align import Align
        from rich.rule import Rule
        RICH_AVAILABLE = True
    except ImportError:
        RICH_AVAILABLE = False

load_dotenv()

# Initialize console
if RICH_AVAILABLE:
    console = Console()

document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def print_beautiful(*args, style="", panel=False, title="", **kwargs):
    """Wrapper for beautiful printing with fallback to regular print"""
    if RICH_AVAILABLE:
        content = " ".join(str(arg) for arg in args)
        if panel:
            console.print(Panel(content, title=title, style=style))
        else:
            console.print(content, style=style, **kwargs)
    else:
        print(*args, **kwargs)

def create_header():
    """Create a beautiful header"""
    if RICH_AVAILABLE:
        title = Text("✨ DRAFTER ✨", style="bold magenta")
        subtitle = Text("Your AI-Powered Document Assistant", style="italic cyan")
        
        header_table = Table.grid(padding=1)
        header_table.add_column(justify="center")
        header_table.add_row(title)
        header_table.add_row(subtitle)
        header_table.add_row(Text("━" * 50, style="bright_blue"))
        
        console.print(Panel(header_table, style="bright_blue", padding=(1, 2)))
    else:
        print("\n" + "="*50)
        print("✨ DRAFTER ✨".center(50))
        print("Your AI-Powered Document Assistant".center(50))
        print("="*50 + "\n")

def show_document_status():
    """Show current document status"""
    if RICH_AVAILABLE:
        if document_content:
            content_preview = document_content[:200] + "..." if len(document_content) > 200 else document_content
            status_table = Table(title="📄 Current Document Status", show_header=False, box=None)
            status_table.add_column("Label", style="cyan", width=15)
            status_table.add_column("Value", style="white")
            
            status_table.add_row("Length:", f"{len(document_content)} characters")
            status_table.add_row("Lines:", f"{document_content.count(chr(10)) + 1 if document_content else 0}")
            status_table.add_row("Preview:", content_preview)
            
            console.print(Panel(status_table, style="green", padding=(0, 1)))
        else:
            console.print(Panel("📝 Document is empty - ready for content!", style="yellow", padding=(0, 1)))
    else:
        print(f"\n--- Document Status ---")
        if document_content:
            print(f"Length: {len(document_content)} characters")
            print(f"Preview: {document_content[:100]}...")
        else:
            print("Document is empty")
        print("-" * 25)

@tool
def update(content: str) -> str:
    """ Update document with provided content """
    global document_content
    document_content = content
    
    if RICH_AVAILABLE:
        console.print("✅ Document updated successfully!", style="bold green")
        show_document_status()
    else:
        print(f"✅ Document updated successfully!\nCurrent length: {len(document_content)} characters")
    
    return f"Document has been updated successfully! Current content length: {len(document_content)} characters"

@tool
def save(filename: str) -> str:
    """
    Save the current document to a text file and finish the process.

    Args:
        filename: Name for the text file.
    """
    global document_content
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"
    
    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(document_content)
        
        if RICH_AVAILABLE:
            save_info = Table(show_header=False, box=None)
            save_info.add_column("", style="cyan")
            save_info.add_column("", style="white")
            save_info.add_row("📁 File:", filename)
            save_info.add_row("📏 Size:", f"{len(document_content)} characters")
            save_info.add_row("🕒 Saved:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            console.print(Panel(
                Align.center(save_info),
                title="💾 Document Saved Successfully!",
                style="bright_green",
                padding=(1, 2)
            ))
        else:
            print(f"\n💾 Document saved successfully to: {filename}")
            print(f"Size: {len(document_content)} characters")
        
        return f"Document has been saved successfully to '{filename}'."
    
    except Exception as e:
        error_msg = f"❌ Error saving document: {str(e)}"
        print_beautiful(error_msg, style="bold red", panel=True, title="Error")
        return f"Error saving document: {str(e)}"

tools = [update, save]
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro"
).bind_tools(tools)

def get_user_input(prompt_text="What would you like to do with the document?"):
    """Get user input with beautiful prompting"""
    if RICH_AVAILABLE:
        return Prompt.ask(f"[bold cyan]🤔 {prompt_text}[/bold cyan]", default="")
    else:
        return input(f"\n🤔 {prompt_text} ")

def display_ai_response(content):
    """Display AI response beautifully"""
    if RICH_AVAILABLE:
        console.print("\n")
        console.print("🤖 AI Assistant:", style="bold blue")
        console.print(Panel(content, style="blue", padding=(0, 1)))
    else:
        print(f"\n🤖 AI: {content}")

def display_tool_usage(tool_calls):
    """Display tool usage information"""
    if RICH_AVAILABLE:
        tool_names = [tc['name'] for tc in tool_calls]
        tools_text = ", ".join(tool_names)
        console.print(f"🔧 Using tools: {tools_text}", style="bold yellow")
    else:
        tool_names = [tc['name'] for tc in tool_calls]
        print(f"🔧 Using tools: {', '.join(tool_names)}")

def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f""" 
    You are Drafter, a helpful writing assistant. You are going to help the user update and edit documents.

    If the user wants to update or modify content, use the 'update' tool with the complete new document.
    If the user wants to save and finish, you need to use the 'save' tool.
    Make sure to always show the current document state after modifications.
    
    Be helpful, friendly, and provide clear guidance on what the user can do.

    The current document content is: {document_content}
    """)

    if not state["messages"]:
        # First interaction
        show_document_status()
        user_input = get_user_input("I'm ready to help you create or edit a document! What would you like to do?")
    else:
        # Subsequent interactions
        user_input = get_user_input()
    
    if RICH_AVAILABLE:
        console.print(f"\n[bold green]👤 You:[/bold green] {user_input}")
        
        # Show thinking animation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("🧠 AI is thinking...", total=None)
            time.sleep(0.5)  # Brief pause for effect
    else:
        print(f"\n👤 You: {user_input}")
        print("🧠 AI is thinking...")

    user_message = HumanMessage(content=user_input)
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    
    response = model.invoke(all_messages)
    
    display_ai_response(response.content)
    
    if hasattr(response, "tool_calls") and response.tool_calls:
        display_tool_usage(response.tool_calls)
    
    return {"messages": list(state["messages"]) + [user_message, response]}

def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    if not messages:
        return "continue"
    
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end"
    return "continue"

def print_messages(messages):
    if not messages or not RICH_AVAILABLE:
        return
    
    for message in messages[-2:]:  # Show last 2 messages
        if isinstance(message, ToolMessage):
            # Tool results are handled by the tools themselves now
            pass

def create_footer():
    """Create a beautiful footer"""
    if RICH_AVAILABLE:
        console.print("\n")
        console.print(Rule(style="bright_blue"))
        footer_text = Text("Thank you for using Drafter! 🎉", style="bold cyan")
        console.print(Align.center(footer_text))
        console.print(Text("Your documents are ready! ✨", style="italic bright_white"))
        console.print(Rule(style="bright_blue"))
    else:
        print("\n" + "="*50)
        print("Thank you for using Drafter! 🎉".center(50))
        print("Your documents are ready! ✨".center(50))
        print("="*50)

# Graph setup
graph = StateGraph(AgentState)
graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges(
    "tools", should_continue,
    {
        "continue": "agent",
        "end": END,
    }
)
app = graph.compile()

def run_document_agent():
    """Run the beautiful document agent"""
    # Clear screen for better presentation
    os.system('cls' if os.name == 'nt' else 'clear')
    
    create_header()
    
    if RICH_AVAILABLE:
        # Show helpful commands
        help_table = Table(title="💡 Quick Commands", show_header=False, box=None)
        help_table.add_column("Command", style="cyan", width=20)
        help_table.add_column("Description", style="white")
        help_table.add_row("'Create a report about...'", "Generate new content")
        help_table.add_row("'Add a section about...'", "Append to existing content")
        help_table.add_row("'Save as [filename]'", "Save and exit")
        help_table.add_row("'Show current document'", "Display current content")
        
        console.print(Panel(help_table, style="yellow", padding=(0, 1)))
        console.print()

    state = {"messages": []}
    
    try:
        for step in app.stream(state, stream_mode="values"):
            if "messages" in step:
                print_messages(step["messages"])
    except KeyboardInterrupt:
        print_beautiful("\n\n👋 Goodbye! Thanks for using Drafter!", style="bold cyan")
    except Exception as e:
        print_beautiful(f"\n❌ An error occurred: {str(e)}", style="bold red")
    
    create_footer()

if __name__ == "__main__":
    run_document_agent()