import requests
import csv
import os
from datetime import datetime

# API 정보
API_KEY = "5%2BbNworyK7gQMq%2Fn%2BMuoiJH0FP13DqNIV0ZVfdiNouI0N8ceNUdlQc7joe%2BAnaqCuOGM1w88vXSjr6ARLZnsnA%3D%3D"
STATION_NAME = "아름동"

# 등급 판별 함수
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

# API 호출
url = (
    f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/"
    f"getMsrstnAcctoRltmMesureDnsty?serviceKey={API_KEY}"
    f"&returnType=json&numOfRows=1&pageNo=1"
    f"&stationName={STATION_NAME}&dataTerm=DAILY&ver=1.3"
)

response = requests.get(url)
data = response.json()
item = data['response']['body']['items'][0]

# 데이터 정리
now = datetime.now().strftime("%Y-%m-%d %H:%M")
pm10 = item['pm10Value']
pm25 = item['pm25Value']

row = {
    "시간": now,
    "PM10": pm10,
    "PM10 등급": get_pm10_grade(pm10),
    "PM2.5": pm25,
    "PM2.5 등급": get_pm25_grade(pm25)
}

# CSV 파일 저장
file_exists = os.path.isfile("data.csv")
with open("data.csv", "a", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)

print("✅ 데이터 저장 완료:", row)