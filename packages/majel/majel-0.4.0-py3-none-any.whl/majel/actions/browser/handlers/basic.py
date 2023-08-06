from .base import Handler


class BasicHandler(Handler):
    """
    The default behaviour: just go to the page and call it a day.  For this
    reason, the priority should be lowest among all other handlers
    """

    PRIORITY = 1

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        return True
