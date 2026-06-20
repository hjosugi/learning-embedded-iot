"""MicroPython hands-on for the Raspberry Pi Pico / Pico 2 (RP2040 / RP2350).

Three classic microcontroller "hello world" exercises in one file:

1. GPIO blink      - turn an LED on and off via ``machine.Pin``.
2. PWM breathing   - fade an LED smoothly with ``machine.PWM`` + ``duty_u16``.
3. ADC read        - sample an analog input (pot / temperature) via ``machine.ADC``.

THE WHOLE POINT: this file imports ``machine`` and uses only MicroPython APIs.
It runs on your laptop *today* through the host shim in ``machine.py`` (no
hardware, no pip install), and the EXACT SAME file later flashes UNCHANGED to a
Pico, where the firmware supplies the real ``machine`` module. See README.md.

Host vs. hardware loop count
----------------------------
On a microcontroller a blink program loops forever::

    while True:
        led.toggle()
        sleep(0.5)

That never terminates, which is wrong for tests/CI on a host. So the demos below
take a bounded ``iterations`` argument and the host entry point passes a small
number. On real hardware you would call these with a ``while True`` loop (or pass
a large/forever count) - the comments show exactly where.

Wiring note (real hardware): the Pico has a built-in LED on the pin named
"LED", so blink/breathe work with no wiring at all. To use an external LED,
connect GPIO15 -> 330 ohm resistor -> LED anode (long leg) -> LED cathode -> GND,
and change ``LED_PIN`` below to ``15``.
"""

from __future__ import annotations

from machine import ADC, PWM, Pin
from time import sleep

# --- Board configuration -----------------------------------------------------
# "LED" is the Pico/Pico 2 onboard LED. Use an int (e.g. 15) for an external LED.
LED_PIN = "LED"
# ADC channel 26 is GPIO26 (ADC0) on the Pico header - wire a potentiometer's
# wiper here. machine.ADC(4) reads the on-die temperature sensor instead.
ADC_PIN = 26
PWM_FREQ_HZ = 1000


def blink(led: Pin, iterations: int, delay: float = 0.1) -> int:
    """Blink ``led`` ``iterations`` times. Returns the number of toggles done.

    On hardware you'd typically wrap this in ``while True`` and use a larger
    delay (e.g. 0.5s). We keep it bounded + fast so the host run terminates.
    """
    toggles = 0
    for _ in range(iterations):
        led.on()
        sleep(delay)
        led.off()
        sleep(delay)
        toggles += 2
    return toggles


def breathe(pwm: PWM, steps: int) -> list[int]:
    """Fade an LED up and down via PWM. Returns the duty values written.

    ``duty_u16`` takes 0..65535. We ramp up then back down so the LED appears to
    "breathe". On hardware this is the same code; the slice drives the pad.
    """
    duties: list[int] = []
    # Ramp up.
    for i in range(steps):
        duty = int(65535 * (i / max(1, steps - 1)))
        pwm.duty_u16(duty)
        duties.append(duty)
        sleep(0.01)
    # Ramp back down.
    for i in range(steps):
        duty = int(65535 * (1 - i / max(1, steps - 1)))
        pwm.duty_u16(duty)
        duties.append(duty)
        sleep(0.01)
    return duties


def read_potentiometer(adc: ADC, samples: int) -> list[int]:
    """Take ``samples`` ADC readings. Returns the raw 16-bit values.

    On hardware these are real conversions (e.g. a pot wiper or temperature).
    On the host the shim returns a deterministic simulated signal.
    """
    readings: list[int] = []
    for _ in range(samples):
        readings.append(adc.read_u16())
        sleep(0.01)
    return readings


def u16_to_celsius(raw: int) -> float:
    """Convert a raw RP2040 temp-sensor ADC count to approximate Celsius.

    The RP2040 datasheet formula assumes a 3.3V / 12-bit reference; ``read_u16``
    left-aligns the 12-bit sample into 16 bits, so divide by 65535. This is the
    same arithmetic you'd run on the board for the on-die sensor.
    """
    voltage = raw / 65535 * 3.3
    return 27.0 - (voltage - 0.706) / 0.001721


def run(blink_iters: int = 5, breathe_steps: int = 16, adc_samples: int = 8) -> dict:
    """Run all three demos once and return a summary dict.

    The host entry point calls this with small counts so it terminates. On real
    hardware, call the demos inside ``while True`` for continuous operation.
    """
    led = Pin(LED_PIN, Pin.OUT)
    toggles = blink(led, blink_iters)

    pwm = PWM(Pin(LED_PIN), freq=PWM_FREQ_HZ)
    duties = breathe(pwm, breathe_steps)
    pwm.duty_u16(0)  # leave the LED off
    pwm.deinit()

    adc = ADC(ADC_PIN)
    readings = read_potentiometer(adc, adc_samples)

    return {
        "toggles": toggles,
        "max_duty": max(duties),
        "min_duty": min(duties),
        "adc_readings": readings,
        "adc_celsius_first": round(u16_to_celsius(readings[0]), 2),
    }


# On real hardware you would usually replace the bounded call below with a
# forever loop, e.g.:
#
#     led = Pin(LED_PIN, Pin.OUT)
#     while True:
#         led.toggle()
#         sleep(0.5)
#
# On the host we run a bounded pass so the program ends and CI can check it.
if __name__ == "__main__":
    summary = run()
    print("summary:", summary)
