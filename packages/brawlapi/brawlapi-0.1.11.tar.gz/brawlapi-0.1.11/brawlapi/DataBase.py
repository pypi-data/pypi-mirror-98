from treefiles import Tree as BaseTree

from brawlapi.Classes import Brawler, Player
from brawlapi.utils import req


class DataBase:
    def __init__(self, url):
        self.url = Tree(url)
        self.url.dir("p", "b")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def players(self) -> list:
        return req(self.url.p.abs()).get("valid")

    def get_player(self, player: str) -> Player:
        return Player(player, self)

    @property
    def brawlers(self) -> list:
        return req(self.url.b.abs()).get("valid")

    def get_brawler(self, brawler: str) -> brawlers:
        return Brawler(brawler, self)



class Tree(BaseTree):
    def abs(self, path=""):
        if self.parent is None:
            return self._name
        return super().abs(path)


