from cleo import argument

from .base import TimeCommand


class KSTCommand(TimeCommand):
    name = 'kst'
    description = 'convert KST time to target timezone'
    arguments = [
        argument('time', 'target time to change'),
        argument('tz', 'target timezone to change', default='UTC', optional=True)
    ]

    def handle(self):
        time = self.argument('time')
        tz = self.argument('tz')
        parsed = self.time_parse(time, 'Asia/Seoul', tz)
        self.line("{} in {} is {}".format(time, tz, parsed.strftime('%H:%M')))


class UTCCommand(TimeCommand):
    name = 'utc'
    description = 'convert UTC time to target timezone'
    arguments = [
        argument('time', 'target time to change'),
        argument('tz', 'target timezone to change', default='Asia/Seoul', optional=True)
    ]

    def handle(self):
        time = self.argument('time')
        tz = self.argument('tz')
        parsed = self.time_parse(time, 'UTC', tz)
        self.line("{} in {} is {}".format(time, tz, parsed.strftime('%H:%M')))
