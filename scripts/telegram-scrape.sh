#!/bin/bash
# Telegram Group Scrape Protocol v11
# Usage: ./telegram-scrape.sh "Group Name" "Requester"
#
# WORKING STEPS:
# 1. Open Telegram
# 2. Cmd+K for global search
# 3. Type group name
# 4. Down arrow to select
# 5. Enter x2 to open group
# 6. Scroll to TOP (oldest message)
# 7. Screenshot
# 8. Scroll down, screenshot, repeat
# 9. Agent analyzes and summarizes

GROUP_NAME="${1:-Cannascend}"
REQUESTER="${2:-Diamond}"

WORKSPACE="/Users/m/.openclaw/workspace"
OUTPUT_DIR="$WORKSPACE/telegram-scrape-$(date +%s)"
mkdir -p "$OUTPUT_DIR"

if [ -z "$GROUP_NAME" ]; then
  echo "Usage: $0 <Group Name> <Requester>"
  echo "Example: $0 Cannascend Diamond"
  exit 1
fi

echo "📱 Step 1: opening Telegram..."
osascript -e 'tell app "Telegram" to activate'
sleep 2

echo "📸 Step 2: Screenshot to orient..."
osascript -e 'tell app "Telegram" to activate'
sleep 1
peekaboo image --mode screen --path "$OUTPUT_DIR/01-orient.png"

echo "🔍 Step 3: Cmd+K for global search..."
peekaboo hotkey --keys "cmd,k"
sleep 2

echo "✍️  Step 4: Typing group name: $GROUP_NAME"
peekaboo type "$GROUP_NAME"
sleep 2

echo "⬇️  Step 5: Down arrow to select from recent results..."
peekaboo press down --count 2
sleep 1

echo "⏎  Step 6: Enter x2 to open group..."
peekaboo press enter --count 2
sleep 2

echo "📸 Step 7: Screenshot after entering group..."
osascript -e 'tell app "Telegram" to activate'
sleep 1
peekaboo image --mode screen --path "$OUTPUT_DIR/02-in-group.png"

echo "⬆️  Step 8: Scrolling to TOP (oldest message)..."
peekaboo press up --count 50
sleep 2

SCREEN_NUM=3
echo "📸 Step 9: Starting scroll capture..."

# Scroll down and screenshot until we reach current (bottom)
for i in {1..20}; do
  osascript -e 'tell app "Telegram" to activate'
  sleep 0.5
  peekaboo image --mode screen --path "$OUTPUT_DIR/$(printf '%02d' $SCREEN_NUM)-scroll.png"
  echo "   → Captured screenshot $SCREEN_NUM"
  SCREEN_NUM=$((SCREEN_NUM + 1))
  
  # Scroll down a screen worth
  peekaboo press down --count 15
  sleep 1.5
done

echo ""
echo "🎉 Complete! Captured $((SCREEN_NUM - 3)) screenshots:"
ls -la "$OUTPUT_DIR/"
echo ""
echo "Now analyze the screenshots and summarize the conversation for $REQUESTER"
