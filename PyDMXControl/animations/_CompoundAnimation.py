from . import Animation

class CompoundAnimation(Animation):

    def __init__(self, animations, *args, **kwargs):
        length = 0
        for anim in animations:
            length = max(length, anim[1] + (anim[0].length * anim[3]))
            # length = max(length, start_time + anim.length)

        self.animations = animations

        super().__init__(length, *args, **kwargs)

    def start(self, controller, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        for anim in self.animations:
            anim[0].start(controller, start_offset + anim[1], anim[2], anim[3])
        super().start(controller, start_offset, snap, repeat)

    def stop(self):
        for anim in self.animations:
            anim[0].stop()
        super().stop()