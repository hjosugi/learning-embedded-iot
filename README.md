# Learning Embedded IoT

Microcontroller, embedded systems, sensors, firmware, and IoT communication experiments.

Last verified: 2026-06-21

## Development Environment

If MicroPython is missing locally, enter the Nix shell:

```bash
nix develop
```

## Runnable Starter Project

Start without hardware by running deterministic sensor telemetry:

```bash
python3 projects/sensor-simulator/sensor_simulator.py --samples 5
python3 projects/sensor-simulator/test_sensor_simulator.py
```

## Target Hands-On Projects

Electronics basics before wiring hardware:

```bash
python3 projects/electronics-basics-lab/circuit_calc.py
python3 projects/electronics-basics-lab/test_circuit_calc.py
```

MicroPython RP2 blink (runs on the host via a `machine` shim; same `main.py`
later flashes to a Pico):

```bash
python3 projects/micropython-rp2-blink/main.py
python3 -m unittest discover -s projects/micropython-rp2-blink -p 'test_*.py'
```

Then copy `projects/micropython-rp2-blink/main.py` to a Pico/Pico 2 as `main.py`
(do not copy `machine.py`). See that project's README for the full flash flow.

## Why This Repo Exists

This repo is for the hardware-adjacent layer:

- microcontroller basics
- electronics basics: voltage, current, resistors, LEDs, buttons, ADC, level shifting
- firmware build and flash flows
- GPIO, I2C, SPI, UART, PWM, ADC
- sensors and small displays
- low-power design
- embedded networking
- MQTT and IoT data ingestion
- safety notes for wiring and power

## What This Repo Teaches

This repo connects software habits to physical constraints.

Each example should make these constraints explicit:

- board and firmware toolchain
- flash/debug workflow
- pin wiring and voltage assumptions
- sensor protocol
- power and sleep behavior
- how secrets are configured on a device
- how to simulate or read the lesson without hardware

## Learning Path

1. Microcontroller mental model
2. Electronics foundations: Ohm's law, LEDs, buttons, voltage dividers, ADC
3. MicroPython on RP2/ESP32
4. Raspberry Pi Pico / Pico 2 basics
5. ESP-IDF basics for ESP32
6. Arduino-style quick experiments
7. Zephyr RTOS basics
8. Sensors and buses: I2C, SPI, UART
9. MQTT to local data stores
10. Power, sleep, watchdogs, and firmware update notes

## Planned Structure

```text
examples/
  micropython-rp2-blink/
  micropython-esp32-sensor/
  pico-c-sdk-blink/
  esp-idf-wifi-mqtt/
  zephyr-blinky/
  sensor-i2c-playground/
  mqtt-to-duckdb/
docs/
  2026-learning-items.md
  board-selection.md
  electronics-foundations.md
  hardware-safety.md
  repository-profile.md
```

## Hardware Strategy

Start with boards that are common, cheap, and well documented:

- Raspberry Pi Pico / Pico 2
- ESP32 development boards
- Arduino-compatible boards where examples are useful

Keep a simulator/no-hardware path when possible:

- MicroPython UNIX port for language basics
- Zephyr native simulation for RTOS basics
- generated sensor data for database and MQTT lessons

## Study Loop

1. read the safety note before wiring anything
2. calculate the circuit before connecting power
3. run the simulator or generated-data path when available
4. flash the smallest blink example before adding network code
5. add one sensor and log raw readings
6. send readings to a local broker or data-store example
7. document board, firmware version, wiring, and failure notes

## What Belongs Elsewhere

- storage comparison belongs in `learning-data-stores`
- MQTT broker operations belong in `learning-platform-engineering`
- protocol design beyond IoT usage belongs in `learning-platform-engineering`
- language-only MicroPython setup notes can be mirrored in `learning-build-systems`

## First Milestones

1. Add MicroPython blink for RP2/Pico.
2. Add ESP32 sensor reading with a generated-data fallback.
3. Add ESP-IDF Wi-Fi/MQTT example with no committed secrets.
4. Add Zephyr blinky and board-selection notes.
5. Add MQTT-to-DuckDB or MQTT-to-InfluxDB handoff notes.

## References

- Zephyr documentation: https://docs.zephyrproject.org/latest/
- ESP-IDF Programming Guide: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/
- MicroPython documentation: https://docs.micropython.org/en/latest/
- Raspberry Pi microcontroller documentation: https://www.raspberrypi.com/documentation/microcontrollers/
