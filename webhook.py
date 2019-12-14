from decouple import config

token = config("TELEGRAM_BOT_TOKEN")
# ngrok_url = "https://07a5716b.ngrok.io/telegram"
ngrok_url = "https://uhuikim.pythonanywhere.com/telegram"

url = f"https://api.telegram.org/bot{token}/setWebhook"

setwebhook_url = f"{url}?url={ngrok_url}" 
# setWebhook은 url을 필수로 필요로 한다

print(setwebhook_url)