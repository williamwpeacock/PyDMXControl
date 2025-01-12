"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""
import tkinter as tk

from typing import List

from ._TransmittingController import TransmittingController
from ..profiles.defaults import Fixture

from .. import Colors

class GUIFixture(tk.Label):
    def __init__(self, window: tk.Tk, fixture: Fixture):
        self.fixture = fixture
        super().__init__(window, text=self.fixture)

    def update(self):
        brightness = 1
        if self.fixture.has_channel('d'):
            brightness = self.fixture.get_channel_value('d')[0]/255

        rgb = [int(v * brightness) for v in self.fixture.get_color()]

        self.configure(bg=Colors.to_hex(rgb))

class GUIController(TransmittingController):

    def _connect(self):
        self.window = tk.Tk()
        self.window.attributes('-topmost', True)
        self.__gui_fixtures = []

    def add_fixture(self, *args, **kwargs):
        fixture = super().add_fixture(*args, **kwargs)

        new_fixture = GUIFixture(self.window, fixture)
        new_fixture.pack(fill=tk.BOTH)
        self.__gui_fixtures.append(new_fixture)

        return fixture

    def _transmit(self, frame: List[int], first: int):
        for fixture in self.__gui_fixtures:
            fixture.update()

    def sleep_till_enter(self):
        print("Close Window to end sleep...")
        self.window.mainloop()
