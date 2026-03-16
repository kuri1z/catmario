import os

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
PLATFORM_COLOR = (139, 69, 19)

# Player
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_COLOR = (255, 50, 50)
PLAYER_SPEED = 5
JUMP_POWER = 15

# Physics
GRAVITY = 0.8
MAX_FALL_SPEED = 15

# Coins
COIN_SIZE = 12
COIN_COLOR = (255, 215, 0)

# Enemy defaults (používané v enemy.py)
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = (200, 20, 20)
ENEMY_SPEED = 2
ENEMY_CHANGE_PROB = 0.02
ENEMY_EDGE_PADDING = 8

# Assets dir (pokud bude potřeba)
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "img"))