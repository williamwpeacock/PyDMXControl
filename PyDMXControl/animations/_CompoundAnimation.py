from . import Animation

class CompoundAnimation(Animation):

    def __init__(self, animations, length = None, *args, **kwargs):
        if length == None:
            length = 0
            for anim in animations:
                length = max(length, anim[2] + (anim[0].length * anim[4]))

        self.animations = animations

        super().__init__(length, *args, **kwargs)

    def start(self, parent, setting_func, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        cb = super().start(parent, setting_func, start_offset, snap, repeat)
        self.start_children(cb)

    def start_at(self, parent, setting_func, start_time: float = 0, repeat: int = 1):
        cb = super().start_at(parent, setting_func, start_time, repeat)
        self.start_children(cb)

    def start_children(self, cb):
        for anim in self.animations:
            if len(anim) == 4:
                anim[0].start_at(cb, anim[1], anim[2], anim[3])
            elif len(anim) == 5:
                anim[0].start(cb, anim[1], anim[2], anim[3], anim[4])

    def stop(self):
        for anim in self.animations:
            anim[0].stop()
        return None