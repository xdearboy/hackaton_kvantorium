from src.manage_owner import Owner
from src.shop import Shop


class Game:
    def __init__(self):
        self._owner = Owner
        self._shop = Shop
        self._day_counter = self._day_counter