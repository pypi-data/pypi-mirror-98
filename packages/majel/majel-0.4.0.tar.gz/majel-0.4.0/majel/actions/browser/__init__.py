from pathlib import Path
from shutil import which
from time import sleep
from typing import Dict, List, Optional, Type

from selenium import webdriver

from ...config import config
from ...messages import Message
from ..base import Action
from .handlers.base import Handler
from .handlers.selector import SelectionHandler


class BrowserAction(Action):  # pragma: no cover

    HOME_URL = (Path(__file__).parent / "index.html").absolute().as_uri()

    def __init__(self):

        super().__init__()

        self.driver = self.get_driver()

        self.cleanup()  # Default to the home page

        self.logger.info(
            "Browser is ready with the following handlers: %s",
            ", ".join(
                [
                    c.__name__.replace("Handler", "")
                    for c in self.get_handlers()
                ]
            ),
        )

    def get_driver(self) -> webdriver.Firefox:

        self.logger.info("Setting up browser")

        options = webdriver.FirefoxOptions()

        if config.firefox_full_screen:
            options.add_argument("--kiosk")

        return webdriver.Firefox(
            service_log_path="/dev/null",
            firefox_profile=webdriver.FirefoxProfile(self.find_profile()),
            firefox_options=options,
            firefox_binary=self.find_binary(),
        )

    def find_profile(self) -> Optional[str]:

        if not config.firefox_profile:
            return None

        glob = (Path.home() / ".mozilla" / "firefox").glob(
            f"*.{config.firefox_profile}"
        )

        try:
            return str(next(glob).absolute())
        except StopIteration:
            self.logger.warning(
                "Could not find Firefox profile: %s", config.firefox_profile
            )
            return None

    def find_binary(self):

        options = (
            "firefox",
            "firefox-developer-edition",
            "firefox-nightly",
        )

        for option in options:
            self.logger.debug("Looking for %s", option)
            if path := which(option):
                self.logger.info("Found: %s", path)
                return path

        raise FileNotFoundError("No Firefox installation could be found.")

    def get_message_types(self) -> Dict[str, callable]:
        return {
            "skill.majel.browser.open": self.handle_single,
            "skill.majel.browser.open-selector": self.handle_multiple,
            "skill.majel.browser.stop": self.handle_stop,
        }

    @staticmethod
    def get_handlers() -> List[Type[Handler]]:
        return sorted(Handler.__subclasses__(), key=lambda c: c.PRIORITY)

    def get_handler(self, payload: str) -> Handler:
        """
        Using the message contents, ask each handler if it can in fact handle
        it.  If it says it can, return an instance of that handler.
        """
        for handler in self.get_handlers():
            name = handler.__name__
            self.logger.info("Checking if %s can handle %s", name, payload)
            if handler := handler.build_from_payload(self.driver, payload):
                self.logger.info("OK: %s can handle %s", name, payload)
                return handler

    def handle_single(self, message: Message) -> None:

        # Force a wait to work around a race condition where Mycroft sends both
        # a stop event and a play event at roughly the same time.
        sleep(1)

        self.logger.info(str(message.data))
        handler = self.get_handler(message.data.get("url"))
        self.is_noisy = handler.handle()

    def handle_multiple(self, message: Message) -> None:

        # See .handle_single() for details.
        sleep(1)

        handler = SelectionHandler(self.driver, message.data.get("urls"))
        self.is_noisy = handler.handle()

    def handle_stop(self, *args) -> None:
        if self.is_noisy:
            self.logger.info("Stopping noisy stream")
            self.cleanup()
        else:
            self.logger.info("Opting to do nothing with a silent stream")

    def cleanup(self) -> None:
        self.is_noisy = False
        self.driver.get(self.HOME_URL)
