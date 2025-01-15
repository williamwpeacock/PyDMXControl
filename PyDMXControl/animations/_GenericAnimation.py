from . import Animation

from .. import Colors

def example_func(t0, y0, t1, y1, t_now, *args, **kwargs):
    pass

# points_dict {
#     color: {
#         "points": [(0, Colors.Black), (1, Colors.Red)],
#         "funcs": [example_func, example_func]
#     }
# }

class GenericAnimation(Animation):

    def __init__(self, setting_func, points, funcs, *args, **kwargs):
        assert len(points) == len(funcs) + 1
        assert points[0][0] == 0
        # assert points in correct order

        self.setting_func = setting_func
        self.points = points
        self.funcs = funcs
        super().__init__(points[-1][0], *args, **kwargs)

    def callback(self, now: float):
        t_now = self.local_pos(now)

        for i in range(1, len(self.points)):
            if now <= self.points[i][0]:
                val_now = self.funcs[i-1](self.points[i-1], self.points[i], t_now)

                self.setting_func(val_now)
                return

    def stop(self):
        self.setting_func(self.points[-1][1])
        super().stop()

