from playwright.async_api import async_playwright 
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pygetwindow as gw

with open("details.json","r",encoding="UTF-8") as f:
    data = json.load(f)

app = Flask(__name__)
CORS(app)

# === GLOBAL VARIABLES ===
playwright = None
browser = None
context = None
browser_window = None
page = None
loop = asyncio.get_event_loop()

# === INIT BROWSER AND GET WINDOW ===
async def init_browser():
    global playwright, browser, context, browser_window, page
    if not browser:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://google.com/")

        # small delay so the Chromium window actually appears
        await asyncio.sleep(2)
        chrome_windows = [w for w in gw.getAllTitles() if "Chrome" in w or "Chromium" in w]
        if chrome_windows:
            browser_window = gw.getWindowsWithTitle(chrome_windows[0])[0]
        else:
            browser_window = None

    return page

# === WINDOW CONTROL FUNCTIONS ===
async def bring_foreground():
    if browser_window:
        browser_window.activate()
        await asyncio.sleep(1)

async def minimize():
    if browser_window:
        browser_window.minimize()
        await asyncio.sleep(1)

async def restore():
    if browser_window:
        browser_window.restore()
        await asyncio.sleep(1)

async def maximize():
    if browser_window:
        browser_window.maximize()
        await asyncio.sleep(1)

# === AUTOMATION TASKS ===
async def hardcoded_automation():
    global page
    await init_browser()
    page = await context.new_page()
    await page.goto("https://spinsci.com/")
    await page.click('xpath=//*[@id="menu-item-10559"]/a')
    await page.click('xpath=//*[@id="menu-site-map-menu-col-10"]/li[2]/a')
    await asyncio.sleep(2)
    await page.fill('xpath=//*[@id="input_15_4"]','E.Y.S.V.S')
    await page.fill('xpath=//*[@id="input_15_5"]', 'Abhay')
    await page.fill('xpath=//*[@id="input_15_7"]', 'abhay.e@monarch.com')
    await page.fill('xpath=//*[@id="input_15_8"]', 'Monarch')
    await page.fill('xpath=//*[@id="input_15_12"]', 'AI Product Developer')
    await page.click('xpath=//*[@id="field_15_11"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', '+91')
    await page.fill('xpath=//*[@id="input_15_6"]', "123456789")
    await page.click('xpath=//*[@id="field_15_16"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', 'Indiana')
    await page.fill('xpath=//*[@id="input_15_14"]','Cisco')
    await page.fill('xpath=//*[@id="input_15_9"]', 'would love to collaborate with your product')

    # Demo of window control
    await maximize()
    await bring_foreground()
    await restore()
    await minimize()
    await maximize()

    await asyncio.sleep(2)
    return "automation done"

async def json_automation(data):
    global page
    await init_browser()
    page = await context.new_page()
    await page.goto("https://spinsci.com/")
    await page.click('xpath=//*[@id="menu-item-10559"]/a')
    await page.click('xpath=//*[@id="menu-site-map-menu-col-10"]/li[2]/a')
    await asyncio.sleep(2)
    await page.fill('xpath=//*[@id="input_15_4"]', data["first_name"])
    await page.fill('xpath=//*[@id="input_15_5"]', data["last_name"])
    await page.fill('xpath=//*[@id="input_15_7"]', data["email"])
    await page.fill('xpath=//*[@id="input_15_8"]', data["company"])
    await page.fill('xpath=//*[@id="input_15_12"]', data["job_title"])
    await page.click('xpath=//*[@id="field_15_11"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', data["country_code"])
    await page.fill('xpath=//*[@id="input_15_6"]', data["phone"])
    await page.click('xpath=//*[@id="field_15_16"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', data["state"])
    await page.fill('xpath=//*[@id="input_15_14"]', data["partner"])
    await page.fill('xpath=//*[@id="input_15_9"]', data["message"])
    await asyncio.sleep(2)
    return "automation done"

async def url_automation(details):
    global page
    await init_browser()
    page = await context.new_page()
    await page.goto("https://spinsci.com/")
    await page.click('xpath=//*[@id="menu-item-10559"]/a')
    await page.click('xpath=//*[@id="menu-site-map-menu-col-10"]/li[2]/a')
    await asyncio.sleep(2)
    await page.fill('xpath=//*[@id="input_15_4"]', details["first_name"])
    await page.fill('xpath=//*[@id="input_15_5"]', details["last_name"])
    await page.fill('xpath=//*[@id="input_15_7"]', details["email"])
    await page.fill('xpath=//*[@id="input_15_8"]', details["company"])
    await page.fill('xpath=//*[@id="input_15_12"]', details["job_title"])
    await page.click('xpath=//*[@id="field_15_11"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', details["country_code"])
    await page.fill('xpath=//*[@id="input_15_6"]', details["phone"])
    await page.click('xpath=//*[@id="field_15_16"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', details["state"])
    await page.fill('xpath=//*[@id="input_15_14"]', details["partner"])
    await page.fill('xpath=//*[@id="input_15_9"]', details["message"])
    await asyncio.sleep(2)
    return "automation done"

# === FLASK ROUTES ===
@app.route("/url_automation", methods=["GET"])
def run_automation():
    details = request.args.to_dict()
    result = loop.run_until_complete(url_automation(details))
    return jsonify({"msg": result})

@app.route('/basic-automation', methods=["GET"])
def main_1():
    result = loop.run_until_complete(hardcoded_automation())
    return jsonify({"message":result})

@app.route('/json-automation', methods=["GET"])
def main_2():
    result = loop.run_until_complete(json_automation(data))
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
