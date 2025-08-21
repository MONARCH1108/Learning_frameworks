from playwright.async_api import async_playwright
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

playwright = None
browser = None
context = None
loop = asyncio.get_event_loop()

async def init_browser():
    global playwright, browser, context
    if not browser:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()

async def url_automation(details):
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
    await asyncio.sleep(5)
    return "automation done in new tab ✅"

@app.route("/url_automation", methods=["GET"])
def run_automation():
    details = request.args.to_dict()
    result = loop.run_until_complete(url_automation(details))
    return jsonify({"status": "success", "msg": result})

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
