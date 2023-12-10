from datetime import datetime, timedelta
from pytz import utc, timezone


class Time(object):
    tashkent_timezone = timezone('Asia/Tashkent')

    def make_lifetime(self, time):
        expiration_time = datetime.now(self.tashkent_timezone) + timedelta(days=10)
        return expiration_time.timestamp()

    def lifetime_checking(self, expiration_time):
        current_time = datetime.now(self.tashkent_timezone)
        exp_datetime = datetime.utcfromtimestamp(expiration_time).replace(tzinfo=utc).astimezone(self.tashkent_timezone)

        return None if current_time > exp_datetime else True
