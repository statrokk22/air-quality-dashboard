import streamlit as st
import requests
import matplotlib.pyplot as plt
import platform

# ===== 스타일 설정 =====
st.set_page_config(page_title="아름동 대기질", page_icon="🌫️")

def get_pm25_grade_color(value):
    value = int(value)
    if value <= 15:
        return "🟢 좋음", "#A0D468"
    elif value <= 35:
        return "🟡 보통", "#FFCE54"
    elif value <= 75:
        return "🟠 나쁨", "#FC6E51"
    else:
        return "🔴 매우 나쁨", "#ED5565"

# ===== API 호출 =====
API_KEY = "5%2BbNworyK7gQMq%2Fn%2BMuoiJH0FP13DqNIV0ZVfdiNouI0N8ceNUdlQc7joe%2BAnaqCuOGM1w88vXSjr6ARLZnsnA%3D%3D"
STATION_NAME = "아름동"

url = f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey={API_KEY}&returnType=json&numOfRows=1&pageNo=1&stationName={STATION_NAME}&dataTerm=DAILY&ver=1.3"
response = requests.get(url)
item = response.json()['response']['body']['items'][0]

# ===== 데이터 파싱 =====
pm10 = int(item['pm10Value'])
pm25 = int(item['pm25Value'])
data_time = item['dataTime']
grade, color = get_pm25_grade_color(pm25)

# ===== 상단 알림 카드 =====
st.markdown(
    f"""
    <div style='background-color:{color}; padding: 1rem; border-radius: 10px; text-align:center; color: white; font-size: 1.2rem'>
        🌫️ <b>{STATION_NAME}</b> 실시간 대기질<br>
        PM2.5: <b>{pm25} ㎍/㎥</b> → <b>{grade}</b><br>
        <span style='font-size: 0.9rem'>({data_time} 기준)</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ===== 미세먼지 그래프 =====
times = ["09:00", "10:00", "11:00", "12:00"]  # 예시
pm10_list = [30, 40, 35, pm10]
pm25_list = [15, 22, 27, pm25]

fig, ax = plt.subplots()
ax.plot(times, pm10_list, label="PM10", marker="o")
ax.plot(times, pm25_list, label="PM2.5", marker="o")
ax.set_title("최근 대기질 추이")
ax.set_ylabel("㎍/㎥")
ax.legend()
st.pyplot(fig)
