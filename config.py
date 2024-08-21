# config.py

TABLE_WIDTH = 800
TABLE_HEIGHT = 400
BALL_RADIUS = 15
POCKET_RADIUS = 32
FPS = 60
FRICTION_COEFFICIENT = 0.99
CUE_LENGTH = 250
DASHED_LINE_LENGTH = 350

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
MAROON = (128, 0, 0)
DARK_GREEN = (0, 128, 0)
GRAY = (169, 169, 169)

# GUI Constants
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 10
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30

# Pockets positions
pockets = [
    (0, 0),  # Top-left corner
    (TABLE_WIDTH // 2, 0),  # Top-center
    (TABLE_WIDTH, 0),  # Top-right corner
    (0, TABLE_HEIGHT),  # Bottom-left corner
    (TABLE_WIDTH // 2, TABLE_HEIGHT),  # Bottom-center
    (TABLE_WIDTH, TABLE_HEIGHT),  # Bottom-right corner
]