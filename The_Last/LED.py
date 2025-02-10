import requests
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time
import board
import neopixel
import datetime
import serial
import cv2
import torch

# NeoPixel 설정
LED_PIN = board.D18
LED_COUNT = 72
ORDER = neopixel.GRB
BRIGHTNESS = 0.5

pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, pixel_order=ORDER, brightness=BRIGHTNESS, auto_write=False)

# GPIO 핀 설정
SWITCH_BLUE_PIN = 27  # 파란색 LED 버튼
SWITCH_RED_PIN = 22   # 빨간색 LED 버튼
BUZZER_PIN = 17       # 부저 핀

GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_BLUE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_RED_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 시리얼 통신 (아두이노)
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='car.pt')
model.conf = 0.5  # 감지 임계값 설정

# LED 상태 변수
blue_led_active = False
red_led_active = False

def season():
    """현재 시간과 계절 판단"""
    current_time = datetime.datetime.now()
    c_hour = current_time.hour
    c_month = current_time.month

    if 3 <= c_month <= 8:  # 여름
        return 1 if (19 <= c_hour <= 23 or 0 <= c_hour <= 6) else 0
    else:  # 겨울
        return 1 if (18 <= c_hour <= 23 or 0 <= c_hour <= 7) else 0

def weather_status():
    """WeatherAPI를 통해 날씨 상태 가져오기"""
    API_KEY = 'YOUR_WEATHER_API_KEY'
    url = f'http://api.weatherapi.com/v1/current.xml?key={API_KEY}&q=incheon&aqi=yes'
    resp = requests.get(url)

    if resp.status_code != 200:
        print("WeatherAPI 요청 실패:", resp.status_code)
        return "unknown"

    root = ET.fromstring(resp.content)
    mm = root.find(".//precip_mm").text
    cloud = root.find(".//cloud").text

    if cloud == '1':
        return "bad"
    elif mm != '0':
        return "snow_rain"
    else:
        return "sunny"

def detect_cars(frame):
    """YOLOv5 모델을 사용하여 자동차 감지"""
    results = model(frame)
    detected_objects = results.pandas().xyxy[0]
    car_count = len(detected_objects[detected_objects['name'] == 'car'])
    return car_count

try:
    cap = cv2.VideoCapture(0)  # 카메라 연결
    
    while True:
        if season() == 1:  # 계절과 시간이 합당한 경우
            # 아두이노에서 센서 값 수신
            arduino_value = arduino.readline().decode('utf-8').strip()
            rain_value = int(arduino_value) if arduino_value.isdigit() else 0
            
            # 날씨 상태 가져오기
            sky = weather_status()
            print(f"Weather: {sky}, Rain Sensor: {rain_value}")
            
            # Snow_rain 상태 처리 (파란색 LED가 활성화 중이 아닐 때만)
            if sky == "snow_rain" and not blue_led_active:
                print("It's snowy")  # 터미널 출력
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(5)  # 부저 5초 울림
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                

            # 버튼 입력 확인
            if GPIO.input(SWITCH_BLUE_PIN) == GPIO.LOW:  # 파란색 LED 버튼
                if red_led_active:  # 빨간색 LED가 활성화 상태면 무효화
                    print("경고: 빨간색 LED가 활성화 중입니다. 파란색 LED 버튼이 무효화되었습니다.")
                else:
                    blue_led_active = not blue_led_active
                    print(f"파란색 LED 상태: {'활성화' if blue_led_active else '비활성화'}")
                time.sleep(0.2)  # 버튼 debounce

            if GPIO.input(SWITCH_RED_PIN) == GPIO.LOW:  # 빨간색 LED 버튼
                if blue_led_active:  # 파란색 LED가 활성화 상태면 무효화
                    print("경고: 파란색 LED가 활성화 중입니다. 빨간색 LED 버튼이 무효화되었습니다.")
                else:
                    red_led_active = not red_led_active
                    print(f"빨간색 LED 상태: {'활성화' if red_led_active else '비활성화'}")
                time.sleep(0.2)  # 버튼 debounce

            # 카메라에서 프레임 읽기
            ret, frame = cap.read()
            if not ret:
                print("카메라 프레임을 읽을 수 없습니다.")
                continue

            # 자동차 감지 (빨간색 LED가 활성화 중이 아닐 때만)
            if not red_led_active:
                car_count = detect_cars(frame)
                print(f"Detected cars: {car_count}")

                # 자동차가 10대 이상 감지되면 부저 울리기
                if car_count >= 10:
                    print("자동차가 10대 이상 감지되었습니다. 부저를 울립니다!")
                    GPIO.output(BUZZER_PIN, GPIO.HIGH)
                    time.sleep(5)  # 5초 동안 부저 울리기
                    GPIO.output(BUZZER_PIN, GPIO.LOW)

            # LED 제어
            if blue_led_active:
                pixels.fill((0, 0, 255))  # 파란색
                pixels.show()
                time.sleep(1)
                pixels.fill((0, 0, 0))  # OFF
                pixels.show()
                time.sleep(1)

            elif red_led_active:
                pixels.fill((255, 0, 0))  # 빨간색
                pixels.show()
                time.sleep(1)
                pixels.fill((0, 0, 0))  # OFF
                pixels.show()
                time.sleep(1)

            elif sky == "bad" and rain_value > 50:  # 흰색 LED 조건
                pixels.fill((255, 255, 255))  # 흰색
                pixels.show()
                time.sleep(1)
                pixels.fill((0, 0, 0))  # OFF
                pixels.show()
                time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated.")
    cap.release()
    cv2.destroyAllWindows()
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()
