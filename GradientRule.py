import Rules
from k_to_rgb import convert_K_to_RGB
import numpy
import datetime


def temperature_and_brightness_to_rgbw_duty_cycle(temp, brightness):
    color_rgb = convert_K_to_RGB(temp)
    return color_and_brightness_to_rgbw_duty_cycle(color_rgb, brightness)


def color_and_brightness_to_rgbw_duty_cycle(color_rgb, brightness):
    # Figure out the minimum RGB value
    min_color = min(color_rgb)

    # Put the minimum RGB value from each of R, G, and B in the white LED
    white_0_255 = min_color

    # Normalize color and white values to be between 0 and 100
    color_0_100 = numpy.divide(color_rgb, 2.55)
    white_0_100 = white_0_255 / 2.55

    # Create rgbw tuple
    rgbw_tuple = tuple(color_0_100) + (white_0_100,)

    # Assign duty cycles to LEDs based on brightness (which is between 0 and 100)
    brightness_adjusted_rgbw = tuple(numpy.multiply(rgbw_tuple, brightness / 100.0))

    # Return tuple of duty cycles
    return brightness_adjusted_rgbw


class GradientRule(Rules.BaseRule):
    def __init__(self, start_datetime, end_datetime, start_temperature, end_temperature,
                 start_brightness, end_brightness):
        """
        Constructor for GradientRule.
        :param start_datetime:
        :param end_datetime:
        :param start_temperature: color temperature in Kelvin
        :param end_temperature: color temperature in Kelvin
        :param start_brightness: a value between 0 (not on) and 100 (max brightness of LED)
        :param end_brightness: a value between 0 (not on) and 100 (max brightness of LED)
        """
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.start_temperature = start_temperature
        self.end_temperature = end_temperature
        self.start_brightness = start_brightness
        self.end_brightness = end_brightness

    def get_last_activation_time(self, cur_datetime):
        return self.start_datetime if self.start_datetime <= cur_datetime else None

    def get_rgbw_at_datetime(self, cur_datetime):
        if cur_datetime < self.start_datetime:
            return None

        if cur_datetime >= self.end_datetime:
            return temperature_and_brightness_to_rgbw_duty_cycle(self.end_temperature, self.end_brightness)

        # for datetimes within the duration of the GradientRule
        duration_proportion = (cur_datetime.timestamp()-self.start_datetime.timestamp())/(self.end_datetime.timestamp()-self.start_datetime.timestamp())
        cur_temperature = self.start_temperature + (self.end_temperature - self.start_temperature)*duration_proportion
        cur_brightness = self.start_brightness + (self.end_brightness - self.start_brightness)*duration_proportion
        return temperature_and_brightness_to_rgbw_duty_cycle(cur_temperature, cur_brightness)

    def get_dict(self):
        return {'type': 'gradient',
                'start_datetime': self.start_datetime.isoformat(),
                'end_datetime': self.end_datetime.isoformat(),
                'start_temperature': self.start_temperature,
                'end_temperature': self.end_temperature,
                'start_brightness': self.start_brightness,
                'end_brightness': self.end_brightness
                }

    @staticmethod
    def get_rule_from_dict(rule_dict):
        start_datetime_str = rule_dict.get('start_datetime')
        end_datetime_str = rule_dict.get('end_datetime')
        start_temperature = rule_dict.get('start_temperature')
        end_temperature = rule_dict.get('end_temperature')
        start_brightness = rule_dict.get('start_brightness')
        end_brightness = rule_dict.get('end_brightness')

        if None in [start_datetime_str, end_datetime_str, start_temperature,
                    end_temperature, start_brightness, end_brightness]:
            return None

        start_datetime = datetime.datetime.fromisoformat(start_datetime_str)
        end_datetime = datetime.datetime.fromisoformat(end_datetime_str)

        return GradientRule(start_datetime, end_datetime, start_temperature,
                             end_temperature, start_brightness, end_brightness)

