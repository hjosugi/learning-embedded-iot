# MicroPython RP2 Blink

MicroPython hands-on for the **Raspberry Pi Pico / Pico 2** (RP2040 / RP2350).

Write MicroPython-style code that runs on plain CPython **today** through a small
host shim, then flashes **unchanged** to a real Pico later. One `main.py`
exercises the three classic microcontroller primitives:

1. **GPIO blink** - drive an LED on/off with `machine.Pin`.
2. **PWM "breathing" fade** - ramp brightness with `machine.PWM` + `duty_u16`.
3. **ADC read** - sample an analog input (potentiometer / temperature) with
   `machine.ADC` + `read_u16`.

Standard library only. No pip install, no network access.

## Files

| File | Role |
| --- | --- |
| `main.py` | MicroPython program. Imports `machine`. Flashes to the Pico unchanged. |
| `machine.py` | **Host-only shim.** Re-implements the slice of MicroPython's `machine` API used here so `main.py` runs on CPython. **NOT copied to the board.** |
| `test_main.py` | `unittest` suite that imports `main` via the shim and asserts toggles / duty writes / ADC reads happened. |

The board's firmware already provides a real, C-backed `machine` module, so the
shim exists purely to let you iterate and test on a laptop. The host run uses a
**bounded** number of loop iterations so it terminates for tests/CI; on real
hardware you would use `while True` (see the comments in `main.py` and the
Upgrade path below).

## Run

```bash
python3 projects/micropython-rp2-blink/main.py
```

You will see the shim log each GPIO write, PWM duty value, and ADC sample, then
a final `summary: {...}`.

## Test

Non-interactive, exits non-zero on failure:

```bash
python3 -m unittest discover -s projects/micropython-rp2-blink -p 'test_*.py'
```

## Board and wiring

- **Board:** Raspberry Pi Pico or Pico 2 (RP2040 / RP2350), 3.3V logic.
- **Onboard LED:** the Pico exposes its built-in LED as the named pin `"LED"`,
  so blink/breathe work with **no wiring at all**.
- **External LED (optional):** GPIO15 -> **330 ohm resistor** -> LED anode (long
  leg) -> LED cathode -> GND. Change `LED_PIN = "LED"` to `LED_PIN = 15` in
  `main.py`. Never drive an LED without a current-limiting resistor.
- **Potentiometer (optional):** outer legs to 3V3 and GND, wiper to **GPIO26
  (ADC0)**. `ADC_PIN = 26` reads it. `machine.ADC(4)` reads the on-die
  temperature sensor instead (no wiring).

See `../../docs/hardware-safety.md` before wiring anything.

## Upgrade path

This host shim is the foundation. To run on **real MicroPython hardware**:

1. **Install MicroPython firmware on the Pico.**
   - Download the official `.uf2` for your board from
     <https://micropython.org/download/> (pick *Raspberry Pi Pico* or
     *Pico 2*).
   - Hold **BOOTSEL**, plug the board into USB. It mounts as a USB drive named
     `RPI-RP2`.
   - Copy the `.uf2` onto that drive. The board reboots running MicroPython.

2. **Copy `main.py` to the board with `mpremote`** (the official tool), or use
   Thonny's "Save as -> MicroPython device":

   ```bash
   # one-time, on a machine WITH network/pip (outside this no-install lab):
   #   pip install mpremote
   mpremote connect auto fs cp \
     projects/micropython-rp2-blink/main.py \
     :main.py
   mpremote connect auto reset
   ```

   The board auto-runs `main.py` on boot. Open the REPL with
   `mpremote connect auto repl` to watch output.

3. **Do NOT copy `machine.py`.** The firmware supplies the real `machine`
   module; copying the shim would shadow it and break hardware access. Only
   `main.py` goes to the board.

4. **Make it run forever.** On hardware, replace the bounded host call at the
   bottom of `main.py` with a `while True:` loop (the file documents exactly
   where), so the LED blinks/breathes continuously.

## Cleanup / reset

- **Host:** delete the generated `__pycache__/` directory if you want a clean
  tree: `rm -rf projects/micropython-rp2-blink/__pycache__`.
- **Board (soft):** `mpremote connect auto reset`, or Ctrl-D in the REPL.
- **Board (remove your program):** `mpremote connect auto fs rm :main.py` so the
  board boots to a bare REPL again.
- **Board (full wipe):** re-flash the MicroPython `.uf2` (or the official
  `flash_nuke.uf2`) via BOOTSEL to clear the filesystem.

## Exercises

1. **External LED + button.** Move blink to GPIO15 with a 330 ohm resistor, add
   a `Pin(14, Pin.IN, Pin.PULL_UP)` button, and only blink while it is pressed.
   Extend the shim so a test can inject button presses.
2. **Map the pot to blink speed.** Use the ADC reading to set the blink delay
   (e.g. `delay = adc.read_u16() / 65535`). Add a test asserting a higher
   reading yields a faster blink.
3. **Real temperature.** Switch `ADC_PIN` to channel 4 (on-die sensor), call
   `u16_to_celsius`, and print readings as JSON lines like the
   `sensor-simulator` project so they can feed the data-store lab.
4. **Timer-driven blink.** Re-implement blink with `machine.Timer` instead of
   `sleep`, and add `Timer` to the shim. This is closer to how real firmware
   avoids blocking.
5. **Flash it.** Follow the Upgrade path, flash to a Pico, and record the board,
   firmware version, wiring, and expected serial output in a notes file.

Last verified: 2026-06-21
