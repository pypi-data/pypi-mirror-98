from .base import Handler


class YoutubeHandler(Handler):

    IS_NOISY = True

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        return payload.startswith("https://www.youtube.com/watch?")

    def get_prepared_url(self) -> str:
        return self.payload.replace("youtube", "yout-ube")

    def post_fetch(self):  # pragma: no cover
        self._click(".ytp-large-play-button")
