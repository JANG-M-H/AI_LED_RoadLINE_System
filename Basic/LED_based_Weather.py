import requests
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time
import board
import neopixel
import datetime

LED_PIN = board.D18  # GPIO 18을 사용 (또는 사용하는 핀에 맞게 변경)
LED_COUNT = 72  # 사용하는 LED 개수
ORDER = neopixel.GRB  # NeoPixel의 색상 순서 (GRB는 일반적인 설정)
BRIGHTNESS = 0.5

pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, pixel_order=ORDER, brightness=BRIGHTNESS, auto_write=False)

def season():
    current_time = datetime.datetime.now()
    c_hour = current_time.hour
    c_month = current_time.month
    
    if 3 <= c_month <= 8:
        season = 'summer'
    else:
        season = 'winter'
        
    if season == 'summer' and (19 <= c_hour <= 23 or 0 <= c_hour <= 6):
        a = 1
    else:
        a = 0
        
    if season == 'winter' and (15 <= c_hour <= 23 or 0 <= c_hour <= 7): #later change 15->19
        a = 1
    else:
        a = 0
        
    return a


def croling():
    # API에서 데이터 가져오기
    url = 'http://api.weatherapi.com/v1/current.xml?key=99aeb4dcebda42d2bb650219232708&q=incheon&aqi=yes'
    resp = requests.get(url)
    xml_string = resp.content  # API 응답의 내용을 가져옴
    # XML 파싱
    root = ET.fromstring(xml_string)
    location = root.find(".//name").text
    time_1 = root.find(".//localtime").text
    update = root.find(".//last_updated").text
    temperature_c = root.find(".//temp_c").text
    humidity = root.find(".//humidity").text
    mm = root.find(".//precip_mm").text
    cloud = root.find(".//cloud").text

    if cloud == '1':
        sky = "bad"
    elif mm != '0':
        sky = "snow_rain"
    else :
        sky = "sunny"
    
    return sky

try:
    while True:
        a = season()
        
        if a == 1:
            sky = croling()
            
            print(f"상태: {sky}")
            
            if sky == "sunny":
                #pass
                pixels.fill((0, 255, 0))
                pixels.show()
            
            if sky == "bad":
                pixels.fill((255, 255, 255))
                pixels.show()                
            
            if sky == "snow_rain":
                pixels.fill((0, 0, 255))
                pixels.show()
                
            time.sleep(1)
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(1)
        
        
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()
