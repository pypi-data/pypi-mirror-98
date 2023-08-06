import shutil

import requests
from box import Box

FRIENDS = dict(
    paul="#YURL00PC",
    jm="#2RQC88R0",
    jojo="#2QV90VPJ",
    adri="#82Q2UGUPP",
    dab="#8UGURCLC",
    pilou="#9YQJVCVU",
    aless="#G8Q9YL0L",
)

RFRIENDS = {v: k for k, v in FRIENDS.items()}


class MODES:
    brawlBall = "brawlBall"
    bounty = "bounty"
    roboRumble = "roboRumble"
    soloShowdown = "soloShowdown"
    gemGrab = "gemGrab"
    heist = "heist"
    duoShowdown = "duoShowdown"
    siege = "siege"
    hotZone = "hotZone"


class TYPES:
    ranked = "ranked"
    friendly = "friendly"
    proLeague = "proLeague"


def req(url):
    r = requests.get(url)
    if r.status_code == 200:
        return Box(r.json())
    else:
        raise BrawlAPIError(r.reason)


def dwnl_image(image_url, fname):
    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(fname, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    else:
        raise BrawlAPIError(r.reason)


class BrawlAPIError(Exception):
    pass
