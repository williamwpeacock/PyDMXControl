from typing import List

from .. import Colors

class Animation:

    def __init__(self, length: float):
        # length in bars
        self.length = length

    def __callback(self, now: float):
        self.callback(now)

    def callback(self, now: float):
        pass

    def pause(self) -> bool:
        self.__animating = not self.__animating
        return self.__animating

    def local_pos(self, absolute_pos: float) -> float:
        return (absolute_pos % self.length)

    def local_progress(self, absolute_pos: float) -> float:
        return (self.local_pos(absolute_pos) / self.length)

    def stop(self):
        pass

    def start(self, parent, setting_func, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        return parent.add_animation(self, setting_func, start_offset, snap, repeat)

    def start_at(self, parent, setting_func, start_time, repeat):
        return parent.add_animation_at(self, setting_func, start_time, repeat)

    @staticmethod
    def linear_color_mix(xy0, xy1, x_):
        return Colors.mix(xy1[1], xy0[1], (x_ - xy0[0]) / (xy1[0] - xy0[0]))
