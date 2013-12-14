import pygame, sys, random, math
from pygame.locals import *

class Burbuja(pygame.sprite.Sprite):
    def __init__(self, posx, posy, resolution):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Others/bb_1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.vivo = True
        self.speed = 0.3
        
    def update(self, pj, time, proyectil,resolution):
        if self.vivo:
            if self.rect.top <= 0:
                self.rect.top = 0
                self.speed *= -1 
            if self.rect.bottom >= resolution[1]:
                self.rect.bottom = resolution[1]
                self.speed *= -1 
            self.rect.centery += self.speed*time
            
            r = random.randint(0,1)
            if r == 1 and proyectil.wait:
                proyectil.wait = False 
             
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
                
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load('Images/Others/vacio.png')
     
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,burbuja):
        pygame.sprite.Sprite.__init__(self)
        self.wait = True
        self.image = pygame.image.load('Images/Others/vacio.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = burbuja.rect.centerx
        self.rect.centery = burbuja.rect.centery
        self.speed = 1
        
    def update(self, pj, time, burbuja, vx, vy,resolution):
        if self.wait:
            self.rect.centery = burbuja.rect.centery
        if not self.wait:
            self.image = pygame.image.load('Images/Others/bb_p.png')
            self.rect.centerx += vx*self.speed*time
            self.rect.centery += vy*self.speed*time
            if self.rect.top <= 0 or self.rect.bottom >= resolution[1] or self.rect.left <= 0 or self.rect.right >= resolution[0]:
                self.desaparicion(burbuja)
            if not burbuja.vivo:
                self.desaparicion(burbuja)
            
    
    def desaparicion(self, burbuja):
        self.wait = True
        self.image = pygame.image.load("Images/Others/vacio.png")
        self.rect.centery = burbuja.rect.centery
        self.rect.centerx = burbuja.rect.centerx
              
class Slime(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Others/slime.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speed = 0.1
        self.vivo = True
        self.right = False
        self.left = False
    
    def update(self, pj, time):
        if self.vivo:
            if pj.rect.centerx - self.rect.centerx > 0:
                self.right = True
                self.left = False
            if pj.rect.centerx - self.rect.centerx < 0:
                self.left = True
                self.right = False
            if self.left:
                self.rect.centerx -= self.speed*time
            if self.right:
                self.rect.centerx += self.speed*time
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
            
    
    def muerte(self):
            self.vivo = False
            self.image = pygame.image.load('Images/Others/vacio.png')
        
##################################################
      
class PJ(pygame.sprite.Sprite):
    def __init__(self, position,sprites):
        self.sheet = pygame.image.load(sprites)
        self.sheet.set_clip(pygame.Rect(6, 52, 30, 50))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        self.vivo = True
        self.onGround=False
        self.attacking = False
        self.frame = 0
        self.alt=position[1]
        self.x = 0

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
            self.attacking = True
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

    def muerte(self, proyectil, enemigo):
        if (pygame.sprite.collide_rect(self, enemigo) and self.vivo and not self.attacking) or ((pygame.sprite.collide_rect(self, proyectil) and self.vivo and not proyectil.wait)): 
            self.vivo = False
            self.image = pygame.image.load('Images/Others/vacio.png')

        
        
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
    def __init__(self,imagen,left,top,resolution):
        self.image = pygame.transform.scale(pygame.image.load(imagen).convert(), resolution)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    
    def mov(self,PJ,keys,time,fondo2,resolution):

        if PJ.rect.x >= resolution[0]/2 and keys[K_RIGHT]:
            self.rect.left -= 0.5 * time
        if self.rect.left < 0 and keys[K_RIGHT] and PJ.rect.right == resolution[0]/2:
            fondo2.rect.left = self.rect.right

def velocidad(pj, burbuja):
    x1 = pj.rect.centerx - burbuja.rect.centerx
    y1 = pj.rect.centery - burbuja.rect.centery
    norm = math.sqrt(x1**2 + y1**2)
    x2 = x1/norm
    y2 = y1/norm
    return x2, y2

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("Images/Others/times.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
    

def main(resolution,sprites):

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    player = PJ((0, resolution[1]-60), sprites)
    fondo1=Fondo("Images/Others/fondo1.png",0,0,resolution)
    fondo2=Fondo("Images/Others/fondo2.png",resolution[0],0,resolution)
    fondo3=Fondo("Images/Others/fondo3.png",resolution[0]*2,0,resolution)
    posx, posx_rect = texto(str(player.rect.centerx), resolution[0]/2, resolution[1]/2,[0,0,0])
    slime = Slime(resolution[0]/2, resolution[1]-30)
    burbuja = Burbuja(resolution[0]*2/3, resolution[1]/2,resolution)
    proyectil = Proyectil(burbuja)
    vx = vy = 0
    
    while player.vivo:
        
        time=clock.tick(60)
        key=pygame.key.get_pressed()
        posx, posx_rect = texto(str(player.rect.centerx), resolution[0]/2, resolution[1]/2,[0,0,0])
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if fondo1.rect.right>=0:
            fondo1.mov(player,key,time,fondo2,resolution)
        if fondo1.rect.right<=0:
            fondo1.rect.left=resolution[0]*2

        if fondo2.rect.right>=0:
            fondo2.mov(player,key,time,fondo3,resolution)
        if fondo2.rect.right<=0:
            fondo2.rect.left=resolution[0]*2

        if fondo3.rect.right>=0:
            fondo3.mov(player,key,time,fondo1,resolution)
        if fondo3.rect.right<=0:
            fondo3.rect.left=resolution[0]*2
        
        if player.vivo:    
            player.handle_event(key)
        if slime.vivo:
            slime.update(player, time)
            player.muerte(proyectil, slime)
        if burbuja.vivo:  
            if proyectil.wait:
                vx, vy = velocidad(player, burbuja)
            burbuja.update(player, time, proyectil,resolution)
            proyectil.update(player, time, burbuja, vx, vy,resolution)
            player.muerte(proyectil, burbuja)
        player.attacking = False
        
        screen.blit(fondo1.image,(fondo1.rect.left,fondo1.rect.top))
        screen.blit(fondo2.image,(fondo2.rect.left,fondo2.rect.top))
        screen.blit(fondo3.image,(fondo3.rect.left,fondo3.rect.top))
        screen.blit(slime.image, slime.rect)
        screen.blit(burbuja.image, burbuja.rect)
        screen.blit(proyectil.image, proyectil.rect)
        screen.blit(player.image, player.rect)
        screen.blit(posx, posx_rect)
        pygame.display.flip()
        clock.tick(10)
    
    else:
        gg, gg_rect = texto("GAMEOVER", resolution[0]/2, resolution[1]/2, [0,0,0])
        screen.fill([200,200,200])
        screen.blit(gg, gg_rect)
        while True:
            pygame.display.flip()
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        
    return 0


