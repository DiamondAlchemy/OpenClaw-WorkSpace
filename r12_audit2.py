#!/usr/bin/env python3
import json
import sys

from playwright.sync_api import sync_playwright

TOKEN = "58c48593-ba09-4892-a1ec-dc9a8a8e80fa"
URL = f"https://app.topsecretcertified.com/admin/claim?token={TOKEN}"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-gpu", "--no-sandbox"]
    )
    context = browser.new_context(
        viewport={"width": 1600, "height": 900}
    )
    page = context.new_page()
    
    print(f"Navigating to {URL}", file=sys.stderr)
    
    # Just navigate and wait, don't try to fill anything yet
    response = page.goto(URL, wait_until="networkidle", timeout=30000)
    
    print(f"Initial URL: {page.url}", file=sys.stderr)
    print(f"Response status: {response.status if response else 'no response'}", file=sys.stderr)
    
    # Wait for any client-side redirects
    page.wait_for_timeout(3000)
    
    print(f"URL after wait: {page.url}", file=sys.stderr)
    
    # Get the page content / DOM
    content = page.content()
    
    # Check for any visible text that indicates auth state
    body_text = page.locator("body").inner_text()
    print(f"Body text (first 1000 chars): {body_text[:1000]}", file=sys.stderr)
    
    # Check if there's a password field
    password_fields = page.locator('input[type="password"]').count()
    print(f"Password fields found: {password_fields}", file=sys.stderr)
    
    # Check if we're on the claim page or admin dashboard
    if "/admin/claim" in page.url:
        print("Still on claim page - token not consumed or redirect failed", file=sys.stderr)
    elif "/admin" in page.url:
        print("On admin page - may need to fill credentials", file=sys.stderr)
        # Check what elements are on this page
        buttons = page.locator("button").all_inner_texts()
        print(f"Buttons: {buttons}", file=sys.stderr)
        
        # Check for any facility-related elements
        facility_links = page.locator("a[href*='facility']").all_inner_texts()
        print(f"Facility links: {facility_links}", file=sys.stderr)
    
    # Output result
    result = {
        "final_url": page.url,
        "body_text_preview": body_text[:500],
        "has_password_field": password_fields > 0,
        "buttons": [b.strip() for b in page.locator("button").all_inner_texts()],
    }
    
    print("===RESULT===")
    print(json.dumps(result, indent=2))
    
    browser.close()
