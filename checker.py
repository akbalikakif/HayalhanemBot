import requests
import schedule
import time
from datetime import datetime

# === AYARLAR ===
TELEGRAM_TOKEN = 'AAGtwL6wFtZLxgUwzb8kufEVAtFWEG5d8eg'
TELEGRAM_CHAT_ID = '1036357014'
YOUTUBE_API_KEY = 'AIzaSyBUhUL4sTVa7m9XcA9eezOEFXJ6FbnybSA'

KANALLAR = {
    "Hayalhanem Mersin": "UCXs8nFqUPQaJZxAt1b3Wblw",
    "Hayalhanem İstanbul": "UC-4_6lIAIsMcyUC57kWLlsA",
    "Hayalhanem Ankara": "UCaDpCyQiDfjLJ5jTmzZz7ZA",
    "Hayalhanem Almanya": "UC-4_6lIAIsMcyUC57kWLlsA",
    "Mehmet Yıldız": "UCaDpCyQiDfjLJ5jTmzZz7ZA"
}

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Telegram'a mesaj gönderilemedi: {e}")

def kontrol_et(kanal_adi, kanal_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={kanal_id}&part=snippet,id&order=date&maxResults=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["items"]:
            video = data["items"][0]
            video_baslik = video["snippet"]["title"]
            video_tarih = video["snippet"]["publishedAt"]
            mesaj = f"✅ {kanal_adi} kanalında yeni video kontrolü yapıldı.\n📹 Video: {video_baslik}\n🕒 Yayınlanma: {video_tarih}"
            telegram_gonder(mesaj)
        else:
            telegram_gonder(f"{kanal_adi} kanalında video bulunamadı.")
    except Exception as e:
        telegram_gonder(f"{kanal_adi} kontrolünde hata oluştu: {e}")

# === Fonksiyonlar ===
def kontrol_hayalhanem_mersin():
    kontrol_et("Hayalhanem Mersin", KANALLAR["Hayalhanem Mersin"])

def kontrol_mehmet_yildiz():
    kontrol_et("Mehmet Yıldız", KANALLAR["Mehmet Yıldız"])

def kontrol_hayalhanem_istanbul():
    kontrol_et("Hayalhanem İstanbul", KANALLAR["Hayalhanem İstanbul"])

def kontrol_hayalhanem_ankara():
    kontrol_et("Hayalhanem Ankara", KANALLAR["Hayalhanem Ankara"])

def kontrol_hayalhanem_almanya():
    kontrol_et("Hayalhanem Almanya", KANALLAR["Hayalhanem Almanya"])

# === Schedule Ayarları ===

# Mersin: Pazartesi Çarşamba Cuma Pazar 19.00
schedule.every().monday.at("19:00").do(kontrol_hayalhanem_mersin)
schedule.every().wednesday.at("19:00").do(kontrol_hayalhanem_mersin)
schedule.every().friday.at("19:00").do(kontrol_hayalhanem_mersin)
schedule.every().sunday.at("19:00").do(kontrol_hayalhanem_mersin)

# Mehmet Yıldız: Salı Perşembe Cumartesi 19.00
schedule.every().tuesday.at("19:00").do(kontrol_mehmet_yildiz)
schedule.every().thursday.at("19:00").do(kontrol_mehmet_yildiz)
schedule.every().saturday.at("19:00").do(kontrol_mehmet_yildiz)

# İstanbul: Salı Perşembe 18.00
schedule.every().tuesday.at("18:00").do(kontrol_hayalhanem_istanbul)
schedule.every().thursday.at("18:00").do(kontrol_hayalhanem_istanbul)

# Ankara: Salı 19.30 | Perşembe 2 haftada bir 19.30
schedule.every().tuesday.at("19:30").do(kontrol_hayalhanem_ankara)
def kontrol_ankara_iki_haftada_bir():
    if datetime.now().isocalendar().week % 2 == 0:
        kontrol_hayalhanem_ankara()
schedule.every().thursday.at("19:30").do(kontrol_ankara_iki_haftada_bir)

# Almanya: Perşembe 20.00
schedule.every().thursday.at("20:00").do(kontrol_hayalhanem_almanya)

# === Sonsuz Döngü ===
print("Bot başlatıldı...")

while True:
    schedule.run_pending()
    time.sleep(60)