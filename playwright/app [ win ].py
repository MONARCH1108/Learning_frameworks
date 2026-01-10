import asyncio
import pygetwindow as gw
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.google.com")
        print("Opened Google!")

        # Get browser window (first active window with "Chrome" in title)
        win = None
        for w in gw.getWindowsWithTitle("Google"):
            win = w
            break

        if win:
            # --- Bring to Foreground ---
            win.activate()
            print("Window brought to foreground")
            await asyncio.sleep(2)

            # --- Send to Background (Minimize) ---
            win.minimize()
            print("Window sent to background (minimized)")
            await asyncio.sleep(2)

            # --- Restore Back ---
            win.restore()
            print("Window restored to normal")
            await asyncio.sleep(2)

        await browser.close()
        print("Browser closed")

asyncio.run(run())
