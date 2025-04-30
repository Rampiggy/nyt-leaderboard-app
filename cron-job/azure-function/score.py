import datetime


class Score:
    def __init__(
        self,
        username: str,
        completion_date: datetime.date,
        time_in_seconds: int,
    ):
        self.username = username
        self.completion_date = completion_date
        self.time_in_seconds = time_in_seconds
