# Sprite classes dla gry
import pygame as pg
from opcje import *
from random import choice, randrange
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.boost_pu = False
        self.reverse_pu = False
        self.jumper_pu=False
        self.jumper_bonus=0
        self.current_frame = 0
        self.last_update = 0
        #self.image = pg.Surface((30, 40))
        #self.image.fill(YELLOW)
        self.image=game.player_img_idle[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        #Słaby skok
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        #skacze tylko jeli stoi na platformie/normalny skok
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
           # self.game.jump_sound.play()
            choice(self.game.jump_sounds).play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP - self.jumper_bonus
        
    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if self.reverse_pu==False:
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC
        else:
            if keys[pg.K_RIGHT]:
                self.acc.x = -PLAYER_ACC
            if keys[pg.K_LEFT]:
                self.acc.x = PLAYER_ACC
                
        # definiowanie tarcia
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # równania ruchu
        self.vel += self.acc
        if abs(self.vel.x) < 0.25:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # boki ekranu
        if self.pos.x > WIDTH + self.rect.width /2:
            self.pos.x = 0 - self.rect.width /2
        if self.pos.x < 0 - self.rect.width /2:
            self.pos.x = WIDTH + self.rect.width /2

        self.rect.midbottom = self.pos
        
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.vel.y < 0:
            self.walking = False  
        # animacja biegu
        if self.walking:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.player_img_runl)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.game.player_img_run[self.current_frame]
                else:
                    self.image = self.game.player_img_runl[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # animacja postac stojaca
        if not self.jumping and not self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.player_img_idle)
                bottom = self.rect.bottom
                self.image = self.game.player_img_idle[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # animacja skoku
        if self.vel.y != 0:
            self.jumping= True
        else:
            self.jumping = False
            
        if self.jumping:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.player_img_jump)
                bottom = self.rect.bottom
                if self.vel.y < 0:
                    self.image = self.game.player_img_jump[self.current_frame]
                if self.vel.x < 0:
                    self.image = self.game.player_img_jumpl[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = (self.game.platform_img)
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Powerup(self.game, self)
        
class Powerup(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POWERUP_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["jumper","boost","reverser"])
        images = (self.game.powerup_img)
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()
class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.mob_img1p
        self.image_up.set_colorkey(BLACK)
        self.image_upp = self.game.mob_img1
        self.image_down = self.game.mob_img2p
        self.image_down.set_colorkey(BLACK)
        self.image_downp = self.game.mob_img2
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.vx > 0:
            if self.dy < 0:
                self.image = self.image_up
            else:
                self.image = self.image_down
        if self.vx < 0:
            if self.dy < 0:
                self.image = self.image_upp
            else:
                self.image = self.image_downp
         
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()