import time
import serial
import RPi.GPIO as GPIO
import board
import neopixel

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
LED_PIN = board.D18  # GPIO 18을 사용 (또는 사용하는 핀에 맞게 변경)
LED_COUNT = 72  # 사용하는 LED 개수
ORDER = neopixel.GRB  # NeoPixel의 색상 순서 (GRB는 일반적인 설정)
BRIGHTNESS = 0.5

pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, pixel_order=ORDER, brightness=BRIGHTNESS, auto_write=False)

def main():
    port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=None)
    while True:
        line = port.readline()
        arr = line.split()
        
        digit = float(arr[0])
        print(digit)
        
        
        if digit >= 30:
            pixels.fill((0, 255, 0))
            pixels.show()
            time.sleep(2)
        else:
            time.sleep(2)
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(2)
try:
    while True:
        if __name__ == "__main__":
            main()
    
finally:
    pixels.fill((0, 0, 0))
    pixels.show()