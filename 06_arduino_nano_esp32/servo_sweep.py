# Servo test - arduino_nano_esp32 - adafruit_motor, barrido
# Senal del servo en D2. Guardar como code.py en CIRCUITPY.

import time
import board
import pwmio
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.D2, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2400)  # ajustar al servo

while True:
    for angle in range(0, 181, 5):
        my_servo.angle = angle
        time.sleep(0.03)
    for angle in range(180, -1, -5):
        my_servo.angle = angle
        time.sleep(0.03)
