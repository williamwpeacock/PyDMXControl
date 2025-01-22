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

import math

class Callback:

    def __init__(self, callback, interval, last, source):
        if not callable(callback):
            raise InvalidArgumentException('callback', 'Not callable')

        self.callback = callback
        self.interval = interval
        self.last = last
        self.source = source

class AnimationCallback:

    def __init__(self, animation, setting_func, start, end, repeat, source):
        self.animation = animation
        self.setting_func = setting_func
        self.start = start
        self.end = end
        self.repeat = repeat
        self.source = source
        self.playing = True

    def callback(self, now):
        result = self.animation.callback(now)
        if self.setting_func:
            self.setting_func(result)

    def stop(self):
        final_result = self.animation.stop()
        if self.setting_func:
            self.setting_func(final_result)

    def restart(self, controller, delay, force = False):
        num_missed = math.floor(delay / self.animation.length)
        if force:
            self.animation.start(
                controller,
                self.setting_func,
                0,
                self.repeat
            )
        elif self.repeat < 1 or (self.repeat > 1 and self.repeat - (1 + num_missed) >= 1):
            self.animation.start_at(
                controller,
                self.setting_func,
                controller.ticker.millis_to_bars(self.end) + (self.animation.length * num_missed),
                self.repeat - (1 + num_missed)
            )

class Ticker:

    @staticmethod
    def millis_now() -> float:
        return time() * 1000.0

    def bars_now(self) -> float:
        return self.millis_to_bars(self.millis_now())
    
    def relative_millis_now(self):
        return self.millis_now() - self.__start_millis
    
    def relative_bars_now(self):
        return self.millis_to_bars(self.relative_millis_now())

    def bars_to_millis(self, bars: float) -> float:
        return ((bars * 4 * 60 * 1000) / self.__bpm)

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
            if animation.start <= self.relative_millis_now() and animation.end > self.relative_millis_now():
                animation.callback(self.relative_bars_now() - self.millis_to_bars(animation.start))

            elif animation.end <= self.relative_millis_now():
                animation.stop()
                delay = self.millis_to_bars(self.relative_millis_now() - animation.end)
                animation.restart(self.__controller, delay)
                self.remove_animation(animation)

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

    def add_animation(self, animation: Animation, setting_func, start_offset: float = 0, snap: bool = True, repeat: int = 1):
        now = round(self.relative_bars_now()) if snap else self.relative_bars_now()
        return self.add_animation_at(animation, setting_func, now + start_offset, repeat)
    
    def add_animation_at(self, animation, setting_func, start_time, repeat):
        start = self.bars_to_millis(start_time)
        end = start + self.bars_to_millis(animation.length)

        anim_callback = AnimationCallback(animation, setting_func, start, end, repeat, getframeinfo(stack()[1][0]))

        self.__animations.append(anim_callback)
        return anim_callback

    def remove_animation(self, animation: AnimationCallback):
        self.__animations = list(filter(lambda x: x != animation, self.__animations))

    def clear_callbacks(self):
        self.__callbacks = []

    def set_bpm(self, bpm: int):
        self.__bpm = bpm

    def get_bpm(self):
        return self.__bpm

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
        # nudge animations

    def sync(self):
        self.__start_millis = self.millis_now()
        for anim in self.__animations:
            anim.stop()
            anim.restart(self.__controller, 0, True)

