# - opcje gry/ ustawienia
TITLE = "PythonGameProject"
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

# - definiowanie kolorów
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED =   (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE =  (0, 0 , 255)
YELLOW =(255, 255, 0)
LIGHTBLUE =(0, 155, 155)
BGCOLOR = BLUE

# Platformy startowe
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, RED),
                  (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20, YELLOW),
                  (125, HEIGHT - 350, 100, 20, RED),
                  (350,200,100,20, RED),
                  (120,100,100,20, RED)]

