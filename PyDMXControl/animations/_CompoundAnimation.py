from . import Animation

class CompoundAnimation(Animation):

    def __init__(self, animations, *args, **kwargs):
        length = 0
        for anim in animations:
            length = max(length, anim[1] + (anim[0].length * anim[3]))
            # length = max(length, start_time + anim.length)

        self.animations = animations

        super().__init__(length, *args, **kwargs)

    def start(self, controller, setting_func, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        for anim in self.animations:
            anim[0].start(controller, anim[1], start_offset + anim[2], anim[3], anim[4])
        super().start(controller, setting_func, start_offset, snap, repeat)

    def start_at(self, controller, setting_func, start_time: float = 0, repeat: int = 1):
        for anim in self.animations:
            anim[0].start_at(controller, anim[1], start_time + anim[2], anim[4])
        super().start_at(controller, setting_func, start_time, repeat)

    def stop(self):
        for anim in self.animations:
            anim[0].stop()
        return None