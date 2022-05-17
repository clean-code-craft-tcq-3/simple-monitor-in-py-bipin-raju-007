from common_types import *


class BatteryVital:
    def get_value_state(self, value, value_ranges: ValueRange):
        value_state = ValueState.Normal
        if value_ranges.low_breach > value:
            value_state = ValueState.Low_Breach
        elif value_ranges.low_breach < value <= value_ranges.low_warning:
            value_state = ValueState.Low_Warning
        elif value_ranges.high_warning < value <= value_ranges.high_breach:
            value_state = ValueState.High_Warning
        elif value_ranges.high_breach < value:
            value_state = ValueState.High_Breach
        return value_state


class BatteryTemperature(BatteryVital):
    temp_low_breach = 0
    temp_low_warning = 2.25
    temp_high_warning = 42.75
    temp_high_breach = 45

    def __init__(self, value, unit_type: Unit = Unit.Celsius):
        self.value = value
        self.unit_type = unit_type
        self.temp_range = ValueRange(self.temp_low_breach, self.temp_low_warning,
                                     self.temp_high_warning, self.temp_high_breach)

    def temperature_in_celsius(self):
        if self.unit_type == Unit.Fahrenheit:
            return (self.value - 32) / 1.8
        else:
            return self.value

    def get_value_state(self):
        return BatteryVital.get_value_state(self, self.temperature_in_celsius(), self.temp_range)


class BatterySOC(BatteryVital):
    soc_low_breach = 20
    soc_low_warning = 24
    soc_high_warning = 76
    soc_high_breach = 80

    def __init__(self, value):
        self.value = value
        self.soc_range = ValueRange(self.soc_low_breach, self.soc_low_warning,
                                    self.soc_high_warning, self.soc_high_breach)

    def get_value_state(self):
        return BatteryVital.get_value_state(self, self.value, self.soc_range)


class BatteryChargeRate(BatteryVital):
    charge_rate_low_breach = 0.20
    charge_rate_low_warning = 0.24
    charge_rate_high_warning = 0.76
    charge_rate_high_breach = 0.8

    def __init__(self, value):
        self.value = value
        self.charge_rate_change = ValueRange(self.charge_rate_low_breach, self.charge_rate_low_warning,
                                             self.charge_rate_high_warning, self.charge_rate_high_breach)

    def get_value_state(self):
        return BatteryVital.get_value_state(self, self.value, self.charge_rate_change)