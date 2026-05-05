import os
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def fetch_tweets():
    url = "https://rsshub.app/twitter/user/elonmusk"

    try:
        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.content)

        tweets = []
        for item in root.findall(".//item"):
            title = item.find("title").text
            tweets.append(title)

        return tweets

    except Exception as e:
        return []

def analyze(tweets):
    count = len(tweets)

    msg = f"""
📊 Elon Tweet Analysis

🐦 Recent tweets: {count}

🔮 Weekly prediction:
👉 {count * 7}

🧠 Insight:
{"High activity" if count > 5 else "Normal"}
"""
    send(msg)

def main():
    tweets = fetch_tweets()

    if not tweets:
        send("⚠️ Failed to fetch tweets (RSS issue)")

