from playwright.async_api import async_playwright
from flask import Flask, request, jsonify
from flask_cors import CORS
import pygetwindow as gw
import asyncio
import logging

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)
CORS(app)

playwright = None
browser = None
context = None
browser_window = None
page = None
loop = asyncio.get_event_loop()

async def init_browser():
    global playwright, browser, context, browser_window, page
    if not browser:
        logging.info("Starting playwright and lauching browser")
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://google.com")
        logging.info("Browser launched and navigated to demo google page")

        await asyncio.sleep(2)
        chrome_window = []
        for w in gw.getAllTitles():
            if "Chrome" in w or "Chromium" in w:
                chrome_window.append(w)
        
        if chrome_window:
            browser_window = gw.getWindowsWithTitle(chrome_window[0])[0]
            logging.info(f"Chrome attaches to browser window: {chrome_window[0]}")
        else:
            browser_window = None
            logging.warning("No Chrome/Chromium window detected.")
    return page

async def bring_front():
    if browser_window:
        browser_window.activate()
        logging.info("Browser window brought to front.")
        await asyncio.sleep(1)

async def minimize():
    if browser_window:
        browser_window.minimize()
        logging.info("Browser window minimized.")
        await asyncio.sleep(1)

async def maximize():
    if browser_window:
        browser_window.maximize()
        logging.info("Browser window maximized.")
        await asyncio.sleep(1)

async def restore():
    if browser_window:
        browser_window.restore()
        logging.info("Browser window restored.")
        await asyncio.sleep(1)

async def automation(data):
    global page
    try:
        await init_browser()
        page = await context.new_page()
        logging.info("New tab opened and navigating to SpinSci...")
        await page.goto("https://spinsci.com/")
        await page.click('xpath=//*[@id="menu-item-10559"]/a')
        await page.click('xpath=//*[@id="menu-site-map-menu-col-10"]/li[2]/a')

        await page.fill('xpath=//*[@id="input_15_4"]', data["first_name"])
        logging.info(f"Filled First Name: {data['first_name']}")
        await page.fill('xpath=//*[@id="input_15_5"]', data["last_name"])
        logging.info(f"Filled Last Name: {data['last_name']}")
        await page.fill('xpath=//*[@id="input_15_7"]', data["work_email"])
        logging.info(f"Filled Email: {data['work_email']}")
        await page.fill('xpath=//*[@id="input_15_8"]', data["company_name"])
        logging.info(f"Filled Company: {data['company_name']}")
        await page.fill('xpath=//*[@id="input_15_12"]', data["job_title"])
        logging.info(f"Filled Job Title: {data['job_title']}")

        await page.click('xpath=//*[@id="field_15_11"]/div/div/span/span[1]/span/span[2]')
        await page.fill('xpath=/html/body/span/span/span[1]/input', data["Country_code"])
        await page.press('xpath=/html/body/span/span/span[1]/input', "Enter")
        logging.info(f"Selected Country: {data['Country_code']}")

        await page.fill('xpath=//*[@id="input_15_6"]', data["ph_number"])
        await page.click('xpath=//*[@id="field_15_16"]/div/div/span/span[1]/span/span[2]')
        await page.fill('xpath=/html/body/span/span/span[1]/input', data["State"])
        await page.press('xpath=/html/body/span/span/span[1]/input', "Enter")
        logging.info(f"Selected State: {data['State']}")

        await page.fill('xpath=//*[@id="input_15_14"]', data["contact_center"])
        logging.info(f"Filled Partner: {data['contact_center']}")
        await page.fill('xpath=//*[@id="input_15_9"]', data["comment"])
        logging.info(f"Filled Message: {data['comment']}")

        await asyncio.sleep(5)
        await minimize()
        await maximize()
        await bring_front()
        await bring_front()
        await minimize()

        logging.info("Automation completed successfully.")
        return "automation demo complete"
    
    except Exception as e:
        logging.error("automation failed: {e}")
        return "automation failed: {e}"

@app.route('/auto', methods=["GET"])
def main():
    data = request.args.to_dict()
    logging.info(f"Received request with data: {data}")
    result = loop.run_until_complete(automation(data))
    return jsonify({"message":result})

@app.route("/close_browser", methods=["GET"])
def close_browser():
    global browser, playwright
    if browser:
        loop.run_until_complete(browser.close())
        loop.run_until_complete(playwright.stop())
        browser = None
        logging.info("Browser closed manually via endpoint.")
    return jsonify({"status": "browser closed"})

if __name__ == "__main__":
    logging.info("Starting Flask server...")
    app.run(debug=True)