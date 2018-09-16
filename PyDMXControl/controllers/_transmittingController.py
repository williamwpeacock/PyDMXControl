"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ._Controller import Controller
from ..utils.timing import Ticker


class transmittingController(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__auto = True
        if 'autostart' in kwargs:
            if type(kwargs['autostart']) is bool:
                self.__auto = kwargs['autostart']

        self.internalTicker = Ticker()
        self.internalTicker.set_interval(0)

        if self.__auto:
            self.run()

    def _send_data(self):
        pass

    def close(self):
        # Stop the threaded loop
        self.internalTicker.stop()
        print("CLOSE: internalTicker stopped")

        # Parent
        super().close()

        return

    def run(self):
        # Create the thread and transmit data
        self.internalTicker.clear_callbacks()
        self.internalTicker.add_callback(self._send_data)
        self.internalTicker.start()
