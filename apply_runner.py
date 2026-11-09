import os
from playwright.sync_api import sync_playwright

def apply_job(job, profile):
    try:
        p=sync_playwright().start()
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(job["url"],wait_until="domcontentloaded",timeout=60000)
        page.wait_for_timeout(1800)
        for key,selectors in {
          "name":['input[name*="name" i]','input[id*="name" i]'],
          "email":['input[type="email"]'],
          "phone":['input[type="tel"]','input[name*="phone" i]']
        }.items():
            value=profile.get(key,"")
            if value:
                for s in selectors:
                    try:
                        el=page.locator(s).first
                        if el.count() and el.is_visible(): el.fill(value); break
                    except: pass
        resume=profile.get("resume_path","")
        if resume and os.path.isfile(resume):
            try:
                el=page.locator('input[type="file"]').first
                if el.count(): el.set_input_files(resume)
            except: pass
        # Keep browser open for user review; no automatic final submission.
        return "Opened for review"
    except Exception as e: return "Could not open: "+str(e)[:100]
