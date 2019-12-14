from flask import Flask, escape, request, render_template
from decouple import config
import requests

app = Flask(__name__)

api_url = "https://api.telegram.org/bot"
token = config("TELEGRAM_BOT_TOKEN") 
google_key=config('GOOGLE_KEY')


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route("/write")
def write():
    return render_template("write.html")

@app.route("/send")
def send():
    user_input = request.args.get("user_input")

    #아이디 찾기위해서 url을 가져옴
    get_update = f"{api_url}{token}/getUpdates"

    res = requests.get(get_update).json()
    chat_id = res["result"][0]["message"]["from"]["id"]

    send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={chat_id}"
    requests.get(send_url)
    
    return render_template("send.html", user_input = user_input)


@app.route("/telegram", methods = ["post"])
def telegram():
    req = request.get_json()
    print(req)
    user_id=req["message"]['from']['id']
    user_input = req['message']['text'] 


    if user_input == "로또":
        return_data = "로또를 입력하셨습니다. "
    elif user_input == "안녕":
        return_data = "안녕하세요"
    #앞 두글자가 번역일때 번역 실행 / 슬래싱으로 앞 두글자를 빼냄
    elif user_input[0:2] == '번역':
        google_api_url="https://translation.googleapis.com/language/translate/v2"
        #사용자가 넣은 데이터를 가져온다. 앞에 번역 두글자와 띄어쓰기 한칸을 뺀 나머지 글자 가져오기
        before_text =  user_input[3:]
        #구글 api에 번역을 요청한다. 
        #필수적으로 필요한 3가지 요소 q(번역전 텍스트),source(원본 언어),target(번역하고 싶은 언어)
        data = {'q':before_text,
                'source': 'ko',
                'target': 'en'}
        #지금까지 requests에는 get을 썼는데 구글은 post요청을 보내야함
        #?는 get방식으로 데이터를 가져오겠다? 구글 키는env 에 있음
        #맨 위에 google_key=config('GOOGLE_KEY') 추가
        request_url = f'{google_api_url}?key={google_key}'
        #데이터가 json 타입으로 온다.
        res= requests.post(request_url,data).json()
        print(res)
        #플라스크 서버에 있는 번역된 텍스트를 뽑아냄
        return_data = res['data']['translations'][0]['translatedText']
    else:
        return_data = "지금 사용가능한 명령어는 로또입니다. "

    #텔레그램 쳇봇이 대답하는 말  
    send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}"

    requests.get(send_url)
    return "ok", 200
# telegram은 지정한 url에 계속해서 요청을 보내게 된다
# 그래서 요청을 받았다는 200을 계속해서 telegram에게 전달을 해줘야 한다


if __name__ == "__main__":
    app.run(debug=True)