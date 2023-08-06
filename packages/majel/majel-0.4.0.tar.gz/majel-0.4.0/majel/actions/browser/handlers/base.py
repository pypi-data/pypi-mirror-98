import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from ....logger import Loggable


class Handler(Loggable):
    """
    The abstract handler for all URLs.  Subclass this to handle different URL
    types.
    """

    MAX_WAIT = 10  # Seconds
    PRIORITY = 0

    IS_NOISY = False

    def __init__(self, driver: webdriver.Firefox, payload: str):
        self.payload = payload
        self.driver = driver

    @classmethod
    def build_from_payload(cls, driver: webdriver.Firefox, payload: str):
        if cls.can_handle(payload):
            return cls(driver, payload)

    @classmethod
    def can_handle(cls, payload: str) -> bool:  # pragma: no cover
        """
        Return True if this URL is something you can handle.
        """
        return False

    def handle(self) -> bool:

        self.pre_fetch()

        url = self.get_prepared_url()

        self.logger.info("Getting %s", url)
        self.driver.get(url)

        self.post_fetch()

        return self.get_noisy_status()

    def pre_fetch(self):
        """
        Do something before the URL has been requested.  I'm not sure how this
        might be used, but it seemed short-sighted not to include a hook for
        it.
        """

    def get_prepared_url(self) -> str:
        """
        Sometimes a URL needs to be modified before it's requested.  If that's
        the case, return the modified version here.
        """
        return self.payload

    def post_fetch(self):
        """
        Do something after the URL has been requested.  Typically this will be
        some Selenium actions.
        """

    def get_noisy_status(self):
        """
        If a URL is considered "noisy", it'll be killed before whenever a
        stop order is issued.  This means that if you're watching Netflix and
        then ask to play the news, the browser will return to the home page.
        However if you're reading a recipe, asking for a weather report won't
        redirect your browser anywhere.
        """
        return self.IS_NOISY

    def _click(self, selector: str) -> None:  # pragma: no cover
        """
        A Selenium hack: attempt to find the thing we want to click on, and
        keep trying for MAX_WAIT seconds just in case the page loading is slow.
        """

        self.logger.info("Clicking %s", selector)

        start_time = time.time()

        while True:
            try:
                self.logger.info(f"Looking for {selector}")
                self.driver.find_element_by_css_selector(selector).click()
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > self.MAX_WAIT:
                    self.logger.error(
                        "Failed to find the thing you wanted to click"
                    )
                    return
                time.sleep(0.5)
