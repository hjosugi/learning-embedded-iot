"""Host shim for MicroPython's ``machine`` module.

This file lets MicroPython-style code (``main.py``) run on plain CPython
*today*, with no hardware and no pip install. It re-implements only the slice
of the ``machine`` API surface that ``main.py`` uses: ``Pin``, ``PWM`` and
``ADC``.

On real hardware the firmware already ships a C-backed ``machine`` module, so
this file is NOT copied to the board. It exists purely so you can iterate on the
logic of ``main.py`` on a laptop and run tests in CI. See the "Upgrade path"
section of README.md.

Host behavior vs. hardware behavior:

- Hardware: these calls poke silicon registers (set a voltage on a pad, drive a
  PWM slice, sample the on-chip ADC).
- Host (this shim): these calls record their effect in memory and optionally log
  it, and ADC returns a deterministic *simulated* reading. Nothing physical
  happens, so it is safe to run anywhere.

The shim keeps a module-level event log so tests can assert that the expected
GPIO toggles / PWM duty writes / ADC reads actually happened.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Any

# ----------------------------------------------------------------------------
# Event log: every state change appends a record here so tests (and humans)
# can inspect what the program "did" without any hardware attached.
# ----------------------------------------------------------------------------


@dataclass
class Event:
    kind: str          # "pin", "pwm", or "adc"
    target: str        # which pin/peripheral, e.g. "Pin(LED)"
    action: str        # e.g. "value", "freq", "duty_u16", "read_u16"
    value: Any         # the value written or read


_EVENTS: list[Event] = []

# Set MACHINE_SHIM_QUIET=1 to silence the human-readable logging (tests do this
# so output stays clean). Logging is on by default so `python3 main.py` is
# educational.
_QUIET = os.environ.get("MACHINE_SHIM_QUIET") == "1"


def _log(message: str) -> None:
    if not _QUIET:
        print(f"[machine-shim] {message}")


def reset_events() -> None:
    """Clear the recorded event log. Tests call this between cases."""
    _EVENTS.clear()


def events() -> list[Event]:
    """Return the recorded events (host-only helper, not part of MicroPython)."""
    return list(_EVENTS)


# ----------------------------------------------------------------------------
# Pin: digital input/output.
# Real API: https://docs.micropython.org/en/latest/library/machine.Pin.html
# ----------------------------------------------------------------------------


class Pin:
    # Direction constants, mirroring MicroPython's class attributes.
    OUT = "OUT"
    IN = "IN"
    # Pull constants are accepted for API parity even though the host ignores
    # the electrical effect.
    PULL_UP = "PULL_UP"
    PULL_DOWN = "PULL_DOWN"

    def __init__(self, id: Any, mode: str = IN, pull: str | None = None) -> None:
        # `id` may be an int GPIO number or a named pin like "LED" on the Pico.
        self.id = id
        self.mode = mode
        self.pull = pull
        self._value = 0
        _log(f"Pin({id!r}) configured as {mode}")

    def __repr__(self) -> str:  # noqa: D401 - matches MicroPython repr style
        return f"Pin({self.id!r})"

    def value(self, val: int | None = None) -> int | None:
        """Read (no arg) or write (with arg) the pin level, like MicroPython."""
        if val is None:
            return self._value
        self._value = 1 if val else 0
        _EVENTS.append(Event("pin", repr(self), "value", self._value))
        _log(f"{self!r} <- {self._value}")
        return None

    def on(self) -> None:
        """Drive the pin high."""
        self.value(1)

    def off(self) -> None:
        """Drive the pin low."""
        self.value(0)

    def toggle(self) -> None:
        """Flip the pin between high and low."""
        self.value(0 if self._value else 1)


# ----------------------------------------------------------------------------
# PWM: pulse-width modulation, used here for the LED "breathing" fade.
# Real API: https://docs.micropython.org/en/latest/library/machine.PWM.html
# ----------------------------------------------------------------------------


class PWM:
    def __init__(self, dest: Pin, freq: int | None = None) -> None:
        self.dest = dest
        self._freq = 0
        self._duty = 0
        _log(f"PWM on {dest!r}")
        if freq is not None:
            self.freq(freq)

    def freq(self, value: int | None = None) -> int | None:
        """Read or set the PWM frequency in Hz."""
        if value is None:
            return self._freq
        self._freq = int(value)
        _EVENTS.append(Event("pwm", repr(self.dest), "freq", self._freq))
        _log(f"PWM {self.dest!r} freq={self._freq} Hz")
        return None

    def duty_u16(self, value: int | None = None) -> int | None:
        """Read or set the duty cycle as a 16-bit value (0..65535).

        On real hardware 0 is fully off and 65535 is fully on. On the host we
        only record the value.
        """
        if value is None:
            return self._duty
        self._duty = max(0, min(65535, int(value)))
        _EVENTS.append(Event("pwm", repr(self.dest), "duty_u16", self._duty))
        _log(f"PWM {self.dest!r} duty_u16={self._duty}")
        return None

    def deinit(self) -> None:
        """Stop the PWM. Real hardware frees the slice; host just logs it."""
        self._duty = 0
        _log(f"PWM {self.dest!r} deinit")


# ----------------------------------------------------------------------------
# ADC: analog-to-digital converter. On the host we synthesize a deterministic
# reading so tests are reproducible and the lesson has "data" to look at.
# Real API: https://docs.micropython.org/en/latest/library/machine.ADC.html
# ----------------------------------------------------------------------------


@dataclass
class _SimSource:
    """Deterministic fake signal for a simulated ADC channel.

    Defaults are centered so ``u16_to_celsius`` (the RP2040 temp-sensor
    formula) maps a reading to a plausible room temperature (~25 C), while the
    sine sweep still varies each sample like a turning potentiometer.
    """

    base: float = 14090.0      # ~0.71 V left-aligned -> ~25 C
    amplitude: float = 1200.0  # small drift, stays in a sane sensor range
    step: int = field(default=0)

    def sample(self) -> int:
        # A smooth sine sweep keeps successive reads varied but reproducible,
        # imitating a potentiometer being turned or a slowly drifting sensor.
        raw = self.base + self.amplitude * math.sin(self.step / 4.0)
        self.step += 1
        return int(max(0, min(65535, raw)))


class ADC:
    # Pico-style named channel for the on-die temperature sensor.
    CORE_TEMP = 4

    def __init__(self, pin: Any) -> None:
        self.pin = pin
        self._sim = _SimSource()
        _log(f"ADC({pin!r}) configured")

    def read_u16(self) -> int:
        """Return a 16-bit ADC sample (0..65535).

        Hardware returns a real conversion; the host returns the next value of
        a deterministic simulated source so tests can assert on it.
        """
        sample = self._sim.sample()
        _EVENTS.append(Event("adc", f"ADC({self.pin!r})", "read_u16", sample))
        _log(f"ADC({self.pin!r}) read_u16={sample}")
        return sample
