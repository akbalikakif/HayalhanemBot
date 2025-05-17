import requests
import schedule
import time
from datetime import datetime

# === AYARLAR ===
BOT_TOKEN = '7566188625:AAGtwL6wFtZLxgUwzb8kufEVAtFWEG5d8eg'
CHAT_ID = '1036357014'
API_KEY = 'AIzaSyBUhUL4sTVa7m9XcA9eezOEFXJ6FbnybSA'

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

# Tekrarlayan kontrol fonksiyonu
def tekrarlayan_kontrol(kanal_adi, kanal_id):
    print(f"{kanal_adi} için 2 dk sonra başlayacak 1 saatlik tekrarlayan kontrol başlıyor.")
    time.sleep(120)  # 2 dakika bekle

    for i in range(6):  # 6 kere kontrol, her biri 10 dakika arayla
        kontrol_et(kanal_adi, kanal_id)
        if i < 5:
            print(f"{kanal_adi} kontrolü {i+1}. kez yapıldı, 10 dk bekleniyor...")
            time.sleep(600)  # 10 dakika bekle

# Schedule fonksiyonlarını güncelle
def kontrol_hayalhanem_mersin():
    tekrarlayan_kontrol("Hayalhanem Mersin", KANALLAR["Hayalhanem Mersin"])

def kontrol_mehmet_yildiz():
    tekrarlayan_kontrol("Mehmet Yıldız", KANALLAR["Mehmet Yıldız"])

def kontrol_hayalhanem_istanbul():
    tekrarlayan_kontrol("Hayalhanem İstanbul", KANALLAR["Hayalhanem İstanbul"])

def kontrol_hayalhanem_ankara():
    tekrarlayan_kontrol("Hayalhanem Ankara", KANALLAR["Hayalhanem Ankara"])

def kontrol_hayalhanem_almanya():
    tekrarlayan_kontrol("Hayalhanem Almanya", KANALLAR["Hayalhanem Almanya"])

# === Schedule Ayarları ===
schedule.every().monday.at("19:00").do(kontrol_hayalhanem_mersin)
schedule.every().wednesday.at("19:00").do(kontrol_hayalhanem_mersin)
schedule.every().friday.at("19:00").do(kontrol_hayalhanem_mersin)
schedule.every().sunday.at("19:00").do(kontrol_hayalhanem_mersin)

schedule.every().tuesday.at("19:00").do(kontrol_mehmet_yildiz)
schedule.every().thursday.at("19:00").do(kontrol_mehmet_yildiz)
schedule.every().saturday.at("19:17").do(kontrol_mehmet_yildiz)

schedule.every().tuesday.at("18:00").do(kontrol_hayalhanem_istanbul)
schedule.every().thursday.at("18:00").do(kontrol_hayalhanem_istanbul)

schedule.every().tuesday.at("19:30").do(kontrol_hayalhanem_ankara)

def kontrol_ankara_iki_haftada_bir():
    if datetime.now().isocalendar().week % 2 == 0:
        tekrarlayan_kontrol("Hayalhanem Ankara", KANALLAR["Hayalhanem Ankara"])

schedule.every().thursday.at("19:30").do(kontrol_ankara_iki_haftada_bir)

schedule.every().thursday.at("20:00").do(kontrol_hayalhanem_almanya)

print("Bot başlatıldı...")

while True:
    schedule.run_pending()
    time.sleep(1)  # 1 saniye bekle daha hızlı tepki için
