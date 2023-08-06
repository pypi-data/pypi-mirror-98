import logging


class Loggable:
    """
    Use this mixin to do logging:
      self.logger.debug("My debugging message")
    """

    __logger = None

    @property
    def logger(self) -> logging.Logger:

        if self.__logger:
            return self.__logger

        logging.basicConfig()

        self.__logger = logging.getLogger(f"majel.{self.__class__.__module__}")
        self.__logger.setLevel(logging.DEBUG)

        return self.logger

    @classmethod
    def get_logger(cls) -> logging.Logger:  # pragma: no cover
        return logging.getLogger(f"majel.{cls.__module__}")
