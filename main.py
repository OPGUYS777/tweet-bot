from telethon import TelegramClient, events
from datetime import datetime
import requests

# ========= CONFIG =========
api_id = 33911412              # <-- apna API ID daal
api_hash = "4acad418f87f623347a8ca83f3b168a9"  # <-- apna API HASH daal

channel = "elonvitalikalerts"

BOT_TOKEN = "8790935199:AAHTjA6v2G4FHVmbgb-EnkxHLgTIyivZ1Kg"
CHAT_ID = "7171044211"
# ==========================

tweet_times = []

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=channel))
async def handler(event):
    text = event.raw_text

    if "x.com" in text:
        now = datetime.now()
        tweet_times.append(now)

        total = len(tweet_times)

        # 🏏 Tweet Run Rate (like cricket)
        if total > 1:
            hours = (tweet_times[-1] - tweet_times[0]).seconds / 3600
            rate = total / hours if hours > 0 else total
        else:
            rate = 1

        # ⏱ Gap
        if total > 1:
            gap = (tweet_times[-1] - tweet_times[-2]).seconds / 60
        else:
            gap = 0

        # 🔥 Signal
        if rate > 10:
            signal = "🚨 HIGH ACTIVITY (PUMP ZONE)"
        elif rate > 5:
            signal = "⚠️ Moderate Activity"
        else:
            signal = "Normal"

        message = f"""
🚨 NEW TWEET DETECTED

👤 Source: Elon/Vitalik Channel

⏰ Time: {now.strftime("%H:%M:%S")}
📊 Total Tweets: {total}

🏏 Tweet Run Rate: {round(rate,2)} / hour
⏱ Gap: {round(gap,2)} min

⚡ Signal: {signal}
"""

        send_telegram(message)

client.start()
print("🚀 Listening...")
client.run_until_disconnected()