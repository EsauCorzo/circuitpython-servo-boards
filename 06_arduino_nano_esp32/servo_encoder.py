# Servo controlado por encoder rotatorio - Arduino Nano ESP32
# Guardar como code.py en CIRCUITPY.
# Requiere: carpeta adafruit_motor en CIRCUITPY/lib/
#
# Los pines se cambian en la seccion CONFIGURACION. Para ver que pines
# existen en tu placa, ejecuta en el REPL:  import board; print(dir(board))
#
# Cableado:
#   Servo signal -> D2  | Servo rojo -> 5V externo | Servo negro -> GND
#   Encoder CLK (A) -> D3
#   Encoder DT  (B) -> D4
#   Encoder SW (boton) -> D5
#   Encoder + -> 3V3  | Encoder GND -> GND

import time
import board
import pwmio
import rotaryio
import digitalio
from adafruit_motor import servo

# ---------------- CONFIGURACION ----------------
# Pines para Arduino Nano ESP32 (nombres de la serigrafia Arduino)
SERVO_PIN = board.D2
ENC_A_PIN = board.D3
ENC_B_PIN = board.D4
BUTTON_PIN = board.D5

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
