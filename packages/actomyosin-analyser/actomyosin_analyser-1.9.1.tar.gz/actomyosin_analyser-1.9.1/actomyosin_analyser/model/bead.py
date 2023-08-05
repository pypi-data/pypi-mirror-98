from typing import List

STATE_FILAMENT_INTERIOR = 2.0
STATE_FILAMENT_START    = 1.0
STATE_FILAMENT_END      = 3.0


class Bead:

    def __init__(self):
        self.previous = -1
        self.next = -1
        self.cross = -1


class Filament:

    def __init__(self, items: List[int], motors: List[int]):
        self.items = items
        self.motors = motors
