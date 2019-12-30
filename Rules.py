from abc import ABC, abstractmethod
import datetime


class BaseRule(ABC):
    def is_activated(self, cur_datetime):
        return self.get_last_activation_time(cur_datetime) is not None

    @abstractmethod
    def get_last_activation_time(self, cur_datetime):
        pass

    @abstractmethod
    def get_rgbw_at_datetime(self, cur_datetime):
        """

        :param cur_datetime:
        :return: An RGBW tuple representing the color of the rule at cur_datetime (or None)
        """
        pass

    @staticmethod
    def get_rule_from_dict(rule_dict):
        import GradientRule

        rule_type = rule_dict.get('type')
        if rule_type == 'onetime':
            return OneTimeRule.get_rule_from_dict(rule_dict)
        elif rule_type == 'gradient':
            return GradientRule.GradientRule.get_rule_from_dict(rule_dict)
        else:
            return None

    @abstractmethod
    def get_dict(self):
        pass


class OneTimeRule(BaseRule):
    def __init__(self, rule_datetime, rgbw):
        self.rule_datetime = rule_datetime
        self.rgbw = rgbw

    def get_last_activation_time(self, cur_datetime):
        return self.rule_datetime if self.rule_datetime <= cur_datetime else None

    def get_rgbw_at_datetime(self, cur_datetime):
        if cur_datetime >= self.rule_datetime:
            return self.rgbw
        else:
            return None

    def get_dict(self):
        return {'type': 'onetime', 'rule_datetime': self.rule_datetime.isoformat(), 'rgbw': self.rgbw}

    @staticmethod
    def get_rule_from_dict(rule_dict):
        rule_datetime_str = rule_dict.get('rule_datetime')
        if rule_datetime_str is None:
            return None
        rule_datetime = datetime.datetime.fromisoformat(rule_datetime_str)

        rgbw_list = rule_dict.get('rgbw')  # This will be a list because tuples get json-ified into lists
        if rgbw_list is None:
            return None
        rgbw_tuple = tuple(rgbw_list)

        return OneTimeRule(rule_datetime, rgbw_tuple)
