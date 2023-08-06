from enum import Enum

class ScheduleMethod(Enum):
    EARLIEST_DUE_DATE = 1,
    PRIORITY = 2,
    CRITICAL_RATIO = 3,
    SLACK_PER_REMAINING_OPERATIONS = 4,
    SHORTEST_PROCESSING_TIME = 5,
    FIRST_COME_FIRST_SERVED = 6,
    DEFINED_SEQUENCE = 7

class ActivityStatus(Enum):
    ToDo = 1,
    InProgress = 2,
    Completed = 3,
    Blocked = 4,
    Available = 5,
    Unknown = 6

    @classmethod
    def by_str(cls, str_name):
        ret = next((item for item in cls if str(item.name) == str_name), None)

        if ret is None:
            ret = next((item for item in cls if str(item) == str_name), None)
        return ret