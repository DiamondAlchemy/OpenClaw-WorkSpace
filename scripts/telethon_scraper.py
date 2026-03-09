#!/usr/bin/env python3
"""
Telethon Telegram Scraper (Async Version)
Usage: python3 telethon_scraper.py
"""

import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Configuration
API_ID = 30111111
API_HASH = 'a4d5c8b45f840d32c2d082f2e8054b3b'
PHONE = '+13039091368'

SESSION_NAME = 'telegram_scraper'

async def main():
    print("🔗 Connecting to Telegram...")
    
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        # This will send the code to your phone on first run
        await client.start(PHONE)
        
        print("✅ Connected!")
        me = await client.get_me()
        print(f"👤 Logged in as: {me.first_name}")
        print("")
        
        print("📋 Your recent dialogs:")
        async for dialog in client.iter_dialogs(limit=15):
            print(f"  - {dialog.name}")

if __name__ == '__main__':
    asyncio.run(main())
