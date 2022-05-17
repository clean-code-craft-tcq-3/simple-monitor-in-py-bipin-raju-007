import enum


class Unit(enum.IntEnum):
    Invalid = -1
    Celsius = 0
    Fahrenheit = 1


class ValueState:
    Low_Breach = 0
    Low_Warning = 1
    Normal = 2
    High_Warning = 3
    High_Breach = 4


class ValueRange:
    def __init__(self, low_breach, low_warning, high_warning, high_breach):
        self.low_breach = low_breach
        self.low_warning = low_warning
        self.high_breach = high_breach
        self.high_warning = high_warning
