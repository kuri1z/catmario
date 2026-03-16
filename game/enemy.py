import pygame
import random
from config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, platform, width=ENEMY_WIDTH, height=ENEMY_HEIGHT,
                 speed=ENEMY_SPEED, color=ENEMY_COLOR,
                 change_prob=ENEMY_CHANGE_PROB, edge_padding=ENEMY_EDGE_PADDING):
        """
        Enemy patroluje po dané platformě.
        """
        super().__init__()
        self.platform = platform
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect()

        # postavíme enemáka na platformu
        self.rect.bottom = platform.rect.top
        self.rect.x = platform.rect.left + edge_padding

        # směry a limity
        self.speed = max(1, int(abs(speed)))
        self.vx = self.speed if random.random() < 0.5 else -self.speed
        self.left_limit = platform.rect.left + edge_padding
        self.right_limit = platform.rect.right - self.rect.width - edge_padding

        self.change_prob = change_prob
        self.alive = True

    def update(self, *args, **kwargs):
        if not self.alive:
            return

        # držíme enemáka na platformě
        self.rect.bottom = self.platform.rect.top

        # náhodné otočení
        if random.random() < self.change_prob:
            self.vx = -self.vx

        self.rect.x += self.vx

        # ohraničení na hranice platformy
        if self.rect.x <= self.left_limit:
            self.rect.x = self.left_limit
            self.vx = abs(self.vx) or self.speed
        elif self.rect.x >= self.right_limit:
            self.rect.x = self.right_limit
            self.vx = -abs(self.vx) or -self.speed

    def die(self):
        # označíme jako mrtvého a odstraníme surface (můžeme přidat animaci)
        self.alive = False
        self.kill()

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)