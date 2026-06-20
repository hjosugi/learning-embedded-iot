# Hardware Safety

Last verified: 2026-06-20

## Basic Rules

- Disconnect power before changing wiring.
- Keep microcontroller GPIO at its expected logic voltage.
- Do not connect 5V signals directly to 3.3V-only pins.
- Use current-limiting resistors for LEDs.
- Double-check power and ground before flashing or running code.
- Avoid mains voltage projects in this repo.
- Use known-safe battery modules instead of improvised charging circuits.

## Git Safety

- Do not commit Wi-Fi passwords.
- Do not commit cloud IoT credentials.
- Use `.env.example` for broker URLs, device IDs, and tokens.
- Generated firmware files are ignored.

## Lesson Safety Template

Each hardware lesson should include:

- board name
- voltage
- wiring table
- power source
- flash command
- expected serial output
- cleanup/reset command
