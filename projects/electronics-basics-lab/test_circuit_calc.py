from circuit_calc import (
    adc_count,
    check_gpio_voltage,
    next_e12_resistor,
    plan_led,
    plan_pullup,
    voltage_divider,
)


def assert_close(actual: float, expected: float, tolerance: float = 0.001) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"expected {expected}, got {actual}")


def assert_raises(fn) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def main() -> None:
    assert next_e12_resistor(260) == 270

    led = plan_led(3.3, 2.0, 5.0)
    assert led.chosen_resistor_ohms == 270
    assert_close(led.actual_current_ma, 4.815)
    assert led.gpio_current_ok is True

    bright_led = plan_led(3.3, 2.0, 20.0)
    assert bright_led.gpio_current_ok is False

    assert_close(voltage_divider(5.0, 10000, 20000), 3.333333, tolerance=0.0001)
    assert check_gpio_voltage(voltage_divider(5.0, 10000, 20000)) is False
    assert check_gpio_voltage(voltage_divider(5.0, 20000, 10000)) is True
    assert adc_count(1.65, reference_v=3.3, bits=12) == 2048

    pullup = plan_pullup(3.3, 10000, capacitance_nf=10)
    assert_close(pullup.idle_current_ma, 0.33)
    assert_close(pullup.time_constant_ms, 0.1)
    assert_close(pullup.five_tau_settle_ms, 0.5)

    assert_raises(lambda: plan_led(3.3, 3.3, 5.0))
    assert_raises(lambda: voltage_divider(3.3, 0, 10000))
    assert_raises(lambda: adc_count(5.0, reference_v=3.3))
    print("ok")


if __name__ == "__main__":
    main()
