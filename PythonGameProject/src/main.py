# Jumping Heavens - platform game


import pygame as pg
import random
from opcje import *
from sprites import *
from os import path
import random as rnd

class Game:
    def __init__(self):
        # inicjalizacja okna gry, itp.       
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        # high score #czytanie i pisanie, jesli nie istnieje to stworzy plik
        self.dir = path.dirname(__file__)
        self.img_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/postac"
        self.plat_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/platformy"
        # ładowanie dźwieków
        self.sound_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/dzwiek"
       # self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, "jumppp2.ogg"))
        self.jump_sounds=[]
        for i in range(2):
            jump1=pg.mixer.Sound(path.join(self.sound_dir, "jumppp2.ogg"))
            self.jump_sounds.append(jump1)
            jump2=pg.mixer.Sound(path.join(self.sound_dir, "jumppp1.ogg"))
            self.jump_sounds.append(jump2)
        
        # jeden obrazek dla gracza
        self.player_img_idle=[]
        self.player_img_jump=[]
        self.player_img_run=[]
        self.player_img_runl=[]
        self.player_img_jumpl=[]
        for i in range(10):
            img_idle=pg.image.load(path.join(self.img_dir,"Idle__00"+str(i)+".png")).convert_alpha()
            img_idle=pg.transform.scale(img_idle,PLAYER_BOXES)
            self.player_img_idle.append(img_idle)
            # skok w prawo
            img_jump=pg.image.load(path.join(self.img_dir,"Jump__00"+str(i)+".png")).convert_alpha()
            img_jump=pg.transform.scale(img_jump,PLAYER_BOXES)
            self.player_img_jump.append(img_jump)
            # skok w lewo
            img_jumpl=pg.image.load(path.join(self.img_dir,"Jump__00"+str(i)+".png")).convert_alpha()
            img_jumpl=pg.transform.scale(img_jumpl,PLAYER_BOXES)
            img_jumpl=pg.transform.flip(img_jumpl, True, False)
            self.player_img_jumpl.append(img_jumpl)
            #bieg w prawo
            img_run=pg.image.load(path.join(self.img_dir,"Run__00"+str(i)+".png")).convert_alpha()
            img_run=pg.transform.scale(img_run,PLAYER_BOXES)
            self.player_img_run.append(img_run)
            #bieg w lewo
            img_runl=pg.image.load(path.join(self.img_dir,"Run__00"+str(i)+".png")).convert_alpha()
            img_runl=pg.transform.scale(img_runl,PLAYER_BOXES)
            img_runl=pg.transform.flip(img_runl, True, False)
            self.player_img_runl.append(img_runl)
            #platformy grafika
        self.platform_img = []
        for i in range(3):
            plat_img=pg.image.load(path.join(self.plat_dir,"platforma"+str(i)+".png")).convert_alpha()
            plat_img=pg.transform.scale(plat_img,PLATFORM_BOXES)
            self.platform_img.append(plat_img)
        
        ## --------------
        with open(path.join(self.dir, HS_FILE), 'w') as f:
             try:
                 self.highscore = int(f.read())
             except:
                 self.highscore = 0
             
    def new(self):
        # Nowa Gra
        rnd.seed(1)
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(self,*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(path.join(self.sound_dir, "old_cave.ogg"))
        self.run()
    
    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while  self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)
         
    def update(self):
        # Game Loop - Update
       self.all_sprites.update()
        # Sprawdza czy  gracz dotyka platformy kiedy tylko spada
       if self.player.vel.y > 0:
             hits = pg.sprite.spritecollide(self.player,self.platforms, False)
             if hits: 
                 lowest = hits[0] #jesli są np 2 platformy nad sobą, snapuje do tej, która przeskoczylismy
                 for hit in hits:
                     if hit.rect.bottom > lowest.rect.bottom:
                         lowest = hit
                 if self.player.pos.y < lowest.rect.centery: #snapuje kiedy stopy sa powyzej platformy
                     self.player.pos.y = lowest.rect.top + 1
                     self.player.vel.y = 0
                     self.player.jumping = False
        # Jesli gracz dociera na sama gore ekranu
       if self.player.rect.top <= HEIGHT /4:
           self.player.pos.y += max(abs(self.player.vel.y), 2)
           for plat in self.platforms:
               plat.rect.y += max(abs(self.player.vel.y), 2)
               if plat.rect.top >= HEIGHT:
                   plat.kill()
                   self.score += 10
        # Smierc gracza
       if self.player.rect.bottom > HEIGHT:
           for sprite in self.all_sprites:
               sprite.rect.y -= max(self.player.vel.y, 10)
               if sprite.rect.bottom < 0:
                   sprite.kill()
       if len(self.platforms) == 0: 
           self.playing = False
           
        # Spawnowanie nowych platform   
       while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)
            
#STARE
                   
    def events(self):
        # Game Loop - Events
       for event in pg.event.get():
           #sprawdza czy zamknieto okno
           if event.type == pg.QUIT:             
               if self.playing:
                   self.playing = False
               self.running = False
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:
                   self.player.jump()
           if event.type == pg.KEYUP:
               if event.key == pg.K_SPACE:
                   self.player.jump_cut()          
        
    
    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawinf everything, flip the display
        pg.display.flip()
    
    def show_start_screen(self):
        # game splash/ekran startowy
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT /4)
        self.draw_text("Użyj strzałek do poruszania się,a spacji do skakania", 22,
                       WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Wcisnij dowolny klawisz, aby zaczac gre", 22, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score:" + str(self.highscore), 22, WHITE, WIDTH /2, 15)
        pg.display.flip()
        self.wait_for_key()
        
    def show_go_screen(self):
        #game over/ kontynuacja
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("Koniec Gry", 48, WHITE, WIDTH / 2, HEIGHT /4)
        self.draw_text("Score:" + str(self.score), 22,
                       WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Wcisnij dowolny klawisz, aby zaczac od nowa", 22, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score:" + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()