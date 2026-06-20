from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


E12_VALUES = (10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82)


@dataclass(frozen=True)
class LedPlan:
    supply_v: float
    forward_v: float
    target_current_ma: float
    ideal_resistor_ohms: float
    chosen_resistor_ohms: int
    actual_current_ma: float
    resistor_power_w: float
    gpio_current_ok: bool


@dataclass(frozen=True)
class PullupPlan:
    supply_v: float
    pullup_ohms: int
    capacitance_nf: float
    idle_current_ma: float
    time_constant_ms: float
    five_tau_settle_ms: float


def next_e12_resistor(ohms: float) -> int:
    if ohms <= 0:
        raise ValueError("resistance must be positive")

    decade = 1
    while E12_VALUES[-1] * decade < ohms:
        decade *= 10

    for value in E12_VALUES:
        candidate = value * decade
        if candidate >= ohms:
            return candidate

    return E12_VALUES[0] * decade * 10


def plan_led(
    supply_v: float,
    forward_v: float,
    target_current_ma: float,
    *,
    gpio_current_limit_ma: float = 8.0,
) -> LedPlan:
    if supply_v <= forward_v:
        raise ValueError("supply voltage must be higher than LED forward voltage")
    if target_current_ma <= 0:
        raise ValueError("target current must be positive")

    current_a = target_current_ma / 1000
    ideal = (supply_v - forward_v) / current_a
    chosen = next_e12_resistor(ideal)
    actual_current_a = (supply_v - forward_v) / chosen
    return LedPlan(
        supply_v=supply_v,
        forward_v=forward_v,
        target_current_ma=target_current_ma,
        ideal_resistor_ohms=round(ideal, 2),
        chosen_resistor_ohms=chosen,
        actual_current_ma=round(actual_current_a * 1000, 3),
        resistor_power_w=round(actual_current_a * actual_current_a * chosen, 4),
        gpio_current_ok=actual_current_a * 1000 <= gpio_current_limit_ma,
    )


def voltage_divider(input_v: float, top_ohms: float, bottom_ohms: float) -> float:
    if input_v < 0:
        raise ValueError("input voltage must not be negative")
    if top_ohms <= 0 or bottom_ohms <= 0:
        raise ValueError("divider resistors must be positive")
    return input_v * bottom_ohms / (top_ohms + bottom_ohms)


def adc_count(input_v: float, reference_v: float = 3.3, bits: int = 12) -> int:
    if reference_v <= 0:
        raise ValueError("reference voltage must be positive")
    if input_v < 0 or input_v > reference_v:
        raise ValueError("input voltage must be between 0V and the ADC reference")
    max_count = (1 << bits) - 1
    return round(input_v / reference_v * max_count)


def plan_pullup(supply_v: float, pullup_ohms: int, capacitance_nf: float = 10.0) -> PullupPlan:
    if supply_v <= 0:
        raise ValueError("supply voltage must be positive")
    if pullup_ohms <= 0:
        raise ValueError("pull-up resistance must be positive")
    if capacitance_nf < 0:
        raise ValueError("capacitance must not be negative")

    idle_current_ma = supply_v / pullup_ohms * 1000
    tau_s = pullup_ohms * capacitance_nf * 1e-9
    return PullupPlan(
        supply_v=supply_v,
        pullup_ohms=pullup_ohms,
        capacitance_nf=capacitance_nf,
        idle_current_ma=round(idle_current_ma, 4),
        time_constant_ms=round(tau_s * 1000, 4),
        five_tau_settle_ms=round(tau_s * 5000, 4),
    )


def check_gpio_voltage(signal_v: float, gpio_max_v: float = 3.3) -> bool:
    if signal_v < 0:
        raise ValueError("signal voltage must not be negative")
    return signal_v <= gpio_max_v


def demo() -> dict[str, object]:
    divided = voltage_divider(5.0, top_ohms=20000, bottom_ohms=10000)
    return {
        "led": asdict(plan_led(3.3, 2.0, 5.0)),
        "divider_5v_to_adc": {
            "output_v": round(divided, 3),
            "gpio_safe": check_gpio_voltage(divided),
            "adc_count_12bit": adc_count(divided),
        },
        "button_pullup": asdict(plan_pullup(3.3, 10000)),
        "raw_5v_gpio_safe": check_gpio_voltage(5.0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--led", nargs=3, type=float, metavar=("SUPPLY_V", "FORWARD_V", "CURRENT_MA"))
    args = parser.parse_args()

    if args.led:
        print(json.dumps(asdict(plan_led(*args.led)), indent=2))
        return

    print(json.dumps(demo(), indent=2))


if __name__ == "__main__":
    main()
