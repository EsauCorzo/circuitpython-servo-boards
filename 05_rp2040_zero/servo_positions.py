# Servo test - rp2040_zero - adafruit_motor, posiciones
# Senal del servo en GP6. Guardar como code.py en CIRCUITPY.

import time
import board
import pwmio
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.GP6, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2400)  # ajustar al servo

while True:
    for angle in (0, 90, 180, 90):
        print("angle:", angle)
        my_servo.angle = angle
        time.sleep(1)
