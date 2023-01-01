from enum import Enum


class BotMode:
    def __init__(self):
        self.current_mode = BotModes.MAIN

    def set_mode(self, value):
        self.current_mode = value


class BotModes(Enum):
    MAIN = 0
    CALCULATOR = 1
    TIC_TAC_TOE = 2
    CONTACTS = 3
