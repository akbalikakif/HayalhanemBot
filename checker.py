import datetime
import requests
from telegram import Bot

# === AYARLAR ===
TELEGRAM_TOKEN = 'AAGtwL6wFtZLxgUwzb8kufEVAtFWEG5d8eg'
TELEGRAM_CHAT_ID = '1036357014'
YOUTUBE_API_KEY = 'AIzaSyBUhUL4sTVa7m9XcA9eezOEFXJ6FbnybSA'

# Kanal ID’leri
CHANNELS = {
    "Hayalhanem Mersin":      {"id": "UCXs8nFqUPQaJZxAt1b3Wblw"},
    "Hayalhanem İstanbul":    {"id": "UC-4_6lIAIsMcyUC57kWLlsA"},
    "Hayalhanem Ankara":      {"id": "UCaDpCyQiDfjLJ5jTmzZz7ZA"},
    "Hayalhanem Almanya":     {"id": "UC-4_6lIAIsMcyUC57kWLlsA"},
    "Mehmet Yıldız":          {"id": "UCaDpCyQiDfjLJ5jTmzZz7ZA"},
}

# Kontrol zamanları
CONTROL_TIMES = {
    "Hayalhanem Mersin":     [("Monday", "19:00"), ("Wednesday", "19:00"), ("Friday", "19:00"), ("Sunday", "19:00")],
    "Mehmet Yıldız":         [("Tuesday", "19:00"), ("Thursday", "19:00"), ("Saturday", "19:00")],
    "Hayalhanem İstanbul":   [("Tuesday", "18:00"), ("Thursday", "18:00")],
    "Hayalhanem Ankara":     [("Tuesday", "19:30"), ("Thursday", "19:30")],
    "Hayalhanem Almanya":    [("Thursday", "20:00")],
}

# 2 haftada bir kontrol yapılacak kanallar
BIWEEKLY = {
    "Hayalhanem Ankara": [("Thursday", "19:30")]
}


def should_run_today(channel_name, day):
    if channel_name not in BIWEEKLY:
        return True
    today = datetime.date.today()
    iso_week = today.isocalendar()[1]  # hafta numarası
    # Tek haftalarda çalışacak şekilde ayarlandı
    return iso_week % 2 == 1


def was_video_uploaded_today(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"
    response = requests.get(url)
    if response.status_code != 200:
        return "⚠️ API hatası"

    data = response.json()
    if "items" not in data or len(data["items"]) == 0:
        return "❌ Video yok"

    latest_video = data["items"][0]
    published_at = latest_video["snippet"]["publishedAt"]
    published_date = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()
    today = datetime.date.today()

    return "✅ Video var" if published_date == today else "❌ Video yok"


def check_and_report():
    now = datetime.datetime.now()
    current_day = now.strftime("%A")  # e.g., "Monday"
    current_time = now.strftime("%H:%M")  # e.g., "19:00"

    report_lines = [f"📅 {current_day} {current_time} Kontrol Raporu:\n"]

    for channel_name, times in CONTROL_TIMES.items():
        for day, time in times:
            if current_day == day and current_time == time:
                if channel_name in BIWEEKLY and (day, time) in BIWEEKLY[channel_name]:
                    if not should_run_today(channel_name, current_day):
                        report_lines.append(f"⏭️ {channel_name}: Bu hafta kontrol yapılmıyor.")
                        continue
                result = was_video_uploaded_today(CHANNELS[channel_name]["id"])
                report_lines.append(f"{channel_name}: {result}")

    # Sadece bir şey kontrol edildiyse mesaj gönder
    if len(report_lines) > 1:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="\n".join(report_lines))


if __name__ == "__main__":
    check_and_report()
