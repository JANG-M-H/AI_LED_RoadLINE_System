import RPi.GPIO as GPIO
import time
import board
import neopixel

LED_PIN_1 = board.D18  
LED_PIN_2 = board.D10
LED_PIN_3 = board.D21
LED_PIN_4 = board.D12

LED_COUNT = 72
LED_COUNT_1 = 72 #14
ORDER = neopixel.GRB

pixels1 = neopixel.NeoPixel(LED_PIN_1, LED_COUNT, pixel_order=ORDER, brightness=1 ,auto_write=False)
pixels2 = neopixel.NeoPixel(LED_PIN_2, LED_COUNT, pixel_order=ORDER, brightness=1 ,auto_write=False)          
pixels3 = neopixel.NeoPixel(LED_PIN_3, LED_COUNT, pixel_order=ORDER, brightness=1 ,auto_write=False)
pixels4 = neopixel.NeoPixel(LED_PIN_4, LED_COUNT, pixel_order=ORDER, brightness=1 ,auto_write=False)

try:
    while True:
        pixels1.fill((0, 0, 255)) #blue
        pixels1.show()
        
        pixels2.fill((255, 255, 0)) #yellow 255, 255, 0
        pixels2.show() 
        
        pixels3.fill((0, 255, 0)) #green  0, 255, 0
        pixels3.show()

        pixels4.fill((0, 255, 255)) #green  0, 255, 0
        pixels4.show()
        
        
except KeyboardInterrupt:
    pixels1.fill((0, 0, 0))
    pixels1.show()
    pixels2.fill((0, 0, 0))
    pixels2.show()
    pixels3.fill((0, 0, 0))
    pixels3.show()
    pixels4.fill((0, 0, 0))
    pixels4.show()

    GPIO.cleanup()        