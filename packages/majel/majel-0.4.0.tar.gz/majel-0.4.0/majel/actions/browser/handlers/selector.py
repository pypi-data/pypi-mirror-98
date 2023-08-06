import json
import random
import tempfile

from pathlib import Path

from .base import Handler


class SelectionHandler(Handler):
    """
    When multiple URLs are sent back to allow the user to choose which one.
    """

    TEMPLATE = Path(__file__).parent.parent / "template.html"

    def __init__(self, driver, payload) -> None:
        super().__init__(driver, payload)
        self.scratch = tempfile.NamedTemporaryFile(
            prefix="majel-", suffix=".html"
        )
        self.pages = json.loads(payload)

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        """
        When the payload isn't a URL at all, but a JSON blob in the format:
          [{"url": url, "title": str},...]
        """
        return payload.startswith("[")

    def get_prepared_url(self) -> str:
        return f"file://{self.scratch.name}"

    def pre_fetch(self):

        with open(self.TEMPLATE) as f:
            template = f.read()

        links = ""
        for page in self.pages:
            links += '<a class="{}" href="{}">{}</a>'.format(
                self._get_button_colour(), page["url"], page["title"]
            )

        with open(self.scratch.name, "w") as f:
            f.write(
                template.replace("{{ links }}", links).replace(
                    "{{ columns }}", str(self._get_columns())
                )
            )

    def _get_columns(self):  # pragma: no cover
        page_count = len(self.pages)
        if page_count < 4:
            return page_count
        if page_count < 10:
            return 3
        if page_count < 17:
            return 4
        return 5

    @staticmethod
    def _get_button_colour():
        return "lc2375{:02d}".format(random.randint(1, 8))
