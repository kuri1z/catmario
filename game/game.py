from os import name
import pygame
from config import *
from game.player import Player
from game.platform import Platform
from game.coin import Coin
from game.enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        # vytvoříme level: zem + několik platforem + coiny + enemy
        self._create_level()

        # score
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.score = 0

    def _create_level(self):
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # několik statických platforem
        plats = [
            (80, SCREEN_HEIGHT - 160, 140, 16),
            (260, SCREEN_HEIGHT - 240, 120, 16),
            (420, SCREEN_HEIGHT - 200, 160, 16),
            (620, SCREEN_HEIGHT - 280, 120, 16),
            (360, SCREEN_HEIGHT - 340, 100, 16),
            (140, SCREEN_HEIGHT - 300, 90, 16)
        ]

        created_platforms = []
        for x, y, w, h in plats:
            p = Platform(x, y, w, h)
            created_platforms.append(p)
            self.platforms.add(p)
            self.all_sprites.add(p)

            # umístíme coin nad střed každé platformy
            coin_x = x + w // 2
            coin_y = y - (COIN_SIZE // 2) - 6
            coin = Coin(coin_x, coin_y)
            self.coins.add(coin)
            self.all_sprites.add(coin)

        # přidej i pár samostatných coinů ve vzduchu
        extra = [(200, 200), (520, 140), (720, 220)]
        for cx, cy in extra:
            c = Coin(cx, cy)
            self.coins.add(c)
            self.all_sprites.add(c)

        # spawneme enemáka na jedné z vytvořených platforem (např. druhá platforma)
        if len(created_platforms) >= 2:
            platform_for_enemy = created_platforms[1]
            enemy = Enemy(platform_for_enemy)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            evt_name = pygame.event.event_name(event.type)

            if event.type == pygame.QUIT:
                self.running = False

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                evt_key = pygame.key.name(event.key)

            elif event.type == pygame.MOUSEMOTION:
                pass

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                pass

    def update(self):
        # aktualizace hráče (platformy jako iterable)
        game_over = self.player.update(self.platforms)
        if game_over:
            self.running = False
            return

        # update enemáků
        self.enemies.update()

        # sbírání coinů: detekce kolize hráč <-> coin, coin zmizí
        hits = pygame.sprite.spritecollide(self.player, self.coins, dokill=True)
        if hits:
            self.score += len(hits)

        # pokud už nejsou žádné coiny -> ukonči hru
        if len(self.coins) == 0:
            self.running = False
            return

        # enemy kolize: pokud hráč na enemáka skočí shora -> enemy dies a hráč odskočí,
        # jinak hráč zemře
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, dokill=False)
        for en in enemy_hits:
            # stomping detekce: byl hráč nad enemy před kolizí a padá dolů?
            was_above = getattr(self.player, "prev_bottom", None) is not None and self.player.prev_bottom <= en.rect.top
            falling = getattr(self.player, "velocity_y", 0) > 0
            if was_above and falling:
                # zabil jsi enemáka
                en.die()
                # bounce hráče trochu nahoru
                self.player.velocity_y = -max(6, JUMP_POWER * 0.6)
                self.player.on_ground = False
                # odstranit z all_sprites již udělá en.kill(), ale ujistíme se
                if en in self.all_sprites:
                    self.all_sprites.remove(en)
            else:
                # hráč umírá při kontaktu z boku/zdola
                self.running = False
                return

    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        for sprite in self.all_sprites:
            sprite.draw(self.screen)

        # vykreslíme score
        score_surf = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_surf, (8, 8))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)