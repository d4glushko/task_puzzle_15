from abc import ABC, abstractmethod


class AbstractInput(ABC):
    @abstractmethod
    def get_ch(self):
        pass


class TerminalInput(AbstractInput):
    def __init__(self, window):
        self.window = window

    def get_ch(self) -> int:
        return self.window.getch()
