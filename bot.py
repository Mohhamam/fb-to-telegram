import time
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# =========================
# ENVIRONMENT VARIABLE
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

if not BOT_TOKEN or not CHANNEL:
    raise Exception("BOT_TOKEN atau CHANNEL belum di-set")

bot = Bot(token=BOT_TOKEN)

# =========================
# DAFTAR FANSPAGE
# =========================
PAGES = [
    "https://www.facebook.com/unboxfactory",
    "https://www.facebook.com/interestingengineering",
    "https://www.facebook.com/mech.eng.world"
]

# =========================
# STORAGE POST YANG SUDAH TERKIRIM
# =========================
sent_posts = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def check_facebook_page(page_url):
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = a["href"]

            if "/posts/" in link:
                if link.startswith("/"):
                    link = "https://www.facebook.com" + link

                if link not in sent_posts:
                    sent_posts.add(link)

                    message = (
                        "📢 *Post Baru Facebook*\n\n"
                        f"🔗 {link}"
                    )

                    bot.send_message(
                        chat_id=CHANNEL,
                        text=message,
                        parse_mode="Markdown",
                        disable_web_page_preview=False
                    )

                    time.sleep(2)  # delay kecil biar aman

    except Exception as e:
        print(f"Error di {page_url}: {e}")

# =========================
# LOOP UTAMA
# =========================
while True:
    for page in PAGES:
        check_facebook_page(page)

    print("Cek selesai, tidur 5 menit...")
    time.sleep(300)  # 5 menit
