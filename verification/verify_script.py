from playwright.sync_api import sync_playwright

def verify_score_calculator():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the Flask App
        page.goto("http://127.0.0.1:5000")
        
        # Check initial state
        print("Page Title:", page.title())
        
        # Fill in the URL input
        url_input = page.locator("#urlInput")
        url_input.fill("https://rrb.digialm.com//per/g22/pub/2667/touchstone/AssessmentQPHTMLMode1//2667O252/2667O252S47D85891/17559611765129741/226243123782986_2667O252S47D85891E1.html")
        
        # Click Calculate
        page.click("button[type=submit]")
        
        # Wait for results to appear
        page.wait_for_selector("#results")
        
        # Take screenshot of the result
        page.screenshot(path="verification/result_screenshot.png")
        print("Screenshot taken.")
        
        browser.close()

if __name__ == "__main__":
    verify_score_calculator()
