import pygame
from pygame.locals import *
from random import randint
from math import sqrt

class Melee(pygame.sprite.Sprite):
    def __init__(self, posx, posy, image, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speed = speed
        self.vivo = True
    
    def update(self, pj, time,*colisionables):
        if self.vivo:
            for c in colisionables:
                if pygame.sprite.spritecollideany(self, c):
                    self.speed *= -1
                    self.rect.centerx += self.speed
                self.rect.centerx += self.speed
                if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                    self.muerte()
    def muerte(self):
            self.vivo = False
            self.image = pygame.image.load('Images/Others/vacio.png')
            
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,enemigo, speed):
        pygame.sprite.Sprite.__init__(self)
        self.wait = True
        self.image = pygame.image.load('Images/Others/bb_p.png')
        self.rect = self.image.get_rect()
        self.image = pygame.image.load('Images/Others/vacio.png')
        self.rect.centerx = enemigo.rect.centerx
        self.rect.centery = enemigo.rect.centery
        self.speed = speed

    def update(self, pj, time, enemigo, vx, vy,resolution, *colisionables):
        if self.wait:
            self.rect.centery = enemigo.rect.centery
            self.rect.centerx = enemigo.rect.centerx
        if not self.wait:
            self.image = pygame.image.load( 'Images/Others/bb_p.png')
            self.rect.centerx += vx*self.speed
            self.rect.centery += vy*self.speed
            for c in colisionables:
                if pygame.sprite.spritecollideany(self, c):
                    self.desaparicion(enemigo)
            if not enemigo.vivo or self.rect.left <= 0 or self.rect.top <= 0 or self.rect.bottom >= resolution[1]:
                self.desaparicion(enemigo)
    
    def desaparicion(self, enemigo):
        self.wait = True
        self.image = pygame.image.load("Images/Others/vacio.png")
        
class Distancia(pygame.sprite.Sprite):
    def __init__(self, posx, posy, image, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect =  self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.vivo = True
        self.speed = speed
        self.proyectil = Proyectil(self, 10)
                
    def update(self, pj, time,resolution, *colisionables):
        """Movimiento de Personaje y colisiones"""
        if self.vivo:
            r = randint(0,2)
            if r == 1 and self.proyectil.wait:
                self.proyectil.wait = False 
            vx, vy = self.velocidad(pj) 

            for c in colisionables:
                if pygame.sprite.spritecollideany(self, c):
                    self.rect.centery -= self.speed
                    self.speed *= -1
                    self.rect.centery += self.speed
                    
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
                    
            self.proyectil.update(pj, time, self, vx, vy, resolution, *colisionables) 

            self.rect.centery += self.speed
    
    def velocidad(self, pj):
        x1 = pj.rect.centerx - self.rect.centerx
        y1 = pj.rect.centery - self.rect.centery
        norm = sqrt(x1**2 + y1**2)
        x2 = x1/norm
        y2 = y1/norm
        return x2, y2
    
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load('Images/Others/vacio.png')