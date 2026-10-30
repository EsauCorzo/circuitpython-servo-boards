# CircuitPython servo + encoder en varias placas

Scripts de prueba para controlar un servo con la libreria `adafruit_motor`,
y para controlarlo con un encoder rotatorio. Un mismo conjunto de tres scripts por placa.

## Scripts por placa

| Script | Que hace |
|---|---|
| `servo_sweep.py` | Barrido continuo del servo de 0 a 180 grados y de vuelta |
| `servo_positions.py` | Lleva el servo a 0, 90, 180 y 90 grados en bucle |
| `servo_encoder.py` | El encoder mueve el servo (5 grados por click); el boton lo centra a 90 |

## Placas y pines

| Carpeta | Placa | Servo | Encoder A / B / SW |
|---|---|---|---|
| `01_stm32_blackpill_f411ce` | STM32F411CE Black Pill | A0 | B12 / B13 / B14 |
| `02_esp32s3_n16r8` | ESP32-S3 N16R8 | IO4 | IO5 / IO6 / IO7 |
| `03_esp32c6_supermini` | ESP32-C6 SuperMini | IO2 | IO0 / IO1 / IO3 |
| `04_raspberry_pi_pico` | Raspberry Pi Pico | GP15 | GP2 / GP3 / GP4 |
| `05_rp2040_zero` | Waveshare RP2040-Zero | GP6 | GP2 / GP3 / GP4 |
| `06_arduino_nano_esp32` | Arduino Nano ESP32 | D2 | D3 / D4 / D5 |

Cableado comun: servo rojo a 5V (fuente externa recomendada), servo negro a GND
(compartido con la placa), encoder `+` a 3V3, encoder GND a GND.

## Uso

1. Instala CircuitPython en la placa con el firmware de tu modelo exacto (circuitpython.org).
2. Mira la primera linea de `boot_out.txt` en la unidad CIRCUITPY para saber tu version.
3. Descarga el bundle de librerias **mpy** con la misma version mayor (circuitpython.org/libraries).
4. Copia la carpeta `adafruit_motor` del bundle a `CIRCUITPY/lib/`.
5. Copia el script que quieras a `CIRCUITPY/code.py`.

## Notas

- En el RP2040 (Pico y Zero), los pines A y B del encoder deben ser consecutivos.
- En el STM32 Black Pill, `rotaryio` no se usa: el encoder se decodifica por software.
- Los pines estan en la seccion CONFIGURACION de `servo_encoder.py` en las placas ESP32, Pico y Nano; en el resto, editalos directamente en el codigo.
- Si `board.IO4` (u otro nombre) falla, ejecuta `import board; print(dir(board))` en el REPL.
- Si hay `Incompatible .mpy file`, la version del bundle no coincide con la del firmware.
