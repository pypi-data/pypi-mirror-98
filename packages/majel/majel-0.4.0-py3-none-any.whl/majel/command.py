#!/usr/bin/env python3

import asyncio
import json
import sys
import time

from websockets import connect as ws_connect
from websockets.exceptions import WebSocketException

from .actions.base import Action
from .config import ConfigurationError, config
from .exceptions import MajelError
from .logger import Loggable
from .messages import Message


class Majel(Loggable):
    """
    The main command the at runs Majel.  When you call this class, it fires up
    a loop wherein it hits up Mycroft's websocket for new information every
    second, actions anything relevant, then executes every action's `passive()`
    method before restarting the loop.
    """

    def __init__(self) -> None:
        self.endpoint = config.mycroft_endpoint
        self.actions = [a() for a in Action.__subclasses__()]
        self.action_register = {}

    def __call__(self, *args, **kwargs):

        for action in self.actions:
            for type_, fn in action.get_message_types().items():
                self.logger.info(
                    "Registering %s to %s.%s",
                    type_,
                    action.__class__.__name__,
                    fn.__name__,
                )
                self.action_register[type_] = fn

        try:
            # self.wait_for_message_bus()
            asyncio.run(self.loop())
        except KeyboardInterrupt:
            self.logger.info("Exiting")

    async def loop(self):
        """
        Run an infinite loop where we wait for messages from Mycroft and also
        execute .passive() so the various actions can do loop-based things
        without need of a message.

        In the common case where one might start Mycroft and Majel at the same
        time, we don't want Majel to flip out 'cause it can't connect to
        Mycroft's message bus.  So we catch any websocket exceptions and just
        re-run the loop.
        """

        try:

            async with ws_connect(self.endpoint) as ws:

                self.logger.info("Mycroft's message bus is up")

                while True:

                    before = time.time()

                    try:
                        message = await asyncio.wait_for(ws.recv(), timeout=1)
                    except asyncio.exceptions.TimeoutError:
                        message = ""

                    if message:
                        try:
                            self.on_message(message)
                        except Exception as e:
                            self.logger.error(e)

                    # Limit calls to .passive() to 1/sec at most
                    if time.time() - before >= 1:
                        self.passive()

        except (WebSocketException, OSError) as e:

            time.sleep(3)

            message = "Couldn't connect to Mycroft (%s).  Trying again..."
            self.logger.info(message, e)

            await self.loop()

    def passive(self):
        for action in self.actions:
            action.passive()

    def on_message(self, message: str):

        try:
            payload = json.loads(message)
            type_ = payload["type"]
            data = payload["data"]
            context = payload.get("context", {})
        except (json.decoder.JSONDecodeError, KeyError):
            raise MajelError(f"Unparseable message received: {message}")

        if type_ not in self.action_register:
            return

        for action in self.actions:
            if action.is_noisy:
                action.cleanup()

        self.logger.info("Message received: %s", message)
        self.action_register[type_](Message(type_, data, context))

    @classmethod
    def run(cls):
        """
        I wish I knew a cleaner way to do this, but this appears to be required
        to play nice with the syntax in pyproject.toml.
        """
        cls()()


if __name__ == "__main__":
    try:
        Majel()()
    except ConfigurationError as exc:
        sys.stderr.write(str(exc))
