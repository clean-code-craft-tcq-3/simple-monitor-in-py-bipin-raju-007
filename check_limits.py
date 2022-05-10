import enum

temperature_lower_limit = 0
temperature_upper_limit = 45
charge_state_lower_limit = 20
charge_state_upper_limit = 80
charge_rate_limit = 0.8


class ValueRange(enum.IntEnum):
    Low = -1
    Normal = 0
    High = 1


class BatteryVital:
    upper_limit = 0
    lower_limit = 0

    def __init__(self, value, lower_limit, upper_limit):
        self.value = value
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def get_value_range(self):
        value_range = ValueRange.Normal
        if self.value > self.upper_limit:
            value_range = ValueRange.High
        elif self.value < self.lower_limit:
            value_range = ValueRange.Low
        return value_range


class BatteryTemperature(BatteryVital):
    def __init__(self, value):
        BatteryVital.__init__(self, value, temperature_lower_limit, temperature_upper_limit)


class BatteryChargeState(BatteryVital):
    def __init__(self, value):
        BatteryVital.__init__(self, value, charge_state_lower_limit, charge_state_upper_limit)


class BatteryChargeRate(BatteryVital):
    def __init__(self, value):
        BatteryVital.__init__(self, value, 0, charge_rate_limit)


def battery_is_ok(battery_validators):
    for validator in battery_validators:
        value_range = validator.get_value_range()
        if value_range is not ValueRange.Normal:
            return False, validator, value_range
    return True, None, ValueRange.Normal


if __name__ == '__main__':
    result, validator, value_range = battery_is_ok([BatteryTemperature(40)])
    assert (result is True)
    assert (validator is None)
    assert (value_range == ValueRange.Normal)

    result, validator, value_range = battery_is_ok([BatteryTemperature(-1)])
    assert (result is False)
    assert (type(validator) is BatteryTemperature)
    assert (value_range == ValueRange.Low)

    result, validator, value_range = battery_is_ok([BatteryTemperature(25), BatteryChargeState(70), BatteryChargeRate(0.7)])
    assert(result is True)
    assert(validator is None)
    assert(value_range == ValueRange.Normal)

    result, validator, value_range = battery_is_ok([BatteryTemperature(50), BatteryChargeState(85), BatteryChargeRate(0)])
    assert (result is False)
    assert (type(validator) is BatteryTemperature)
    assert (value_range == ValueRange.High)

    result, validator, value_range = battery_is_ok([BatteryTemperature(40), BatteryChargeState(85), BatteryChargeRate(0)])
    assert (result is False)
    assert (type(validator) is BatteryChargeState)
    assert (value_range == ValueRange.High)

    result, validator, value_range = battery_is_ok([BatteryTemperature(40), BatteryChargeState(45), BatteryChargeRate(0.9)])
    assert (result is False)
    assert (type(validator) is BatteryChargeRate)
    assert (value_range == ValueRange.High)
