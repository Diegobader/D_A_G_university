import pygame
import pygame, sys
from pygame.locals import *
width=640
height=420
class BB(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('stk_and_soap_mace.png')
        self.sheet.set_clip(pygame.Rect(341, 10, 69, 67))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        self.frame = 0

        self.left_states={ 0: (341, 10, 69, 67)}
        self.bu_states={0: (416,10,69,67)}

        
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect


    def update(self, left,bu,right):
        if left:
            self.clip(self.left_states)
            self.xvel=-5
        if bu:
            self.clip(self.bu_states)

        if right:
            self.xvel=5
            self.clip(self.left_states)
        if not (right or left):
            self.xvel=0
        if self.xvel==0 and not bu:
            self.clip(self.left_states[0])
        self.rect.x+=self.xvel   
        self.bu=False    
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        
    def handle_event(self):
        left=bu=right=False
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        while pygame.event.get(): pass
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            game_over = True
        
        if event.type == pygame.KEYDOWN:

            if key[pygame.K_a]:
                left=True
            if key[pygame.K_f]:
                bu=True
            if key[pygame.K_d]:
                right=True

        if event.type == pygame.KEYUP:  
 

            if event.key == pygame.K_a:
                left=False
            if event.key==pygame.K_f:
                bu=False
            if event.key==pygame.K_d:
                right=False
        self.update(left,bu,right)

        
##################################################

        
class PJ(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('stk_and_soap_mace.png')
        self.sheet.set_clip(pygame.Rect(6, 52, 30, 50))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        self.onGround=False
        self.frame = 0
        self.alt=position[1]

        self.right_states={ 0: (6, 52, 30, 50),
                           1: (49, 52, 30, 50),
                           2: (86, 52, 30, 50),
                           3: (123, 52, 35, 50),
                           4: (167, 52, 35, 50),
                           5: (215, 52, 30, 50)}
        self.left_states={ 0: (6, 52, 30, 50),
                           1: (49, 52, 30, 50),
                           2: (86, 52, 30, 50),
                           3: (123, 52, 35, 50),
                           4: (167, 52, 35, 50),
                           5: (215, 52, 30, 50)}
        self.upright_states={ 0: (16, 216, 32, 45),
                              1: (59, 216, 32, 45),
                              2: (103, 216, 32, 45),
                              3: (145, 216, 32, 45)}
        self.attackright_states={0: (24, 372, 43, 53),
                                 #1: (68, 372, 60, 53),
                                 #2: (132, 372, 60, 53),
                                 1: (195, 372, 60, 53),
                                 2: (255, 372, 60, 53)}
        
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect


    def update(self, up,right, left,attack):
        if attack:
            self.clip(self.attackright_states)
        if self.rect.y==self.alt-10:
            self.onGround=True
        if up:
            if self.onGround:
                self.yvel=-30
            else:
                pass
        if right and self.onGround:
            if not attack:
                self.clip(self.right_states)
            self.xvel= 5
            if attack:
                self.clip(self.attackright_states)
        if left and self.onGround:
            self.clip(self.left_states)
            self.xvel= -5
        if not self.onGround:
            
            self.yvel+=5

            if self.yvel<-4:
                self.clip(self.upright_states[0])
            elif self.yvel<4:
                self.clip(self.upright_states[1])
            elif self.yvel<12:
                self.clip(self.upright_states[2])
            elif self.yvel<20:
                self.clip(self.upright_states[3])
            if self.yvel>30:
                self.yvel=30
                
        if not (right or left):
            self.xvel=0
        if self.onGround and self.xvel==0 and not attack:
            self.clip(self.right_states[1])
        self.rect.x+=self.xvel
        self.rect.y+=self.yvel
        self.onGround=False
        if self.rect.y>=self.alt-10:
            self.onGround=True
            self.rect.y=self.alt-10

 
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        
    def handle_event(self,key):
        right=up=left=attack=False
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        if key[pygame.K_RIGHT]:
            right=True
        if key[pygame.K_UP]:
            up=True
        if key[pygame.K_LEFT]:
            left=True
        if key[pygame.K_k]:
            attack=True

        self.update(up,right,left,attack)
class Fondo(pygame.sprite.Sprite):
    def __init__(self,imagen,left,top):
        self.image = pygame.image.load(imagen)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    
    def mov(self,PJ,keys,time,fondo2):

        if PJ.rect.x >= width/2 and keys[K_RIGHT]:
            self.rect.left -= 0.5 * time
        if self.rect.left < 0 and keys[K_RIGHT] and PJ.rect.right == width/2:
            fondo2.rect.left = self.rect.right




def main():

    fondo='fondo1.png' 
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    player = PJ((0, height-60))
    fondo1=Fondo("fondo1.png",0,0)
    fondo2=Fondo("fondo2.png",width,0)
    fondo3=Fondo("fondo3.png",width*2,0)

    while True:
        
        time=clock.tick(60)
        key=pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit()
        if fondo1.rect.right>=0:
            fondo1.mov(player,key,time,fondo2)
        if fondo1.rect.right<=0:
            fondo1.rect.left=width*2

        if fondo2.rect.right>=0:
            fondo2.mov(player,key,time,fondo3)
        if fondo2.rect.right<=0:
            fondo2.rect.left=width*2

        if fondo3.rect.right>=0:
            fondo3.mov(player,key,time,fondo1)
        if fondo3.rect.right<=0:
            fondo3.rect.left=width*2    
        player.handle_event(key)

        background=pygame.image.load(fondo).convert()
        screen.blit(background,(0,0))
        screen.blit(fondo1.image,(fondo1.rect.left,fondo1.rect.top))
        screen.blit(fondo2.image,(fondo2.rect.left,fondo2.rect.top))
        screen.blit(fondo3.image,(fondo3.rect.left,fondo3.rect.top))
        screen.blit(player.image, player.rect)
     
        pygame.display.flip()
        clock.tick(15)
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
    pass

