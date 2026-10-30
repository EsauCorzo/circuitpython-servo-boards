# Servo controlado por encoder rotatorio - STM32F411CE Black Pill
# Guardar como code.py en CIRCUITPY.
# Requiere: carpeta adafruit_motor en CIRCUITPY/lib/
#
# Cableado:
#   Servo signal -> A0 (PA0)  | Servo rojo -> 5V | Servo negro -> GND
#   Encoder CLK (A) -> B12
#   Encoder DT  (B) -> B13
#   Encoder SW (boton) -> B14
#   Encoder + -> 3V3  | Encoder GND -> GND
#
# Nota: rotaryio no esta disponible en las builds de STM32, asi que el
# encoder se decodifica por software (lectura continua de los pines).

import time
import board
import pwmio
import digitalio
from adafruit_motor import servo

STEP = 5            # grados por cada click del encoder
MIN_ANGLE = 0
MAX_ANGLE = 180
CENTER_ANGLE = 90

# Servo
pwm = pwmio.PWMOut(board.A0, duty_cycle=0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2400)  # ajustar al servo


def make_input(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return io


enc_a = make_input(board.B12)
enc_b = make_input(board.B13)
button = make_input(board.B14)

# Tabla de decodificacion en cuadratura: indice = (estado_previo << 2) | estado_nuevo
QUAD_TABLE = (0, -1, 1, 0,
              1, 0, 0, -1,
              -1, 0, 0, 1,
              0, 1, -1, 0)

last_state = (enc_a.value << 1) | enc_b.value
sub_steps = 0       # un click del encoder = 4 transiciones

angle = CENTER_ANGLE
my_servo.angle = angle
last_button = button.value

print("Angulo:", angle)

while True:
    # Giro del encoder
    state = (enc_a.value << 1) | enc_b.value
    if state != last_state:
        sub_steps += QUAD_TABLE[(last_state << 2) | state]
        last_state = state
        click = 0
        if sub_steps >= 4:
            click = 1
            sub_steps = 0
        elif sub_steps <= -4:
            click = -1
            sub_steps = 0
        if click:
            angle = max(MIN_ANGLE, min(MAX_ANGLE, angle + click * STEP))
            my_servo.angle = angle
            print("Angulo:", angle)

    # Boton: centrar el servo
    current_button = button.value
    if last_button and not current_button:
        angle = CENTER_ANGLE
        my_servo.angle = angle
        print("Centrado:", angle)
        time.sleep(0.05)  # antirrebote
    last_button = current_button
