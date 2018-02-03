# Sprite classes dla gry
import pygame as pg
from opcje import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        #self.image = pg.Surface((30, 40))
        #self.image.fill(YELLOW)
        self.image=game.player_img_idle[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    def jump(self):
        #skacze tylko jeli stoi na platformie
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
             self.vel.y = -PLAYER_JUMP
        
    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
                
        # definiowanie tarcia
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # równania ruchu
        self.vel += self.acc
        if abs(self.vel.x) < 0.25:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # boki ekranu
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
        
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # animacja biegu
        if self.walking:
            if now - self.last_update > 180:
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
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.player_img_idle)
                bottom = self.rect.bottom
                self.image = self.game.player_img_idle[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, col):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
