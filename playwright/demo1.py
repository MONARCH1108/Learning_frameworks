from playwright.async_api import async_playwright
from flask import Flask, request, jsonify
from flask_cors import CORS
import pygetwindow as gw
import asyncio

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
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://google.com")
        await asyncio.sleep(2)
        chrome_window = []
        for w in gw.getAllTitles():
            if "Chrome" in w or "Chromium" in w:
                chrome_window.append(w)
        
        if chrome_window:
            browser_window = gw.getWindowsWithTitle(chrome_window[0])[0]
        else:
            browser_window = None
    return page

async def bring_front():
    if browser_window:
        browser_window.activate()
        await asyncio.sleep(1)

async def minimize():
    if browser_window:
        browser_window.minimize()
        await asyncio.sleep(1)

async def maximize():
    if browser_window:
        browser_window.maximize()
        await asyncio.sleep(1)

async def restore():
    if browser_window:
        browser_window.restore()
        await asyncio.sleep(1)

async def automation(data):
    global page
    await init_browser()
    page = await context.new_page()
    await page.goto("https://spinsci.com/")
    await page.click('xpath=//*[@id="menu-item-10559"]/a')
    await page.click('xpath=//*[@id="menu-site-map-menu-col-10"]/li[2]/a')
    await page.fill('xpath=//*[@id="input_15_4"]', data["first_name"])
    await page.fill('xpath=//*[@id="input_15_5"]', data["last_name"])
    await page.fill('xpath=//*[@id="input_15_7"]', data["work_email"])
    await page.fill('xpath=//*[@id="input_15_8"]', data["company_name"])
    await page.fill('xpath=//*[@id="input_15_12"]', data["job_title"])
    await page.click('xpath=//*[@id="field_15_11"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', data["Country_code"])
    await page.press('xpath=/html/body/span/span/span[1]/input', "Enter")
    await page.fill('xpath=//*[@id="input_15_6"]', data["ph_number"])
    await page.click('xpath=//*[@id="field_15_16"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', data["State"])
    await page.press('xpath=/html/body/span/span/span[1]/input', "Enter")
    await page.fill('xpath=//*[@id="input_15_14"]', data["contact_center"])
    await page.fill('xpath=//*[@id="input_15_9"]', data["comment"])
    await asyncio.sleep(5)
    await minimize()
    await maximize()
    await bring_front()
    await bring_front()
    await minimize()
    return "automation demo complete"

@app.route('/auto', methods=["GET"])
def main():
    data = request.args.to_dict()
    result = loop.run_until_complete(automation(data))
    return jsonify({"message":result})

@app.route("/close_browser", methods=["GET"])
def close_browser():
    global browser, playwright
    if browser:
        loop.run_until_complete(browser.close())
        loop.run_until_complete(playwright.stop())
        browser = None
    return jsonify({"status": "browser closed"})

if __name__ == "__main__":
    app.run(debug=True)