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

class GUIFixture(tk.Label):
    def __init__(self, window: tk.Tk, fixture: Fixture):
        super().__init__(window, text=fixture)

class GUIController(TransmittingController):

    def _connect(self):
        self.window = tk.Tk()

        self.__gui_fixtures = []

    def add_fixture(self, *args, **kwargs):
        fixture = super().add_fixture(*args, **kwargs)
        new_fixture = GUIFixture(self.window, fixture)
        new_fixture.pack()
        self.__gui_fixtures.append(new_fixture)
        return fixture

    def _transmit(self, frame: List[int], first: int):
        # self.window.update()
        print(first, frame)
