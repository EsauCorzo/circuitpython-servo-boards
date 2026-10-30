# Servo controlado por encoder rotatorio - Raspberry Pi Pico
# Guardar como code.py en CIRCUITPY.
# Requiere: carpeta adafruit_motor en CIRCUITPY/lib/
#
# Los pines se cambian en la seccion CONFIGURACION. Para ver que pines
# existen en tu placa, ejecuta en el REPL:  import board; print(dir(board))
#
# Cableado:
#   Servo signal -> GP15 (pin fisico 20)
#   Servo rojo -> VBUS (pin 40) o 5V externo | Servo negro -> GND
#   Encoder CLK (A) -> GP2 (pin fisico 4)
#   Encoder DT  (B) -> GP3 (pin fisico 5)   (A y B deben ser pines consecutivos)
#   Encoder SW (boton) -> GP4 (pin fisico 6)
#   Encoder + -> 3V3 (pin 36)  | Encoder GND -> GND (pin 38)

import time
import board
import pwmio
import rotaryio
import digitalio
from adafruit_motor import servo

# ---------------- CONFIGURACION ----------------
# Pines para Raspberry Pi Pico
SERVO_PIN = board.GP15
ENC_A_PIN = board.GP2
ENC_B_PIN = board.GP3   # debe ser el pin siguiente a ENC_A_PIN
BUTTON_PIN = board.GP4

STEP = 5            # grados por cada click del encoder
MIN_ANGLE = 0
MAX_ANGLE = 180
CENTER_ANGLE = 90
# ------------------------------------------------

# Servo
pwm = pwmio.PWMOut(SERVO_PIN, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2400)  # ajustar al servo

# Encoder
encoder = rotaryio.IncrementalEncoder(ENC_A_PIN, ENC_B_PIN)

# Boton del encoder (pull-up interno, activo en bajo)
button = digitalio.DigitalInOut(BUTTON_PIN)
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
