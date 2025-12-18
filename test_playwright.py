from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://rrb.digialm.com//per/g22/pub/2667/touchstone/AssessmentQPHTMLMode1//2667O252/2667O252S47D85891/17559611765129741/226243123782986_2667O252S47D85891E1.html"
        print(f"Navigating to {url}...")
        response = page.goto(url)
        print(f"Status: {response.status}")
        print(f"Title: {page.title()}")
        if response.status == 200:
             content = page.content()
             if "Manish Kumar Meena" in content:
                 print("Success! Found candidate name.")
             else:
                 print("Page loaded but candidate name not found (maybe blocked/captcha?)")
             print(content[:500])
        else:
             print("Failed to load page.")
        browser.close()

if __name__ == "__main__":
    run()
