# Servo controlado por encoder rotatorio - Waveshare RP2040-Zero
# Guardar como code.py en CIRCUITPY.
# Requiere: carpeta adafruit_motor en CIRCUITPY/lib/
#
# Cableado:
#   Servo signal -> GP6   | Servo rojo -> 5V | Servo negro -> GND
#   Encoder CLK (A) -> GP2
#   Encoder DT  (B) -> GP3   (A y B deben ser pines consecutivos)
#   Encoder SW (boton) -> GP4
#   Encoder + -> 3V3  | Encoder GND -> GND

import time
import board
import pwmio
import rotaryio
import digitalio
from adafruit_motor import servo

STEP = 5            # grados por cada click del encoder
MIN_ANGLE = 0
MAX_ANGLE = 180
CENTER_ANGLE = 90

# Servo
pwm = pwmio.PWMOut(board.GP6, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2400)  # ajustar al servo

# Encoder
encoder = rotaryio.IncrementalEncoder(board.GP2, board.GP3)

# Boton del encoder (pull-up interno, activo en bajo)
button = digitalio.DigitalInOut(board.GP4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

angle = CENTER_ANGLE
my_servo.angle = angle
last_position = encoder.position
last_button = button.value

print("Angulo:", angle)

while True:
    # Giro del encoder
    position = encoder.position
    if position != last_position:
        angle += (position - last_position) * STEP
        angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))
        my_servo.angle = angle
        last_position = position
        print("Angulo:", angle)

    # Boton: centrar el servo
    current_button = button.value
    if last_button and not current_button:
        angle = CENTER_ANGLE
        my_servo.angle = angle
        print("Centrado:", angle)
        time.sleep(0.05)  # antirrebote
    last_button = current_button

    time.sleep(0.005)
