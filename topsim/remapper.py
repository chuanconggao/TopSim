#! /usr/bin/env python3

class Remapper(object):
    def __init__(self, start: int = 0, step: int = 1) -> None:
        self.start = start
        self.step = step


    def next(self) -> int:
        v, self.start = self.start, self.start + self.step
        return v
