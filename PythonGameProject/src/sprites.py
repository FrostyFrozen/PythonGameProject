# Sprite classes dla gry
import pygame as pg 
from opcje import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        def update(self):
            self.acc = vec(0, 0)
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.acc.x = -0.5
            if keys[pg.K_RIGHT]:
                self.acc.x = 0.5
            self.vec += self.acc
            self.pop += self.vel + 0.5 * self.acc
            
            self.rect.center = self.pos
