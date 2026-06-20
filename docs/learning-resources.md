# Further learning resources

Last verified: 2026-06-21

Curated, canonical primary sources for this repo's named learning tech:
**MicroPython on the RP2040 / Raspberry Pi Pico** (GPIO, PWM, ADC, flashing).
Only official docs, standards bodies, and the chip/board vendors are listed.

## MicroPython language and `machine` API

- **MicroPython documentation** — <https://docs.micropython.org/en/latest/>
  The official docs. The `machine` module reference (`machine.Pin`,
  `machine.PWM`, `machine.ADC`) is exactly the API the host shim re-implements;
  match its method signatures when you extend the shim.

- **MicroPython project site** — <https://micropython.org/>
  Project home, news, and the gateway to the firmware download index. Good entry
  point for what MicroPython is and which ports exist.

- **MicroPython firmware downloads** — <https://micropython.org/download/>
  Official per-board `.uf2` firmware images. This is where you get the Raspberry
  Pi Pico / Pico 2 build to flash before copying `main.py`.

- **RP2 (Raspberry Pi Pico) port quick reference** —
  <https://docs.micropython.org/en/latest/rp2/quickref.html>
  Board-specific pin names, the onboard `"LED"` pin, ADC channels, and `machine`
  examples for exactly this hardware family.

## Raspberry Pi Pico hardware and tooling

- **Raspberry Pi microcontroller documentation** —
  <https://www.raspberrypi.com/documentation/microcontrollers/>
  Official Pico / Pico 2 docs: getting started, the BOOTSEL flashing workflow,
  MicroPython vs. C SDK, datasheets, and pinouts (wiring reference).

- **`mpremote` tool documentation** —
  <https://docs.micropython.org/en/latest/reference/mpremote.html>
  The official command-line tool for copying files to and resetting a board
  (`mpremote fs cp`, `mpremote reset`, `mpremote repl`) used in the upgrade path.

- **Thonny IDE** — <https://thonny.org/>
  Beginner-friendly IDE with first-class MicroPython device support; the GUI
  alternative to `mpremote` for saving `main.py` to the board and using the REPL.

## Deeper reading

- **"Get Started with MicroPython on Raspberry Pi Pico" (Raspberry Pi Press)** —
  <https://www.raspberrypi.com/products/raspberry-pi-pico/>
  The official Pico product page links the canonical getting-started book and
  resources covering GPIO, PWM, ADC, and sensors on this exact board.

- **RP2040 / RP2350 datasheets** —
  <https://www.raspberrypi.com/documentation/microcontrollers/>
  Authoritative electrical detail behind the APIs: ADC reference voltage and the
  on-die temperature-sensor conversion formula used in `u16_to_celsius`.
