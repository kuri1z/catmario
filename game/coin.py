import pygame
from config import *

class Coin(pygame.sprite.Sprite):
    """
    Jednoduchý sběratelný coin.
    Má .image a .rect a metodu draw pro konzistentní vykreslování.
    """

    def __init__(self, x, y):
        super().__init__()
        size = COIN_SIZE
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # nakreslíme kruh do průhledného surface
        pygame.draw.circle(self.image, COIN_COLOR, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        