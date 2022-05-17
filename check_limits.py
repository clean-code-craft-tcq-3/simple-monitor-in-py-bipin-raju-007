from battery_vitals import *


def battery_is_ok(battery_validators):
    for battery_validator in battery_validators:
        value_state = battery_validator.get_value_state()
        if value_state != ValueState.Normal:
            return False, battery_validator, value_state
    return True, None, ValueState.Normal


if __name__ == '__main__':
    result, validator, state = battery_is_ok([BatteryTemperature(40)])
    assert (result is True)
    assert (validator is None)
    assert (state == ValueState.Normal)

    result, validator, state = battery_is_ok([BatteryTemperature(100, Unit.Fahrenheit)])
    assert (result is True)
    assert (validator is None)
    assert (state == ValueState.Normal)

    result, validator, state = battery_is_ok([BatteryTemperature(-1)])
    assert (result is False)
    assert (type(validator) is BatteryTemperature)
    assert (state == ValueState.Low_Breach)

    result, validator, state = battery_is_ok([BatteryTemperature(43)])
    assert (result is False)
    assert (type(validator) is BatteryTemperature)
    assert (state == ValueState.High_Warning)

    result, validator, state = battery_is_ok(
        [BatteryTemperature(25), BatterySOC(70), BatteryChargeRate(0.7)])
    assert (result is True)
    assert (validator is None)
    assert (state == ValueState.Normal)

    result, validator, state = battery_is_ok(
        [BatteryTemperature(50), BatterySOC(85), BatteryChargeRate(0)])
    assert (result is False)
    assert (type(validator) is BatteryTemperature)
    assert (state == ValueState.High_Breach)

    result, validator, state = battery_is_ok(
        [BatteryTemperature(40), BatterySOC(85), BatteryChargeRate(0)])
    assert (result is False)
    assert (type(validator) is BatterySOC)
    assert (state == ValueState.High_Breach)

    result, validator, state = battery_is_ok(
        [BatteryTemperature(40), BatterySOC(45), BatteryChargeRate(0.9)])
    assert (result is False)
    assert (type(validator) is BatteryChargeRate)
    assert (state == ValueState.High_Breach)

    result, validator, state = battery_is_ok(
        [BatteryTemperature(40), BatterySOC(45), BatteryChargeRate(0.22)])
    assert (result is False)
    assert (type(validator) is BatteryChargeRate)
    assert (state == ValueState.Low_Warning)
