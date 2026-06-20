# Electronics Basics Lab

Microcontroller work starts with the circuit, not the firmware. This lab uses
Python to make the first electronics calculations explicit before wiring a
breadboard.

## Run

```bash
python3 projects/electronics-basics-lab/circuit_calc.py
python3 projects/electronics-basics-lab/test_circuit_calc.py
```

## What It Teaches

- LED current-limiting resistor selection
- GPIO current and resistor power checks
- voltage dividers for sensors
- ADC quantization
- pull-up resistor current and RC settling time
- why 5V signals must not go directly into 3.3V GPIO

## Breadboard Exercises

Start unpowered. Wire once, inspect twice, then power.

### LED

| Part | Connection |
| --- | --- |
| Pico/Pico 2 `GP15` | resistor |
| resistor | LED anode, long leg |
| LED cathode, short leg | `GND` |

Use the calculator before choosing the resistor:

```bash
python3 projects/electronics-basics-lab/circuit_calc.py --led 3.3 2.0 5
```

### Button Input

| Part | Connection |
| --- | --- |
| Pico/Pico 2 `GP14` | button leg 1 |
| button leg 2 | `GND` |

Configure the pin as input with pull-up in firmware. Pressed = low, released = high.

### Analog Sensor / Potentiometer

| Part | Connection |
| --- | --- |
| potentiometer end 1 | `3V3` |
| potentiometer end 2 | `GND` |
| potentiometer wiper | `ADC0` / `GP26` |

Never feed a 5V sensor output directly into an ADC pin. Use a divider or a
level shifter and verify the maximum voltage first.

## Safety Boundary

This repo avoids mains voltage. Keep experiments on USB-powered microcontroller
boards, low-current LEDs, switches, sensors, and known-safe modules.
