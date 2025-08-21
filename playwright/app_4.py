import asyncio
import pygetwindow as gw
from playwright.async_api import async_playwright

# === GLOBAL VARIABLES ===
playwright = None
browser = None
context = None
page = None
browser_window = None   # global window handle

# === INIT BROWSER AND GET WINDOW ===
async def init_browser():
    global playwright, browser, context, browser_window

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)  # visible browser
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://spinsci.com/")

    # Find the Chromium/Chrome window
    await asyncio.sleep(2)  # small delay so window loads
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


# === AUTOMATION TASK ===
async def hardcoded_automation():
    global page
    page = await init_browser()

    # Perform automation
    await page.click('xpath=//*[@id="menu-item-10559"]/a')
    await page.click('xpath=//*[@id="menu-site-map-menu-col-10"]/li[2]/a')
    await asyncio.sleep(2)
    await page.fill('xpath=//*[@id="input_15_4"]', 'E.Y.S.V.S')
    await page.fill('xpath=//*[@id="input_15_5"]', 'Abhay')
    await page.fill('xpath=//*[@id="input_15_7"]', 'abhay.e@monarch.com')
    await page.fill('xpath=//*[@id="input_15_8"]', 'Monarch')
    await page.fill('xpath=//*[@id="input_15_12"]', 'AI Product Developer')
    await page.click('xpath=//*[@id="field_15_11"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', '+91')
    await page.fill('xpath=//*[@id="input_15_6"]', "123456789")
    await page.click('xpath=//*[@id="field_15_16"]/div/div/span/span[1]/span/span[2]')
    await page.fill('xpath=/html/body/span/span/span[1]/input', 'Indiana')
    await page.fill('xpath=//*[@id="input_15_14"]', 'Cisco')
    await page.fill('xpath=//*[@id="input_15_9"]', 'would love to collaborate with your product')

    await asyncio.sleep(3)

    # === DEMO: Call window control functions ===
    await bring_foreground()
    await minimize()
    await restore()
    await maximize()

    await asyncio.sleep(3)

    # Cleanup
    await browser.close()
    await playwright.stop()
    return "automation + window control demo done"


if __name__ == "__main__":
    asyncio.run(hardcoded_automation())
