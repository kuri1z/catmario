import pygame
from config import *
from game.platform import Platform
from game.coin import Coin

class Level:
    """
    Vytvoří kolekci platforem a coinů pro dané číslo levelu.
    Metoda create vrací dvě seznamy: [Platform], [Coin]
    """
    @staticmethod
    def create(level_num: int):
        platforms = []
        coins = []

        # ground
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        platforms.append(ground)

        # základní rozložení platforem (můžeš změnit podle level_num)
        plats = [
            (80, SCREEN_HEIGHT - 160, 140, 16),
            (260, SCREEN_HEIGHT - 240, 120, 16),
            (420, SCREEN_HEIGHT - 200, 160, 16),
            (620, SCREEN_HEIGHT - 280, 120, 16),
            (360, SCREEN_HEIGHT - 340, 100, 16),
            (140, SCREEN_HEIGHT - 300, 90, 16)
        ]

        # případně malé obměny podle level_num (např. posunout platformy)
        offset = (level_num - 1) * 0  # upravitelné
        for x, y, w, h in plats:
            p = Platform(x + offset, y, w, h)
            platforms.append(p)

            # coin nad středem každé platformy
            coin_x = x + w // 2 + offset
            coin_y = y - (COIN_SIZE // 2) - 6
            coins.append(Coin(coin_x, coin_y))

        # pár extra coinů ve vzduchu
        extra = [(200, 200), (520, 140), (720, 220)]
        for cx, cy in extra:
            coins.append(Coin(cx, cy))

        return platforms, coins