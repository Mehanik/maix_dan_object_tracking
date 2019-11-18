from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO
from main import main
import utime

test_pin = 16
fpioa = FPIOA()
fpioa.set_function(test_pin, FPIOA.GPIO7)
test_gpio = GPIO(GPIO.GPIO7, GPIO.IN)
lcd.init(color=(255, 0, 0))
lcd.direction(lcd.YX_LRUD)
lcd.draw_string(lcd.width() // 2 - 68,
                lcd.height() // 2 - 4, "Hackspace NSU", lcd.WHITE, lcd.RED)
utime.sleep(2)

if test_gpio.value() == 0:
    print('PIN 16 pulled down, enter test mode')
    # import sensor
    # import image
    # sensor.reset()
    # sensor.set_pixformat(sensor.RGB565)
    # sensor.set_framesize(sensor.QVGA)
    # sensor.run(1)
    # lcd.freq(16000000)
    # while True:
    #     img = sensor.snapshot()
    #     lcd.display(img)
else:
    main()
