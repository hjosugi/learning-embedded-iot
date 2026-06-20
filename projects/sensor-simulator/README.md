# Sensor Simulator

A no-hardware embedded/IoT starter project.

It generates deterministic sensor readings and emits JSON lines shaped like device telemetry.

## Run

```bash
python3 projects/sensor-simulator/sensor_simulator.py --samples 5
```

## Unit Test

```bash
python3 projects/sensor-simulator/test_sensor_simulator.py
```

## Exercise

1. Add a second sensor.
2. Change the alert threshold.
3. Write readings to the data-store lab.
4. Replace the simulator with MicroPython on real hardware.
