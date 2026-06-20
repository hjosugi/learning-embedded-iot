# 2026 Learning Items: Embedded IoT

Last verified: 2026-06-20

## Must Learn

### Microcontroller basics

- GPIO
- pull-up and pull-down resistors
- PWM
- ADC
- timers
- interrupts
- serial console
- firmware flashing

Projects:

- `examples/micropython-rp2-blink`
- `examples/pico-c-sdk-blink`

### MicroPython

- REPL workflow
- `boot.py` and `main.py`
- filesystem basics
- board quick references
- sensor reads
- network basics on ESP32

Projects:

- `examples/micropython-esp32-sensor`

### ESP-IDF

- project structure
- target selection
- Wi-Fi setup
- NVS basics
- logging
- FreeRTOS task basics
- MQTT client

Projects:

- `examples/esp-idf-wifi-mqtt`

### Zephyr RTOS

- west workspace
- board selection
- Kconfig
- devicetree
- drivers
- samples
- native simulation where possible

Projects:

- `examples/zephyr-blinky`

### IoT data flow

- MQTT topic design
- JSON vs binary payloads
- device ID strategy
- time stamping
- offline buffering
- ingest into local data stores

Projects:

- `examples/mqtt-to-duckdb`
- companion notes with `learning-data-stores`

## Definition of Done

- Every hardware example has a board name and wiring note.
- Every firmware example says how to build and flash.
- Every sensor example can be run with generated data when hardware is unavailable.
- Every network example documents credentials through `.env.example`.
- Every lesson has a cleanup/reset note.
