# Board Selection

Last verified: 2026-06-20

## Starter Boards

| Board family | Good for | Notes |
| --- | --- | --- |
| Raspberry Pi Pico / Pico 2 | GPIO, MicroPython, C SDK, low-cost basics | Good first microcontroller path |
| ESP32 dev boards | Wi-Fi, Bluetooth, MQTT, IoT sensors | Use ESP-IDF for serious examples |
| Arduino-compatible boards | quick sensor sketches and beginner wiring | Good for fast experiments, less ideal for deeper RTOS learning |
| Zephyr-supported boards | RTOS, portability, devicetree/Kconfig | Pick boards from official supported list |

## Buying Rule

Prefer boards with:

- official docs
- USB serial built in
- many examples
- low replacement cost
- 3.3V logic clearly documented
- easy reset/boot buttons

## Avoid at First

- rare boards with weak docs
- boards that need special programmers before the basics are learned
- high-voltage projects
- lithium battery charging circuits without a known-safe module
