from abc import ABC, abstractmethod
import datetime


class BaseAlarm(ABC):
    def is_activated(self, cur_datetime):
        return self.get_last_activation_time(cur_datetime) is not None

    @abstractmethod
    def get_last_activation_time(self, cur_datetime):
        pass

    @abstractmethod
    def get_rgbw_at_datetime(self, cur_datetime):
        """

        :param cur_datetime:
        :return: An RGBW tuple representing the color of the alarm at cur_datetime (or None)
        """
        pass

    @staticmethod
    def get_alarm_from_dict(alarm_dict):
        alarm_type = alarm_dict.get('type')
        if alarm_type == 'onetime':
            return OneTimeAlarm.get_alarm_from_dict(alarm_dict)
        else:
            return None

    @abstractmethod
    def get_dict(self):
        pass


class OneTimeAlarm(BaseAlarm):
    def __init__(self, alarm_datetime, rgbw):
        self.alarm_datetime = alarm_datetime
        self.rgbw = rgbw

    def get_last_activation_time(self, cur_datetime):
        return self.alarm_datetime if self.alarm_datetime <= cur_datetime else None

    def get_rgbw_at_datetime(self, cur_datetime):
        if cur_datetime >= self.alarm_datetime:
            return self.rgbw
        else:
            return None

    def get_dict(self):
        return {'type': 'onetime', 'alarm_datetime': self.alarm_datetime.isoformat(), 'rgbw': self.rgbw}

    @staticmethod
    def get_alarm_from_dict(alarm_dict):
        alarm_datetime_str = alarm_dict.get('alarm_datetime')
        if alarm_datetime_str is None:
            return None
        alarm_datetime = datetime.datetime.fromisoformat(alarm_datetime_str)

        rgbw_list = alarm_dict.get('rgbw')  # This will be a list because tuples get json-ified into lists
        if rgbw_list is None:
            return None
        rgbw_tuple = tuple(rgbw_list)

        return OneTimeAlarm(alarm_datetime, rgbw_tuple)
