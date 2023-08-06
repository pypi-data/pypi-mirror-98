from typing import Dict

from ..logger import Loggable


class Action(Loggable):

    IS_NOISY = False

    def __init__(self):
        self.is_noisy = self.IS_NOISY

    def get_message_types(self) -> Dict[str, callable]:
        return {}

    def passive(self) -> None:
        pass

    def cleanup(self) -> None:
        pass
