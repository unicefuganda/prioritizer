from models.priority import Priority


class FilterProcessor(object):

    def __init__(self, high_filters=None, low_filters=None):
        self.high_filters = high_filters
        self.low_filters = low_filters

    def is_low_priority(self, filter_instance):
        return filter_instance.prioritize() is Priority.LOW

    def is_high_priority(self, filter_instance):
        return filter_instance.prioritize() is Priority.HIGH

    def execute(self):
        for priority_filter in self.low_filters:
            if self.is_low_priority(priority_filter):
                return Priority.LOW

        for priority_filter in self.high_filters:
            if self.is_high_priority(priority_filter):
                return Priority.HIGH

        return Priority.LOW