import requests
from decouple import config

token = config("TELEGRAM_BOT_TOKEN") 
# 자동으로 .env파일을 찾아서 안에 있는 값의 Key값을 톻해 해당 값을 가지고 온다

url = f"https://api.telegram.org/bot{token}/getUpdates" # chatbot 정보 업데이트

print(url) # 결과 url을 확인하기 위해서 사용

res = requests.get(url).json() # JSON >> dict형식으로 바꿀려고
print(res) # 결과 출력

# print(res["result"][0]["message"]["from"]["id"]) # dict에서 원하는 데이터로 접근
# 어떤 user_id가 말을 걸었는지를 확인하기 위한 id 추출

user_input = input("입력 : ")
chat_id = res["result"][0]["message"]["from"]["id"]

url = f"https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={chat_id}" # Message전송을 위한

requests.get(url) 
