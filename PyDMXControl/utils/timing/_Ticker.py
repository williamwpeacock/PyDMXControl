"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from inspect import getframeinfo, stack
from threading import Thread
from time import sleep, time
from typing import Callable
from warnings import warn

from ..exceptions import InvalidArgumentException
from ... import DEFAULT_INTERVAL

from ...effects.defaults import Effect
from ...animations import Animation

class Callback:

    def __init__(self, callback, interval, last, source):
        if not callable(callback):
            raise InvalidArgumentException('callback', 'Not callable')

        self.callback = callback
        self.interval = interval
        self.last = last
        self.source = source

class AnimationCallback:

    def __init__(self, animation, start, end, repeat, source):
        self.animation = animation
        self.start = start
        self.end = end
        self.repeat = repeat
        self.source = source


class Ticker:

    @staticmethod
    def millis_now() -> float:
        return time() * 1000.0

    def bars_now(self) -> float:
        return self.millis_to_bars(self.millis_now())

    def relative_bars_to_millis(self, bars: float) -> float:
        return self.bars_to_millis(bars) + self.__start_millis

    def bars_to_millis(self, bars: float) -> float:
        return ((bars * 4 * 60 * 1000) / self.__bpm)

    def relative_millis_to_bars(self, millis: float) -> float:
        return self.millis_to_bars(millis - self.__start_millis)

    def millis_to_bars(self, millis: float) -> float:
        return ((millis * self.__bpm) / (60 * 1000 * 4))

    def __init__(self, controller, interval_millis: float = DEFAULT_INTERVAL * 1000.0, warn_on_behind: bool = True, bpm: float = 175):
        self.__controller = controller
        self.__callbacks = []
        self.__animations = []
        self.__paused = False
        self.__ticking = False
        self.__interval = interval_millis
        self.__warn_on_behind = warn_on_behind

        self.__bpm = bpm
        self.__start_millis = self.millis_now()

    def __ticker(self):
        # Loop over each callback
        for callback in self.__callbacks:
            # New
            if callback.last is None:
                callback.last = self.millis_now()

            # If diff in milliseconds is interval, run
            if self.millis_now() - callback.last >= callback.interval:
                callback.callback()
                # CHANGED TO REFLECT TIME WHEN SHOULD HAVE FIRED INSTEAD OF TIME WHEN ACTUALLY FIRED
                callback.last = callback.last + callback.interval

        for animation in self.__animations:
            if animation.start < self.millis_now() and self.millis_now() < animation.end:
                animation.animation.callback(self.bars_now() - self.millis_to_bars(animation.start))
            elif self.millis_now() >= animation.end:
                if animation.repeat == 1:
                    animation.animation.stop()
                else:
                    if animation.repeat > 1:
                        animation.repeat -= 1

                    length = self.bars_to_millis(animation.animation.length)
                    animation.start += length
                    animation.end += length

        self.__controller.flush()

    def __ticker__loop(self):
        # Reset
        for callback in self.__callbacks:
            callback.last = None
        self.__paused = False

        # Use a variable so loop can be stopped
        self.__ticking = True
        while self.__ticking:
            # Track start time
            loop_start = self.millis_now()

            # Call ticker
            if not self.__paused:
                self.__ticker()

            # Get end time and duration
            loop_end = self.millis_now()
            loop_dur = loop_end - loop_start
            wait_dur = self.__interval - loop_dur

            # Handle negative wait
            if wait_dur < 0:
                if self.__warn_on_behind:
                    warn("Ticker loop behind by {:,}ms, took {:,}ms".format(-wait_dur, loop_dur))
                continue

            # Sleep DMX delay time
            sleep(wait_dur / 1000.0)

    def add_callback(self, callback: Callable, interval_millis: float = 1000.0):
        self.__callbacks.append(Callback(callback, interval_millis, None, getframeinfo(stack()[1][0])))

    def remove_callback(self, callback: Callable):
        idx = [i for i, cb in enumerate(self.__callbacks) if cb.callback == callback]
        if len(idx):
            del self.__callbacks[idx[0]]

    def add_animation(self, animation: Animation, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        now = int(self.bars_now()) if snap else self.bars_now()
        start = self.bars_to_millis(now + start_offset)
        end = start + self.bars_to_millis(animation.length)

        self.__animations.append(AnimationCallback(animation, start, end, repeat, getframeinfo(stack()[1][0])))

    def remove_animation(self, animation: Animation):
        self.__animations = list(filter(lambda x: x.animation != animation, self.__animations))

    def clear_callbacks(self):
        self.__callbacks = []

    def set_bpm(self, bpm: int):
        self.__bpm = bpm

    def stop(self):
        # Stop the threaded loop
        self.__ticking = False

    @property
    def paused(self) -> bool:
        return self.__paused

    def pause(self) -> bool:
        # Toggle pause state
        self.__paused = not self.__paused
        return self.paused

    def start(self):
        if not self.__ticking:
            # Create the thread and run loop
            thread = Thread(target=self.__ticker__loop, daemon=True)
            thread.start()

    def nudge(self, ms):
        self.__start_millis += ms
        for callback in self.__callbacks:
            callback.last += ms
            cb_parent_instance = callback.__self__
            if isinstance(cb_parent_instance, Effect):
                cb_parent_instance.nudge(ms)

    def sync(self):
        self.__start_millis = self.millis_now()
        for callback in self.__callbacks:
            callback.last = self.__start_millis
            cb_parent_instance = callback.__self__
            if isinstance(cb_parent_instance, Effect):
                cb_parent_instance.source.sync(self.__start_millis)
