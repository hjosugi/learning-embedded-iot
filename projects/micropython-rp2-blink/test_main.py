"""Tests for the MicroPython RP2 blink hands-on, run on CPython via the shim.

These import ``main`` (which imports ``machine`` -> the host shim in this
directory) and assert that GPIO toggles, PWM duty writes, and ADC reads actually
happened. No hardware is touched.

Run non-interactively (exits non-zero on failure):

    python3 -m unittest discover \
        -s /mnt/data/workspace/learning-embedded-iot/projects/micropython-rp2-blink \
        -p 'test_*.py'
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

# Keep shim output quiet during tests, and make sure THIS directory wins on the
# import path so `import machine` resolves to the host shim, not anything else.
os.environ["MACHINE_SHIM_QUIET"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import machine  # noqa: E402  (path set above)
import main  # noqa: E402


class BlinkTest(unittest.TestCase):
    def setUp(self) -> None:
        machine.reset_events()

    def test_blink_toggles_pin(self) -> None:
        led = machine.Pin("LED", machine.Pin.OUT)
        toggles = main.blink(led, iterations=3, delay=0)
        self.assertEqual(toggles, 6)
        pin_events = [e for e in machine.events() if e.kind == "pin"]
        # 3 iterations * (on + off) == 6 writes.
        self.assertEqual(len(pin_events), 6)
        # The final write leaves the LED off.
        self.assertEqual(pin_events[-1].value, 0)
        self.assertEqual(led.value(), 0)

    def test_pin_on_off_toggle(self) -> None:
        led = machine.Pin(15, machine.Pin.OUT)
        led.on()
        self.assertEqual(led.value(), 1)
        led.off()
        self.assertEqual(led.value(), 0)
        led.toggle()
        self.assertEqual(led.value(), 1)

    def test_breathe_writes_full_duty_range(self) -> None:
        pwm = machine.PWM(machine.Pin("LED"), freq=1000)
        duties = main.breathe(pwm, steps=8)
        self.assertEqual(pwm.freq(), 1000)
        # Ramp up + ramp down -> 16 duty writes.
        self.assertEqual(len(duties), 16)
        # Reaches (near) full brightness and returns to off.
        self.assertEqual(max(duties), 65535)
        self.assertEqual(duties[0], 0)
        duty_events = [e for e in machine.events() if e.action == "duty_u16"]
        self.assertEqual(len(duty_events), 16)

    def test_duty_u16_is_clamped(self) -> None:
        pwm = machine.PWM(machine.Pin("LED"))
        pwm.duty_u16(999999)
        self.assertEqual(pwm.duty_u16(), 65535)
        pwm.duty_u16(-5)
        self.assertEqual(pwm.duty_u16(), 0)

    def test_adc_reads_are_in_range_and_logged(self) -> None:
        adc = machine.ADC(26)
        readings = main.read_potentiometer(adc, samples=5)
        self.assertEqual(len(readings), 5)
        for value in readings:
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 65535)
        adc_events = [e for e in machine.events() if e.kind == "adc"]
        self.assertEqual(len(adc_events), 5)

    def test_temperature_conversion_is_reasonable(self) -> None:
        # Mid-scale-ish reading should map to a plausible room temperature.
        celsius = main.u16_to_celsius(13800)  # ~0.7V left-aligned
        self.assertGreater(celsius, -40.0)
        self.assertLess(celsius, 125.0)

    def test_run_end_to_end(self) -> None:
        summary = main.run(blink_iters=4, breathe_steps=10, adc_samples=6)
        self.assertEqual(summary["toggles"], 8)
        self.assertEqual(summary["max_duty"], 65535)
        self.assertEqual(summary["min_duty"], 0)
        self.assertEqual(len(summary["adc_readings"]), 6)
        # The full run exercised all three peripheral kinds.
        kinds = {e.kind for e in machine.events()}
        self.assertEqual(kinds, {"pin", "pwm", "adc"})


if __name__ == "__main__":
    unittest.main()
