from playwright.async_api import async_playwright
import asyncio
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open("data.json","r",encoding="UTF-8") as f:
    data = json.load(f)

async def hardcoded_automation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
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
        await asyncio.sleep(5)
    return "automation done"

async def json_automation(data):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
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
        await asyncio.sleep(5)
    return "automation done"

async def url_automation(details):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
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
    return "automation done"


@app.route('/basic-automation', methods=["GET"])
async def main_1():
    result = await hardcoded_automation()
    return jsonify({"message":result})

@app.route('/json-automation', methods=["GET"])
async def main_2():
    result = await json_automation(data)
    return jsonify({"message":result})

@app.route('/url_automation', methods=["GET"])
async def main_3():
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
    return jsonify({"message":result})

if __name__ == "__main__":
    app.run(debug=True)

# http://127.0.0.1:5000/url_automation?first_name=E.Y.S.V.S&last_name=Abhay&email=abhay.e@monarch.com&company=Monarch&job_title=AI%20Product%20Developer&country_code=+91&phone=123456789&state=Indiana&partner=Cisco&message=Would%20love%20to%20collaborate