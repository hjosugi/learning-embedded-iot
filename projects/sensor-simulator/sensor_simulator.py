from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Reading:
    sequence: int
    sensor: str
    celsius: float
    alert: bool


def generate(samples: int) -> list[Reading]:
    readings = []
    for index in range(samples):
        celsius = 24.0 + math.sin(index / 2) * 3.5
        readings.append(
            Reading(
                sequence=index,
                sensor="simulated-temp-01",
                celsius=round(celsius, 2),
                alert=celsius >= 27.0,
            )
        )
    return readings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=10)
    args = parser.parse_args()
    for reading in generate(args.samples):
        print(json.dumps(asdict(reading)))


if __name__ == "__main__":
    main()

