from . import Animation

from .. import Colors

class GenericAnimation(Animation):

    def __init__(self, points, funcs = None, *args, **kwargs):
        if funcs == None:
            func = Animation.linear_color_mix
            if isinstance(points[0][1], int):
                func = Animation.linear_mix
            funcs = [func for _ in range(len(points)-1)]

        assert len(points) == len(funcs) + 1
        assert points[0][0] == 0
        # assert points in correct order

        self.points = points
        self.funcs = funcs
        super().__init__(points[-1][0], *args, **kwargs)

    def callback(self, now: float):
        t_now = self.local_pos(now)

        for i in range(1, len(self.points)):
            if now <= self.points[i][0]:
                val_now = self.funcs[i-1](self.points[i-1], self.points[i], t_now)

                return val_now
            
        return self.points[-1][1]

    def stop(self):
        return self.points[-1][1]

