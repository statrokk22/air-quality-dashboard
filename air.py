import requests
from datetime import datetime

# ====== 설정 ======
API_KEY = "5%2BbNworyK7gQMq%2Fn%2BMuoiJH0FP13DqNIV0ZVfdiNouI0N8ceNUdlQc7joe%2BAnaqCuOGM1w88vXSjr6ARLZnsnA%3D%3D"
STATION_NAME = "아름동"

TELEGRAM_TOKEN = "8002713760:AAHqMSCt9tvMYupvUg-kOSBcVdOa0COVXO8"
CHAT_ID = "6128157766"

# ====== 함수 정의 ======

def get_pm10_grade(value):
    value = int(value)
    if value <= 30:
        return "좋음"
    elif value <= 80:
        return "보통"
    elif value <= 150:
        return "나쁨"
    else:
        return "매우 나쁨"

def get_pm25_grade(value):
    value = int(value)
    if value <= 15:
        return "좋음"
    elif value <= 35:
        return "보통"
    elif value <= 75:
        return "나쁨"
    else:
        return "매우 나쁨"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

# ====== API 호출 ======

url = (
    f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/"
    f"getMsrstnAcctoRltmMesureDnsty?serviceKey={API_KEY}"
    f"&returnType=json&numOfRows=1&pageNo=1"
    f"&stationName={STATION_NAME}&dataTerm=DAILY&ver=1.3"
)

response = requests.get(url)
data = response.json()
item = data['response']['body']['items'][0]

# ====== 데이터 추출 ======

pm10_value = int(item['pm10Value']) if item['pm10Value'].isdigit() else 0
pm25_value = int(item['pm25Value']) if item['pm25Value'].isdigit() else 0
data_time = item['dataTime']

# ====== 출력 ======
print(f"[{data_time}] {STATION_NAME}")
print(f"PM10: {pm10_value} ㎍/㎥ → {get_pm10_grade(pm10_value)}")
print(f"PM2.5: {pm25_value} ㎍/㎥ → {get_pm25_grade(pm25_value)}")

# ====== 알림 조건 및 전송 ======
if pm25_value > 35:
    message = f"""
📢 [대기질 경고]
{STATION_NAME} 초미세먼지(PM2.5): {pm25_value} ㎍/㎥ → {get_pm25_grade(pm25_value)} 😷
외출 시 마스크 착용하세요!
({data_time})
"""
    send_telegram_message(message)
    print("✅ 텔레그램 알림 전송 완료!")
else:
    print("ℹ️ 공기질 상태 양호 – 알림 전송 안 함.")


send_telegram_message("✅ 테스트용 텔레그램 알림입니다!")

requests.post(url, data=payload, verify=False)