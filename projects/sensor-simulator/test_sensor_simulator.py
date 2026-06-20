from sensor_simulator import generate


def test_generate_count_and_alerts() -> None:
    readings = generate(5)
    assert len(readings) == 5
    assert readings[0].sequence == 0
    assert readings[0].alert is False
    assert readings[-1].alert is True


if __name__ == "__main__":
    test_generate_count_and_alerts()
    print("ok")

