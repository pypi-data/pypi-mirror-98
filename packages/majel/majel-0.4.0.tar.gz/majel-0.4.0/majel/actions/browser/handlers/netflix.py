from .base import Handler


class NetflixHandler(Handler):

    IS_NOISY = True

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        return payload.startswith("https://www.netflix.com/title/")

    def get_prepared_url(self) -> str:
        return f"https://www.netflix.com/watch/{self.payload[30:]}"

    def post_fetch(self):  # pragma: no cover
        self._click(".nf-big-play-pause > button:nth-child(1)")
