import random

from . import Animation

class RandomAnimation(Animation):

    def __init__(self, animations, length = None, *args, **kwargs):
        if length == None:
            length = 0
            for anim in animations:
                length = max(length, anim.length)

        self.animations = animations

        super().__init__(length, *args, **kwargs)

    def start(self, parent, setting_func, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        cb = super().start(parent, setting_func, start_offset, snap, repeat)
        self.start_children(cb)

    def start_at(self, parent, setting_func, start_time: float = 0, repeat: int = 1):
        cb = super().start_at(parent, setting_func, start_time, repeat)
        self.start_children(cb)

    def start_children(self, cb):
        anim = random.choice(self.animations)
        anim.start(cb, None, 0, True, 1)
