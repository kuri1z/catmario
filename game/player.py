import pygame
import os
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # cesta k souboru relativně k tomuto modulu
        base_dir = os.path.dirname(__file__)
        image_rel = os.path.join(base_dir, "..", "img", "Cat_Mario.webp")
        image_path = os.path.abspath(os.path.normpath(image_rel))

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            print(f"Načten obrázek hráče: {image_path}")
        except (pygame.error, FileNotFoundError, Exception) as e:
            print(f"Nelze načíst '{image_path}': {e}. Používám fallback Surface.")
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
            self.image.fill(PLAYER_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = False

        # pro detekci "stomp" kolize
        self.prev_bottom = self.rect.bottom

    def update(self, platforms):
        # uložíme předchozí spodní pozici pro detekci, zda jsme při kolizi byli nad enemy
        self.prev_bottom = self.rect.bottom

        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
       
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED

        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = -JUMP_POWER
            self.on_ground = False

        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
       
        self.rect.x += self.velocity_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
       
        self.rect.y += self.velocity_y

        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)