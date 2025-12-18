from playwright.sync_api import sync_playwright

def fetch_stealth(url):
    with sync_playwright() as p:
        # Launch browser with specific arguments to look human
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # Navigate and wait for the main content table to load
            response = page.goto(url, wait_until="networkidle", timeout=60000)
            if response.status == 200:
                return page.content()
            return None
        except Exception as e:
            print(f"Fetch failed: {e}")
            return None
        finally:
            browser.close()
