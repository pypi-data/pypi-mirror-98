import typing
from abc import ABC, abstractmethod
from threading import Thread
from typing import Callable

from fishy.gui.funcs import GUIFuncsMock

if typing.TYPE_CHECKING:
    from fishy.gui import GUI


class IEngine(ABC):

    def __init__(self, gui_ref: 'Callable[[], GUI]'):
        self.get_gui = gui_ref
        self.start = False
        self.window = None
        self.thread = None

    @property
    def gui(self):
        if self.get_gui is None:
            return GUIFuncsMock()

        return self.get_gui().funcs

    @abstractmethod
    def toggle_start(self):
        ...

    @abstractmethod
    def run(self):
        ...
