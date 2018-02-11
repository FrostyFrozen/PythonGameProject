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
        self.freeze_all_motor_functions=False
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        self.img_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/postac"
        self.plat_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/platformy"
        self.item_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/przedmioty"
        self.mob_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/mob"
        self.background_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/images/tlo"
        # ładowanie dźwieków
        self.sound_dir="C:/Users/czajk/Desktop/Programowanie/PythonGameProject/PythonGameProject/dzwiek"
       # self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, "jumppp2.ogg"))
        self.jump_sounds=[]
        jump1=pg.mixer.Sound(path.join(self.sound_dir, "jumppp2.ogg"))
        self.jump_sounds.append(jump1)
        jump2=pg.mixer.Sound(path.join(self.sound_dir, "jumppp1.ogg"))
        self.jump_sounds.append(jump2)
        self.boost_sound=pg.mixer.Sound(path.join(self.sound_dir, "boost.wav"))
        self.jumper_sound=pg.mixer.Sound(path.join(self.sound_dir, "jumper.wav"))
        self.reverser_sound=pg.mixer.Sound(path.join(self.sound_dir, "reverser.wav"))
        self.death_sound= pg.mixer.Sound(path.join(self.sound_dir, "dead.ogg"))
        
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
            
            #POWER UP
        self.powerup_img=[]
        power_img = pg.image.load(path.join(self.item_dir,"boxItem"+".png")).convert_alpha()
        power_img = pg.transform.scale(power_img,ITEM_BOXES)
        self.powerup_img.append(power_img)
            #MOB
        self.mob_img1 = pg.image.load(path.join(self.mob_dir,BAT_IMG)).convert_alpha()
        self.mob_img1 = pg.transform.scale(self.mob_img1,MOB_BOXES)
        self.mob_img2 = pg.image.load(path.join(self.mob_dir,BAT_FLY_IMG)).convert_alpha()
        self.mob_img2 = pg.transform.scale(self.mob_img2,MOB_BOXES)
        
        self.mob_img1p = pg.image.load(path.join(self.mob_dir,BAT_IMG)).convert_alpha()
        self.mob_img1p = pg.transform.scale(self.mob_img1p,MOB_BOXES)
        self.mob_img1p = pg.transform.flip(self.mob_img1p, True, False)
        self.mob_img2p = pg.image.load(path.join(self.mob_dir,BAT_FLY_IMG)).convert_alpha()
        self.mob_img2p = pg.transform.scale(self.mob_img2p,MOB_BOXES)
        self.mob_img2p = pg.transform.flip(self.mob_img2p, True, False)
            #TŁO
        self.background_img = pg.image.load(path.join(self.background_dir,"cave2"+".png")).convert_alpha()
        self.background_img = pg.transform.scale(self.background_img,BG_SIZE)
        self.background_img_dark = pg.image.load(path.join(self.background_dir,"cave_dark"+".png")).convert_alpha()
        self.background_img_dark = pg.transform.scale(self.background_img_dark,BG_SIZE)

        
        # high score, jesli nie istnieje to stworzy plik
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
             try:
                 self.highscore = int(f.read())
             except:
                 self.highscore = 0
             
    def new(self):
        # Nowa Gra
        rnd.seed(1)
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self,*plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.sound_dir, "old_cave.ogg"))
        pg.mixer.music.play(loops=-1)
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
        pg.mixer.music.fadeout(800)
         
    def update(self):
        # Game Loop - Update
       self.all_sprites.update()
       # spawnowanie mobów
       now = pg.time.get_ticks()
       if now - self.mob_timer > 5000 + choice([-1000, -500, 0, 500, 1000]):
           self.mob_timer = now
           Mob(self)
       # kiedy dotyka moba
       mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
       if mob_hits:
           self.playing = False
           self.death_sound.play()
           
       # Sprawdza czy  gracz dotyka platformy kiedy tylko spada
       if self.player.vel.y > 0:
             hits = pg.sprite.spritecollide(self.player,self.platforms, False)
             if hits: 
                 lowest = hits[0] #jesli są np 2 platformy nad sobą, snapuje do tej, która przeskoczylismy
                 for hit in hits:
                     if hit.rect.bottom > lowest.rect.bottom:
                         lowest = hit
                 if self.player.pos.x - 12 < lowest.rect.right and \
                     self.player.pos.x + 12 > lowest.rect.left:
                         if self.player.pos.y < lowest.rect.centery: #snapuje kiedy stopy sa powyzej platformy
                             self.player.pos.y = lowest.rect.top + 1
                             self.player.vel.y = 0
                             self.player.jumping = False
                     
        # Jesli gracz dociera na sama gore ekranu
       if self.player.rect.top <= HEIGHT /4:
           self.player.pos.y += max(abs(self.player.vel.y), 2)
           for mob in self.mobs:
               mob.rect.y += max(abs(self.player.vel.y), 2)
           for plat in self.platforms:
               plat.rect.y += max(abs(self.player.vel.y), 2)
               if plat.rect.top >= HEIGHT:
                   plat.kill()
                   self.score += 10
        # kiedy gracz doknie powerupa
       pow_hits = pg.sprite.spritecollide(self.player,self.powerups, True)
       for pow in pow_hits:
            if pow.type == "boost":
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
                self.freeze_all_motor_functions = True
                self.player.boost_pu=True
                now = pg.time.get_ticks()
                self.boost_update = now

                    
            if pow.type == "reverser":
                self.reverser_sound.play()
                self.player.reverse_pu=True
                now = pg.time.get_ticks()
                self.reverser_update = now
            if pow.type == "jumper":
                self.jumper_sound.play()
                self.player.jumper_pu=True
                now = pg.time.get_ticks()
                self.jumper_update = now
                self.player.jumper_bonus=10
                
                
       if self.player.boost_pu==True:
            now = pg.time.get_ticks()
            if now - self.boost_update > 1200:
                self.freeze_all_motor_functions = False
                self.player.boost_pu=False
                
       if self.player.reverse_pu==True:
            now = pg.time.get_ticks()
            if now - self.reverser_update > 4000:
                self.player.reverse_pu=False
                
       if self.player.jumper_pu==True:
            now = pg.time.get_ticks()
            if now - self.jumper_update > 4000:
                self.player.jumper_pu=False
                self.player.jumper_bonus=0
                    
        
                
                
        # Smierc gracza
       if self.player.rect.bottom > HEIGHT:
           for sprite in self.all_sprites:
               sprite.rect.y -= max(self.player.vel.y, 10)
               if sprite.rect.bottom < 0:
                   sprite.kill()
       if len(self.platforms) == 0: 
           self.playing = False
           self.death_sound.play()
           
        # Spawnowanie nowych platform   
       while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            
                   
    def events(self):
        # Game Loop - Events
       for event in pg.event.get():
           #sprawdza czy zamknieto okno
           if event.type == pg.QUIT:             
               if self.playing:
                   self.playing = False
               self.running = False
           if event.type == pg.KEYDOWN and self.freeze_all_motor_functions==False:
               if event.key == pg.K_SPACE:
                   self.player.jump()
           if event.type == pg.KEYUP and self.freeze_all_motor_functions==False:
               if event.key == pg.K_SPACE:
                   self.player.jump_cut()          
        
    
    def draw(self):
        # Game Loop - Draw
        self.screen.blit(self.background_img, [0,0])
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawinf everything, flip the display
        pg.display.flip()
    
    def show_start_screen(self):
        # game splash/ekran startowy
        pg.mixer.music.load(path.join(self.sound_dir, "Space_Sprinkles.ogg"))
        pg.mixer.music.play(loops=-1)
        self.screen.blit(self.background_img_dark, [0,0])
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT /4)
        self.draw_text("Użyj strzałek do poruszania się,a spacji do skakania", 22,
                       WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Wciśnij dowolny klawisz, aby zacząć grę", 22, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Najlepszy wynik:" + str(self.highscore), 22, WHITE, WIDTH /2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(1000)
        
    def show_go_screen(self):
        #game over/ kontynuacja
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.sound_dir, "Lurid_Delusion.ogg"))
        pg.mixer.music.play(loops=-1)
        self.screen.blit(self.background_img, [0,0])
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
        pg.mixer.music.fadeout(900)
    
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