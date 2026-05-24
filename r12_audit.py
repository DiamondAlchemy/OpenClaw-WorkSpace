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
    page.goto(URL, wait_until="networkidle", timeout=30000)
    
    print(f"Current URL: {page.url}", file=sys.stderr)
    
    # Find the password input field and fill it
    page.fill('input[type="password"]', TOKEN)
    print("Filled token into password field", file=sys.stderr)
    
    # Click the Sign In button
    page.click('button:has-text("Sign In")')
    print("Clicked Sign In button", file=sys.stderr)
    
    # Wait for navigation
    page.wait_for_load_state("networkidle", timeout=15000)
    print(f"URL after sign-in: {page.url}", file=sys.stderr)
    
    # Wait a bit more for any client-side renders
    page.wait_for_timeout(3000)
    
    # Get tier badge
    tier_badge = None
    try:
        # Look for badge text
        badge = page.locator('[class*="badge"], [class*="tier"], [class*="role"]').first
        tier_badge = badge.inner_text()
    except:
        pass
    
    # Also check for "Reporter" text anywhere
    reporter_text = None
    if "reporter" in page.content().lower():
        reporter_text = "Reporter"
    
    print(f"Tier badge: {tier_badge or reporter_text or 'not found'}", file=sys.stderr)
    
    # Count facilities
    facilities = []
    try:
        # Try to find facility rows/cards
        facility_elements = page.locator('[class*="facility"], [class*="Facility"]').all()
        for el in facility_elements:
            text = el.inner_text()
            if text.strip():
                facilities.append(text.strip()[:100])  # truncate long text
    except Exception as e:
        print(f"Error finding facilities: {e}", file=sys.stderr)
    
    print(f"Facility count: {len(facilities)}", file=sys.stderr)
    for f in facilities[:20]:  # max 20
        print(f"  - {f}", file=sys.stderr)
    
    # Look for "act-as" button
    act_as_btn = None
    try:
        # Look for buttons with text like "act as", "switch", "impersonate", etc.
        buttons = page.locator('button').all()
        for btn in buttons:
            text = btn.inner_text().lower()
            if any(kw in text for kw in ["act", "switch", "imperson", "as", "facility", "enter"]):
                act_as_btn = btn.inner_text().strip()
                break
    except:
        pass
    
    print(f"Act-as button: {act_as_btn or 'not found'}", file=sys.stderr)
    
    # Output final URL as JSON for parsing
    result = {
        "url": page.url,
        "tier_badge": tier_badge or reporter_text,
        "facility_count": len(facilities),
        "facilities": facilities,
        "act_as_button": act_as_btn
    }
    
    print("===RESULT===")
    print(json.dumps(result, indent=2))
    
    browser.close()
