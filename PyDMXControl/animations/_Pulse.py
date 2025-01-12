from ..PyDMXControl.effects.Custom import Animation

from ..PyDMXControl import Colors

class Pulse(Animation):

    def __init__(self, color, fixtures, mid_time, end_time, start_transform = Colors.mix, end_transform = Colors.mix, *args, **kwargs):
        # Pulse(color=Colors.Red, fixtures=[1], mid_time, end_time, start_transform, end_transform)
        self.color = color
        self.fixtures = fixtures
        self.mid_time = mid_time
        self.end_time = end_time
        self.start_transform = start_transform
        self.end_transform = end_transform
        
        super().__init__(*args, **kwargs)

    def callback(self, now: float):
        if now < self.mid_time:
            self.start_transform(Colors.Black, self.color, now / self.mid_time)
        elif now > self.mid_time:
            self.end_transform(self.color, Colors.Black, now / (self.end_time - self.mid_time))
        else:
            self.fixtures.color(self.color)
            
