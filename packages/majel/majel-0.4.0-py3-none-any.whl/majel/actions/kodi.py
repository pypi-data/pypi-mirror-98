import json
import subprocess
import time

from typing import Any, Dict
from urllib.parse import urlparse

import kodijson

from mpv import MPV

from ..config import config
from ..messages import Message
from .base import Action


class KodiAction(Action):

    IS_NOISY = True

    def __init__(self) -> None:

        super().__init__()

        self.mount = None
        if config.kodi_mount:
            if mount_remote := config.kodi_mount.get("remote"):
                if mount_local := config.kodi_mount.get("local"):
                    self.mount = {
                        "remote": mount_remote,
                        "local": mount_local,
                    }

        self._meta = {}
        self.client = None
        self.player = None
        self.is_enabled = self.check_setup()

        if self.is_enabled:
            self.client = self.get_client(config.kodi_endpoint)
            self.player = self.get_player()

    def check_setup(self) -> bool:

        if not config.kodi_endpoint:
            self.logger.warning(
                "No Kodi endpoint set.  Without that, we can't be expected to "
                "handle Kodi URLs, so we're disabling the Kodi player."
            )
            return False

        if not self.mount:
            self.logger.warning(
                "No Kodi mount set.  We're assuming there's no media share to "
                "play with, so we're disabling the Kodi player."
            )
            return False

        if not subprocess.call(["mpv", "--version"]) == 0:
            self.logger.warning(
                "MPV does not appear to be installed.  We can't play local "
                "video without it."
            )
            return False

        return True

    @staticmethod
    def get_client(endpoint: str) -> kodijson.Kodi:
        """
        The kodi-json library doesn't understand standard BasicAuth URLs,
        instead requiring you to extract the username & password from the URL
        and pass them as separate arguments.
        """

        p = urlparse(endpoint)

        url = f"{p.scheme}://{p.hostname}{p.path}"
        if p.port:
            url = f"{p.scheme}://{p.hostname}:{p.port}{p.path}"

        kwargs = {}
        if p.username:
            kwargs["username"] = p.username
        if p.password:
            kwargs["password"] = p.password

        return kodijson.Kodi(url, **kwargs)

    def get_message_types(self) -> Dict[str, callable]:

        if not self.is_enabled:
            return {}

        return {
            "skill.majel.kodi.play": self.play,
            "skill.majel.kodi.stop": self.stop,
        }

    def play(self, info: Message) -> None:  # pragma: no cover

        self.cleanup()

        self.logger.info("Media player started for %s", info)

        self._meta = self._get_details(info.data)

        if self.mount["remote"] not in self._meta["file"]:
            self.logger.warning(
                "The remote Kodi mount you have specified in the config "
                "doesn't appear in the file just received from Kodi.  Are you "
                "sure you've set things up correctly?"
            )

        url = self._meta["file"].replace(
            self.mount["remote"],
            self.mount["local"],
        )
        position = self._meta["resume"]["position"]

        self.player.play(url)

        while self.player.time_remaining is None:
            self.logger.info('Waiting for playback of "%s" to begin', url)
            time.sleep(0.1)

        if not position == 0:
            self.logger.info(f"Seeking to {position}")
            self.player.seek(position, reference="absolute")

        self.setup_next()

    def stop(self, *args) -> None:  # pragma: no cover
        self.logger.info("Stopping")
        self.cleanup()

    def passive(self) -> None:  # pragma: no cover

        if not self.player:
            return

        if self.player.time_remaining:
            return

        # We've reached the end of the episode.  Time to see if there's
        # something next.

        episode_id = self._meta.get("next")
        if episode_id:
            self.logger.info("Next episode id: %s", episode_id)
            self.play(
                Message(
                    "skill.majel.kodi.play",
                    data={"episodeid": episode_id},
                    context={},
                )
            )

        return super().passive()

    def cleanup(self) -> None:  # pragma: no cover

        if not self.player:
            return

        if self.player.stream_pos or self._meta:
            self.save_state()
            self.player.terminate()

        self._meta = {}

        self.player = self.get_player()

    @staticmethod
    def get_player() -> MPV:  # pragma: no cover
        return MPV(
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            fs=True,
        )

    def process(self, raw_data: str) -> None:  # pragma: no cover

        self.logger.info("Media reference found: %s", raw_data)

        # No data means we should stop playing
        if not raw_data:
            return

        info = json.loads(raw_data)

        if not self.player:
            self.logger.error(
                "No NFS mount configured, so %s can't be played", info
            )
            return

        self.play(info)

    def setup_next(self) -> None:  # pragma: no cover
        """
        Ask Kodi if there's a next episode, and if there is, put it into our
        special kodi._meta dict so we can queue it up when this episode
        finishes.
        """

        show_id = self._meta.get("tvshowid")
        episode_id = self._meta.get("episodeid")
        if not show_id:
            return

        self.logger.info("Attempting to get next episode id")

        episodes = self.client.VideoLibrary.GetEpisodes(
            tvshowid=show_id, properties=["title", "playcount"]
        )
        ids = [_["episodeid"] for _ in episodes["result"]["episodes"]]

        try:
            self._meta["next"] = ids[ids.index(episode_id) + 1]
        except IndexError:
            pass  # I guess we're on the last one

    def save_state(self) -> None:  # pragma: no cover
        """
        If the user is fiddling with the play head, `player.time_pos` can have
        a value and then suddenly be `None`, which will cause the math we do
        here to barf.  To work around this, we capture the value early on and
        test that variable for the rest of this method rather than constantly
        referring to `self.player.time_pos`.
        """

        if not self.player:
            return

        t = self.player.time_pos or 1

        self.logger.info(f"Elapsed time: {t}")

        key = "episodeid"
        fn = self.client.VideoLibrary.SetEpisodeDetails
        if "movieid" in self._meta:
            key = "movieid"
            fn = self.client.VideoLibrary.SetMovieDetails

        position = int(t)

        playcount = 0
        if (self.player.time_remaining or 0) < 120:
            playcount = 1
            position = 0

        self.logger.info(
            "Updating Kodi with position=%s, playcount=%s", t, playcount
        )

        fn(
            resume={
                "position": position,
                "total": self._meta["resume"]["total"],
            },
            playcount=playcount,
            **{key: self._meta[key]},
        )

    def _get_details(
        self, info: Dict[str, str]
    ) -> Dict[str, Any]:  # pragma: no cover
        """
        Return format:

          {
            "file": "nfs://host/path/to/movies/file.extension",
            "label": "Movie Title",
            "movieid": 123,
            "tvshowid": 123,
            "episodeid": 123
            "resume": {"position": 0.0, "total": 0.0},
          }

        For movies, you get the `movieid` but not `tvshowid` or `episodeid`.
        For episodes, you get `tvshowid` and `episodeid`, but no `movieid`.
        """

        id_name, pk = info.popitem()

        key = "episodedetails"
        fn = self.client.VideoLibrary.GetEpisodeDetails
        properties = ["file", "resume", "tvshowid"]
        if id_name == "movieid":
            key = "moviedetails"
            fn = self.client.VideoLibrary.GetMovieDetails
            properties = ["file", "resume"]

        r = fn(**{id_name: pk}, properties=properties)["result"][key]

        self.logger.info(f"Received '{r}' from Kodi")

        return r
