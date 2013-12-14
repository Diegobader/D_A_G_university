import pygame
import pygame, sys
from pygame.locals import *
width=640
height=420
WIN_WIDTH = width
WIN_HEIGHT = height
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)   

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

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("dirt.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)
    def update(self):
        pass

class PJ(Entity):
    def __init__(self, position):
        Entity.__init__(self)
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


    def update(self, up,right, left,attack,platforms):
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
        self.collide(self.xvel, 0 , platforms)
        self.collide(0, self.yvel , platforms)

 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    def reset(self,x,y):
        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y)
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Platform):
                    self.clip(self.right_states[0])
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
        
    def handle_event(self,key,platforms):
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

        self.update(up,right,left,attack,platforms)

def main():

    fondo='fondo1.png' 
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fondo1=Fondo("fondo1.png",0,0)
    fondo2=Fondo("fondo2.png",width,0)
    fondo3=Fondo("fondo3.png",width*2,0)
    
    x=y=0
    level= [
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "p                                                              p",
    "                                                                                                              W",
    "                              p                                                                                W",
    "                           p     p                                                                             W",
    "                   ppppp            p                  p                                                       W",
    "          pppppp                                                                                                     W",
    "      "
    "          "
    "            "
    "pppppppppp        ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
    "ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp"
    ]
    platforms=[]
    
    entities=pygame.sprite.Group()
    for row in level:
        for col in row:
            if col =="p":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            x += 18
        y += 18
        x = 0
    player=PJ((0,height-60))
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)


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

        player.handle_event(key,platforms)
        camera.update(player)
        background=pygame.image.load(fondo).convert()
        screen.blit(background,(0,0))
        #screen.blit(fondo1.image,(fondo1.rect.left,fondo1.rect.top))
        #screen.blit(fondo2.image,(fondo2.rect.left,fondo2.rect.top))
        #screen.blit(fondo3.image,(fondo3.rect.left,fondo3.rect.top))
        screen.blit(player.image, player.rect)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
     
        pygame.display.flip()
        clock.tick(15)
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
    pass

