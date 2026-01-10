from playwright.async_api import async_playwright
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

playwright = None
browser = None
persistent_page = None   

async def init_browser():
    global playwright, browser, persistent_page
    if playwright is None:
        playwright = await async_playwright().start()
    if browser is None:
        browser = await playwright.chromium.launch(headless=False)
        persistent_page = await browser.new_page()
        await persistent_page.goto("about:blank")

async def url_automation(details):
    await init_browser()
    page = await browser.new_page()
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
    await page.close()
    return "automation done"

@app.route('/url_automation', methods=["GET"])
async def url_route():
    details = {
        "first_name": request.args.get("first_name", ""),
        "last_name": request.args.get("last_name", ""),
        "email": request.args.get("email", ""),
        "company": request.args.get("company", ""),
        "job_title": request.args.get("job_title", ""),
        "country_code": request.args.get("country_code", ""),
        "phone": request.args.get("phone", ""),
        "state": request.args.get("state", ""),
        "partner": request.args.get("partner", ""),
        "message": request.args.get("message", "")
    }
    result = await url_automation(details)
    return jsonify({"message": result})

if __name__ == "__main__":
    app.run(debug=True)
