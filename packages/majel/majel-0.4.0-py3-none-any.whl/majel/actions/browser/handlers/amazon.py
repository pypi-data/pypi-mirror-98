import re

from .base import Handler


class AmazonHandler(Handler):

    # Amazon's URL schema is WACKY and varies from country to country.  I have
    # no way of knowing if this regex covers them all, but we have to be
    # careful not to inadvertently claim support for an AWS page or a normal
    # Amazon page selling socks.
    CAN_HANDLE_REGEX = re.compile(
        r"^https://("
        r"watch\.amazon\.[^/]+/detail?.*asin=[A-Z0-9]{5}|"
        r"(www\.)?amazon\.[^/]+/gp/(video|product)/[A-Z0-9]{5}|"
        r"(www\.)?amazon\.[^/]+/gp/video/detail/[A-Z0-9]{5}"
        r")"
    )

    IS_NOISY = True

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        return bool(cls.CAN_HANDLE_REGEX.match(payload))

    def post_fetch(self):  # pragma: no cover
        self._click("#dv-action-box a:first-of-type")
