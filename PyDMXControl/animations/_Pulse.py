from . import Animation

from .. import Colors

class Pulse(Animation):

    def __init__(self, fixture, color, mid_time, end_time, start_transform = Colors.mix, end_transform = Colors.mix, *args, **kwargs):
        # Pulse(color=Colors.Red, fixtures=[1], mid_time, end_time, start_transform, end_transform)
        assert mid_time < end_time
        self.color = color
        self.mid_time = mid_time
        self.end_time = end_time
        self.start_transform = start_transform
        self.end_transform = end_transform

        super().__init__(fixture, end_time, *args, **kwargs)

    def callback(self, now: float):
        now = self.local_pos(now)
        if now <= self.mid_time:
            new_color = self.start_transform(self.color, Colors.Black, now / self.mid_time)
        elif now > self.mid_time:
            progress = (now - self.mid_time) / (self.end_time - self.mid_time)
            new_color = self.end_transform(self.color, Colors.Black, 1-progress)

        self.fixture.color(new_color)

    def stop(self):
        self.fixture.color(Colors.Black)
        super().stop()

