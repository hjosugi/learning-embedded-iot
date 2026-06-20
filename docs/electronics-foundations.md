# Electronics Foundations

Last verified: 2026-06-21

## Study Order

1. voltage, current, resistance, and power
2. breadboard rails and common ground
3. current-limiting resistors for LEDs
4. GPIO output current limits
5. pull-up and pull-down inputs
6. switch bounce and debouncing
7. ADC input range and voltage dividers
8. transistor or MOSFET switching for loads
9. I2C/SPI/UART wiring and logic levels
10. power budget, sleep current, and battery limits

## Minimum Bench Kit

- breadboard
- jumper wires
- resistor kit
- LEDs
- tactile buttons
- potentiometer
- multimeter
- Raspberry Pi Pico / Pico 2 or ESP32 development board
- USB power only for beginner lessons

## Circuit Review Checklist

- Is every signal sharing a common ground?
- Is the GPIO voltage within the board's logic level?
- Does every LED have a current-limiting resistor?
- Is the expected current below the GPIO or module limit?
- Is the ADC input below the reference voltage?
- Is the load small enough for a GPIO pin, or does it need a transistor/MOSFET?
- Is the wiring table written before power is connected?

## Repo Rule

Every hardware project should include both:

- firmware or host simulation
- circuit explanation: wiring table, voltage/current assumptions, and safety note
