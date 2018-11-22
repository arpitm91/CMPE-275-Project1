from __future__ import print_function
from threading import Timer
from random import randint
from input_output_util import log_info


class TimerUtil:
    def __init__(self, callback, time=None):
        self.timer = None
        self.callback = callback
        self.time = time
        log_info("creating timer")

    def start(self):
        if self.timer != None:
            self.stop()
        if not self.time:
            time = self.get_random_time()
        else:
            time = self.time
        self.timer = Timer(time, self.callback)
        self.timer.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()
        self.timer = None

    def reset(self):
        self.stop()
        self.start()

    def get_random_time(self):
        return (randint(150, 300) / 100) * 4
