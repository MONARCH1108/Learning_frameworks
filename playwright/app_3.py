import asyncio
import pygetwindow as gw
from playwright.async_api import async_playwright

async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)  # browser window visible
    context = await browser.new_context()
    return playwright, browser, context

async def hardcoded_automation():
    playwright, browser, context = await init_browser()
    page = await context.new_page()

    await page.goto("https://spinsci.com/")
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

    # === CONTROL BROWSER WINDOW USING pygetwindow ===
    # Get all chrome windows
    chrome_windows = [w for w in gw.getAllTitles() if "Chrome" in w or "Chromium" in w]
    if chrome_windows:
        win = gw.getWindowsWithTitle(chrome_windows[0])[0]

        # Bring to foreground
        win.activate()
        await asyncio.sleep(2)

        # Minimize
        win.minimize()
        await asyncio.sleep(2)

        # Restore (un-minimize)
        win.restore()
        await asyncio.sleep(2)

        # Maximize
        win.maximize()
        await asyncio.sleep(2)

        # Send to background (minimize again as demo)
        win.minimize()
        await asyncio.sleep(2)

        # Bring foreground again
        win.restore()
        win.activate()

    await asyncio.sleep(5)
    await browser.close()
    await playwright.stop()

    return "automation + window control done"


if __name__ == "__main__":
    asyncio.run(hardcoded_automation())
