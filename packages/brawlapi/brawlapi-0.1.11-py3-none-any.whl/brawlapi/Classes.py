from datetime import timedelta

import pandas as pd
from box import Box
from dateutil.parser import parse as ParseDate

from brawlapi.utils import req, dwnl_image


class BaseP:
    def __init__(self, name, db):
        self.name = name
        self.db = db

        self.url = db.url.p.dir(name)

    @property
    def keys(self):
        return req(self.url.abs()).get("valid")

    def __repr__(self):
        return f"<class 'api.{type(self).__name__}'>: {self.name!r}"


class Battle(Box):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

    @property
    def start(self):
        return ParseDate(self.get("battle_time"))

    @property
    def end(self):
        if self.duration is not None:
            return self.start + timedelta(seconds=self.duration)

    @property
    def duration(self):
        return self.battle.get("duration")

    @property
    def mode(self):
        return self.battle.mode


class Player(BaseP):
    def __init__(self, name, db):
        super().__init__(name, db)
        self.url = db.url.p.dir(name)

    def get_battles(self, day_key) -> list:
        battles = req(self.url.path(day_key))
        return list(map(Battle, battles.values()))

    def __getitem__(self, iday):
        return self.get_battles(self.keys[iday])

    def __len__(self):
        return len(self.keys)

    @property
    def battles(self):
        for x in self.keys:
            yield self.get_battles(x)


class Brawler(BaseP):
    def __init__(self, name, db):
        super().__init__(name, db)
        self.url = db.url.b.dir(name)

    def get_csv(self, key) -> pd.DataFrame:
        assert key != "img"
        csv = req(self.url.path(key))
        return pd.DataFrame(data=csv)

    @property
    def stats(self):
        return self.get_csv("stats")

    @property
    def invocs(self):
        return self.get_csv("invocs")

    @property
    def levels(self):
        return self.get_csv("levels")

    def dwnl_image(self, fname) -> None:
        image_url = self.url.path("img")
        dwnl_image(image_url, fname)
