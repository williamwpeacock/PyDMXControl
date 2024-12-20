from math import ceil, floor

from ...utils.exceptions import MissingArgumentException, InvalidArgumentException

from ... import Colors
from . import Animation

class MyChase(Animation):

    def __init__(self, *args, **kwargs):
        if 'colors' not in kwargs:
            raise MissingArgumentException('colors', True)
        self.__colors = kwargs['colors'].copy()
        del kwargs['colors']

        self.__num_colors = len(self.__colors)
        if self.__num_colors < 2:
            raise InvalidArgumentException('callback', 'Must contain two or more colors', True)

        self.__snap = False
        if 'snap' in kwargs and isinstance(kwargs['snap'], bool):
            self.__snap = kwargs['snap']
        if 'snap' in kwargs:
            del kwargs['snap']

        super().__init__(*args, **kwargs)

    def callback(self, now: float):
        # Convert to color index
        progress_index = self.local_progress(now) * self.__num_colors
        next_i = ceil(progress_index) - 1
        previous_i = floor(progress_index) - 1
        percent = 1 - (progress_index - 1 - previous_i)

        # Hit 0% & 100%
        if percent >= 0.99:
            percent = 1
        if percent <= 0.01:
            percent = 0

        # Snapping
        if self.__snap:
            if percent <= 0.5:
                percent = 0
            else:
                percent = 1

        # Generate color
        color = Colors.mix(self.__colors[previous_i], self.__colors[next_i], percent)

        # Apply color
        self.fixture.color(color, 0)