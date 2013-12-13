
import pygame, sys
from pygame.locals import *

width = 640
height = 480

class mario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mario.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width/7
        self.rect.centery = height*9/10
    
    def mover(self, time, keys):
        if keys[K_RIGHT] and self.rect.right <= width/2:
            self.rect.centerx += 0.5 * time
            if self.rect.right >= width/2:
                self.rect.right = width/2
        if keys[K_LEFT] and self.rect.left >= 0:
            self.rect.centerx -= 0.5 * time
            if self.rect.left <= 0:
                self.rect.left = 0
  
class Fondo(pygame.sprite.Sprite):
    def __init__(self,imagen,left,top):
        self.image = pygame.image.load(imagen)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    
    def mov(self,mario,keys,time,fondo2):
        if mario.rect.right == width/2 and keys[K_RIGHT]:
            self.rect.left -= 0.5 * time
        if self.rect.left < 0 and keys[K_RIGHT] and mario.rect.right == width/2:
            fondo2.rect.left = self.rect.right

def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("fondo")
 
    fondo1 = Fondo("fondo1.png",0,0)
    fondo2 = Fondo("fondo2.png",width,0)
    fondo3 = Fondo("fondo3.png",width*2,0)
    m = mario()
 
    clock = pygame.time.Clock()
     
    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 
        if fondo1.rect.right >= 0:
            fondo1.mov(m, keys, time, fondo2)
        if fondo1.rect.right <= 0:
            fondo1.rect.left = width*2 #El multiplicador n en width*n es igual a la cantidad de fondos
        if fondo2.rect.right >= 0:
            fondo2.mov(m, keys, time, fondo3)
        if fondo2.rect.right <= 0:
            fondo2.rect.left = width*2
        if fondo3.rect.right >= 0:
            fondo3.mov(m, keys, time, fondo1)
        if fondo3.rect.right <= 0:
            fondo3.rect.left = width*2
            
        m.mover(time, keys)
        screen.blit(fondo1.image, (fondo1.rect.left, fondo1.rect.top))
        screen.blit(fondo2.image, (fondo2.rect.left, fondo2.rect.top))
        screen.blit(fondo3.image, (fondo3.rect.left, fondo3.rect.top))
        screen.blit(m.image, m.rect)
        
        pygame.display.flip()
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
    pass