# - opcje gry/ ustawienia
TITLE = "Cave Jumper"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"

# Ustawienia gracza
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22
PLAYER_BOXES=(50,70)
PLATFORM_BOXES=(100,50)
ITEM_BOXES=(15,15)
# Ustawienia mobów
MOB_BOXES=(60,30)
MOB_FREQ=(5000)
BAT_IMG= "bat1.png"
BAT_FLY_IMG= "bat2.png"
#Layers
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POWERUP_LAYER = 1
MOB_LAYER = 2


# Ustawienia powerupów
BOOST_POWER = 60
POW_SPAWN_PCT = 7
# - definiowanie kolorów
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED =   (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE =  (0, 0 , 255)
YELLOW =(255, 255, 0)
LIGHTBLUE =(0, 155, 155)
BGCOLOR = BLACK
BG_SIZE =(WIDTH, HEIGHT)

# Platformy startowe
PLATFORM_LIST = [(0, HEIGHT - 40),
                  (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                  (125, HEIGHT - 350),
                  (350,200),
                  (120,100)]
#PLAYER_SKIN="Idle__000.png"

