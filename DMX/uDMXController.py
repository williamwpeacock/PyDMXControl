from threading import Thread

from DMX.Controller import Controller
from pyudmx import pyudmx


class Controller(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.udmx = pyudmx.uDMXDevice()
        self.udmx.open()

        self.__sending = True
        self.__auto = True
        if 'autostart' in kwargs:
            if type(kwargs['autostart']) is bool:
                self.__auto = kwargs['autostart']

        if self.__auto:
            self.run()

    def __send_data(self):
        # Start loop
        self.__sending = True
        while self.__sending:
            # Transmit frame
            self.udmx.send_multi_value(1, self.frame)

            # Sleep (Minimum transmission break for DMX512)
            self.sleep(0.000001 * 92)

        return

    def close(self, all_zero=False):
        # Stop the threaded loop
        self.__sending = False

        # Send blank frame if wanted
        if all_zero:
            self.udmx.send_multi_value(1, [0 for v in range(0, 512)])

        # Close device
        self.udmx.close()

    def run(self):
        # Create the thread and transmit data
        Thread(target=self.__send_data).start()
        return