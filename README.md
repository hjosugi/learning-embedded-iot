# Learning Embedded IoT

Microcontroller, embedded systems, sensors, firmware, and IoT communication experiments.

Last verified: 2026-06-20

## Why This Repo Exists

This repo is for the hardware-adjacent layer:

- microcontroller basics
- firmware build and flash flows
- GPIO, I2C, SPI, UART, PWM, ADC
- sensors and small displays
- low-power design
- embedded networking
- MQTT and IoT data ingestion
- safety notes for wiring and power

## Learning Path

1. Microcontroller mental model
2. MicroPython on RP2/ESP32
3. Raspberry Pi Pico / Pico 2 basics
4. ESP-IDF basics for ESP32
5. Arduino-style quick experiments
6. Zephyr RTOS basics
7. Sensors and buses: I2C, SPI, UART
8. MQTT to local data stores
9. Power, sleep, watchdogs, and firmware update notes

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

## References

- Zephyr documentation: https://docs.zephyrproject.org/latest/
- ESP-IDF Programming Guide: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/
- MicroPython documentation: https://docs.micropython.org/en/latest/
- Raspberry Pi microcontroller documentation: https://www.raspberrypi.com/documentation/microcontrollers/
