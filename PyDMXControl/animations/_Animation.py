from typing import List

class Animation:

    def __init__(self, fixture: 'Fixture', length: float):
        # The fixture effect is applied to
        self.fixture = fixture

        # length in bars
        self.length = length

        # Animating flag for ticker
        self.__animating = False

    def __callback(self, now: float):
        if self.__animating:
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
        self.__animating = False
        self.fixture.controller.ticker.remove_animation(self)

    def start(self, start_offset: float = 0):
        self.__animating = True
        self.fixture.controller.ticker.add_animation(self, 0, start_offset)
