"""
    Converter classes. Useful for bindings.
"""

# standard libraries
import datetime
import locale
import pathlib
import re
import uuid

# third party libraries
# none

# local libraries
# none


class IntegerToStringConverter:
    """ Convert between int value and formatted string. """

    def __init__(self, format=None, pass_none=False, fuzzy=True):
        """ format specifies int to string conversion """
        self.__format = format if format else "{:d}"
        self.__pass_none = pass_none
        self.__fuzzy = fuzzy

    def convert(self, value):
        """ Convert value to string using format string """
        if self.__pass_none and value is None:
            return None
        return self.__format.format(int(value))

    def convert_back(self, formatted_value):
        """ Convert string to value using standard int conversion """
        formatted_value = re.sub("[^0-9]", "", formatted_value) if self.__fuzzy and formatted_value else None
        if formatted_value:
            return int(formatted_value)
        else:
            return None if self.__pass_none else 0


class FloatToStringConverter:
    """ Convert between float value and formatted string. """

    def __init__(self, format=None, pass_none=False, fuzzy=True):
        self.__format = format if format else "{:g}"
        self.__pass_none = pass_none
        self.__fuzzy = fuzzy

    def convert(self, value):
        """ Convert value to string using format string """
        if self.__pass_none and value is None:
            return None
        return self.__format.format(value)

    def convert_back(self, formatted_value):
        """ Convert string to value using standard float conversion """
        if self.__pass_none and (formatted_value is None or len(formatted_value) == 0):
            return None
        if self.__fuzzy:
            _parser = re.compile(r"""        # A numeric string consists of:
                (?P<sign>[-+])?              # an optional sign, followed by either...
                (
                    (?=\d|[\.,]\d)              # ...a number (with at least one digit)
                    (?P<int>\d*)             # having a (possibly empty) integer part
                    ([\.,](?P<frac>\d*))?       # followed by an optional fractional part
                    (E(?P<exp>[-+]?\d+))?    # followed by an optional exponent, or...
                )
            """, re.VERBOSE | re.IGNORECASE).match
            m = _parser(formatted_value.strip())
            if m is not None:
                decimal_point = locale.localeconv().get("decimal_point", ".")
                if decimal_point != '.':
                    return locale.atof(m.group(0).replace(".", decimal_point))
                return locale.atof(m.group(0))
            return 0.0
        else:
            decimal_point = locale.localeconv().get("decimal_point", ".")
            if decimal_point != '.':
                return locale.atof(formatted_value.replace(".", decimal_point))
            return locale.atof(formatted_value)


class FloatToScaledIntegerConverter:
    """ Convert between float value and int (float * 100). """
    def __init__(self, n: int, value_min: float=0, value_max: float=1):
        self.n = n
        self.value_min = value_min
        self.value_max = value_max

    def convert(self, value):
        """ Convert float between 0, 1 to percentage int """
        return int(self.n * (value - self.value_min) / (self.value_max - self.value_min))

    def convert_back(self, value_int):
        """ Convert int percentage value to float """
        return value_int * (self.value_max - self.value_min) / self.n + self.value_min


class FloatToPercentStringConverter:
    """ Convert between float value and percentage string. """

    def convert(self, value):
        """ Convert float between 0, 1 to percentage string """
        return str(int(value * 100)) + "%"

    def convert_back(self, formatted_value):
        """ Convert percentage string to float between 0, 1 """
        return float(formatted_value.strip('%'))/100.0


class PhysicalValueToStringConverter:
    """ Convert between physical value represented by a float and a formatted string. """

    def __init__(self, units: str, multiplier: float=1.0, format=None, pass_none=False, fuzzy=True):
        self.__units = units
        self.__multiplier = multiplier
        self.__format = format + " {:s}" if format else "{:g} {:s}"
        self.__pass_none = pass_none
        self.__fuzzy = fuzzy

    def convert(self, value):
        """ Convert value to string using format string """
        if self.__pass_none and value is None:
            return None
        return self.__format.format(value * self.__multiplier, self.__units)

    def convert_back(self, formatted_value):
        """ Convert string to value using standard float conversion """
        return FloatToStringConverter().convert_back(formatted_value) / self.__multiplier


class CheckedToCheckStateConverter:
    """ Convert between bool and checked/unchecked strings. """

    def convert(self, value):
        """ Convert bool to checked or unchecked string """
        return "checked" if value else "unchecked"

    def convert_back(self, value):
        """ Convert checked or unchecked string to bool """
        return value == "checked"


class UuidToStringConverter:
    def convert(self, value):
        return str(value) if value else None
    def convert_back(self, value):
        if re.fullmatch("[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}",
                        value.strip(), re.IGNORECASE) is not None:
            return uuid.UUID(value.strip())
        return None


class PathToStringConverter:
    def convert(self, value):
        return str(value) if value else None
    def convert_back(self, value):
        return pathlib.Path(value) if value else None


class DatetimeToStringConverter:
    def convert(self, value):
        return value.isoformat() if value is not None else None
    def convert_back(self, value):
        try:
            if len(value) == 26:
                return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            elif len(value) == 19:
                return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError as e:
            pass  # fall through
        return None
