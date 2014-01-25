import pygame, sys, random, math
from pygame.locals import *
largo=50
ancho=2075


#############################################################################

def rezize(image,resolution):
    return  pygame.transform.scale(pygame.image.load(image).convert(), resolution)

###############################################################################

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

############################################################################

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/v.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)
    def update(self):
        pass
    
#################################################################################################
      
class Fondo(pygame.sprite.Sprite):
    def __init__(self,imagen,left,top,resolution):
        self.image = rezize(imagen, resolution)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    
    def mov(self,PJ,keys,time,fondo2,resolution):

        if PJ.rect.x >= resolution[0]/2 and keys[K_RIGHT] and not PJ.choque:
            self.rect.left -= 0.5 * time
        if self.rect.left < 0 and keys[K_RIGHT] and PJ.rect.right == resolution[0]/2:
            fondo2.rect.left = self.rect.right

#############################################################################

class Camera(object):
    def __init__(self, camera_func, resolution):
        self.camera_func = camera_func
        self.state = Rect(0, 0, resolution[0], resolution[1])


    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target,resolution):
        self.state = self.camera_func(self.state, target.rect,resolution)

def simple_camera(camera, target_rect,resolution):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+resolution[0]/2, -t+resolution[1]/2, w, h)

def complex_camera(camera, target_rect,resolution):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+(resolution[0]/2), -t+resolution[1]/2, w, h


    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-ancho, l)   # stop scrolling at the right edge
    t = max(-(camera.height-resolution[1]), t) # stop scrolling at the bottom
    t = max(t, -largo)                           # stop scrolling at the top
    return Rect(l, t, w, h)

##################################################################################

class Burbuja(pygame.sprite.Sprite):
    def __init__(self, posx, posy, resolution):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Others/bb_1.png')
        self.rect =  Rect(posx, posy, 70, 66)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.vivo = True
        self.speed = 3
        self.proyectil = Proyectil(self)
        global burbuja
        burbuja=True
        
    def update(self, pj, time, platforms,oils,resolution):
        """Movimiento de Personaje y colisiones"""
        if self.vivo:
            #if self.rect.top <= 0:
            #    self.rect.top = 0
            #    self.speed *= -1 
            #if self.rect.bottom >= resolution[1]:
            #    self.rect.bottom = resolution[1]
            #    self.speed *= -1 
            r = random.randint(0,1)
            if r == 1 and self.proyectil.wait:
                self.proyectil.wait = False 
            vx, vy = self.velocidad(pj) 

            for p in platforms:
                if pygame.sprite.collide_rect(self, p):
                    self.speed *= -1
                    self.rect.centery += self.speed

            for o in oils:
                if pygame.sprite.collide_circle(self, o):
                    self.speed *= -1
                    self.rect.centery += self.speed
                    
            self.proyectil.update(pj, time, self, vx, vy, platforms, oils,resolution) 

            self.rect.centery += self.speed
            
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
                global burbuja
                burbuja=False
                print(burbuja)
    
    def velocidad(self, pj):
        x1 = pj.rect.centerx - self.rect.centerx
        y1 = pj.rect.centery - self.rect.centery
        norm = math.sqrt(x1**2 + y1**2)
        x2 = x1/norm
        y2 = y1/norm
        return x2, y2
    
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load('Images/Others/vacio.png')

#########################################################################
     
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,burbuja):
        pygame.sprite.Sprite.__init__(self)
        self.wait = True
        self.image = pygame.image.load('Images/Others/vacio.png')
        self.rect = Rect(burbuja.rect.centerx, burbuja.rect.centery, 30, 28)
        self.rect.centerx = burbuja.rect.centerx
        self.rect.centery = burbuja.rect.centery
        self.speed = 10
        
    def update(self, pj, time, burbuja, vx, vy,platforms,oils,resolution):
        if self.wait:
            self.rect.centery = burbuja.rect.centery
            self.rect.centerx = burbuja.rect.centerx
        if not self.wait:
            self.image = pygame.image.load('Images/Others/bb_p.png')
            self.rect.centerx += vx*self.speed
            self.rect.centery += vy*self.speed
            for p in platforms:
                if pygame.sprite.collide_rect(self, p):
                    self.desaparicion(burbuja)
            for o in oils:
                if pygame.sprite.collide_rect(self, o):
                    self.desaparicion(burbuja)
            if not burbuja.vivo or self.rect.left <= 0 or self.rect.top <= 0 or self.rect.bottom >= resolution[1]:
                self.desaparicion(burbuja)
    
    def desaparicion(self, burbuja):
        self.wait = True
        self.image = pygame.image.load("Images/Others/vacio.png")

###################################################################################
              
class Slime(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Others/slime.png')
        self.rect = Rect(posx, posy, 39, 34)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speed = 2
        self.vivo = True
        self.right = False
        self.left = True
    
    def update(self, pj, time,platforms,oils):
        if self.vivo:
            #if pj.rect.centerx - self.rect.centerx > 0:
            #    self.right = True
            #    self.left = False
            #if pj.rect.centerx - self.rect.centerx < 0:
            #    self.left = True
            #    self.right = False
            for p in platforms:
                if pygame.sprite.collide_rect(self,p):
                    self.speed *= -1
                    self.rect.centerx += self.speed
            for o in oils:
                if pygame.sprite.collide_rect(self, o):
                    self.speed *= -1
                    self.rect.centerx += self.speed
            self.rect.centerx += self.speed
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
    def muerte(self):
            self.vivo = False
            self.image = pygame.image.load('Images/Others/vacio.png')
        
####################################################################################
      
class PJ(Entity,pygame.sprite.Sprite):
    def __init__(self, position,sprites):
        Entity.__init__(self)
        self.sheet = pygame.image.load(sprites)
        self.sheet.set_clip(pygame.Rect(6, 52, 30, 50))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        global vivo
        vivo=True
        self.woman=False
        self.stick=False
        self.man=False
        self.onGround=False
        self.attacking = False
        self.frame = 0
        self.facel=False
        self.facer=True
        self.alt=position[1]
        self.atupright=False
        self.atupleft=False
        if sprites=='Images/Woman/1_1.png':
            self.woman=True
        elif sprites=='Images/Sticks/1_1.png':
            self.stick=True
        elif sprites=='Images/Man/1_1.png':
            self.man=True
################################### stick ######################################
        if self.stick:
            self.right_states={0: (6, 52, 30, 50),
                               1: (49, 52, 30, 50),
                               #2: (86, 52, 30, 50),
                               #3: (123, 52, 35, 50),
                               #4: (167, 52, 35, 50),
                               2: (215, 52, 30, 50)}
            self.left_states={ 0: (1175, 52, 30, 50),
                               1: (1136, 52, 30, 50),
                               #2: (1090, 52, 30, 50),
                               #3: (1045, 52, 35, 50),
                               #4: (1012, 52, 35, 50),
                               2: (978, 52, 30, 50)}
            self.upright_states={ 0: (16, 216, 32, 45),
                                  1: (59, 216, 32, 45),
                                  2: (103, 216, 32, 45),
                                  3: (145, 216, 32, 45)}
            self.upleft_states={  0: (1245, 216, 32, 45),
                                  1: (1200, 216, 32, 45),
                                  2: (1157, 216, 32, 45),
                                  3: (1119, 216, 32, 45)}
            self.attackright_states={0: (24, 372, 43, 53),
                                     #1: (68, 372, 60, 53),2: (132, 372, 60, 53),
                                     1: (195, 372, 60, 53),
                                     2: (255, 372, 60, 53)}
            self.attackleft_states={0: (1223, 372, 43, 53),
                                     #1: (1160, 372, 60, 53),2: (1100, 372, 60, 53),
                                     1: (1040, 372, 60, 53),
                                     2: (984, 372, 60, 53)}
            self.atupright_states={0:(2,485,60,53),
                                   1:(72,485,60,53),
                                   2:(130,485,60,53),
                                   3:(180,485,32,53),
                                   4:(222,485,57,53)}
            self.atupleft_states={0:(1232,485,57,53),
                                   1:(1157,485,60,53),
                                   2:(1063,485,57,53),
                                   3:(1020,485,32,53),
                                   4:(1002,485,57,53)}
################################# woman ########################################
        elif self.woman:
            self.left_states={ 5:(518,203,39,60),
                               4:(553,203,39,60),
                               3:(587,203,39,60),
                               2:(624,203,39,60),
                               1:(660,203,37,60),
                               0:(691,203,39,60)}
            self.right_states={0:(724,203,39,60),
                               1:(758,203,37,60),
                               2:(790,203,39,60),
                               #3:(827,203,39,60),
                               3:(863,203,39,60)}
                               #3:(900,203,39,60)}
            self.upleft_states={10:(274,452,39,60),
                               9:(320,452,39,60),
                               8:(362,452,39,60),
                               7:(410,452,39,60),
                               6:(454,452,37,60),
                               5:(492,452,39,60),
                               4:(534,452,39,60),
                               3:(570,452,39,60),
                               2:(602,452,39,60),
                               1:(640,452,39,60),
                               0:(683,452,39,60)}
            self.upright_states={0:(728,452,39,60),
                               1:(770,452,39,60),
                               2:(810,452,39,60),
                               3:(849,452,39,60),
                               4:(882,452,37,60),
                               5:(920,452,39,60),
                               6:(962,452,39,60),
                               7:(1003,452,39,60),
                               8:(1048,452,39,60),
                               9:(1093,452,39,60),
                               10:(1135,452,39,60)}
            self.attackleft_states={#0:(305,586,39,60),1:(350,586,39,60),2:(393,586,39,60),3:(430,586,39,60),4:(470,586,39,60),
                               3:(510,586,50,60),
                               4:(510,586,50,60),
                               #6:(565,586,45,60),
                               2:(611,586,39,60),
                               1:(653,586,39,60),
                               0:(690,586,39,60)}
            self.attackright_states={0:(725,586,39,60),
                               1:(763,586,39,60),
                               2:(763,586,39,60),
                               #3:(803,586,39,60),4:(847,586,39,60),
                               3:(895,586,50,60),
                               4:(895,586,50,60)}
                               #6:(945,586,45,60),7:(985,586,39,60),8:(653,586,39,60),9:(1025,586,39,60)}
            self.atupleft_states={7:(348,522,39,60),
                               6:(394,522,39,60),
                               5:(436,522,39,60),
                               4:(480,522,39,60),
                               3:(524,522,49,60),
                               2:(581,522,45,60),
                               1:(635,522,45,60),
                               0:(685,522,39,60)}
            self.atupright_states={0:(732,522,39,60),
                               1:(777,522,40,60),
                               2:(830,522,45,60),
                               3:(880,522,49,60),
                               4:(933,522,39,60),
                               5:(980,522,39,60),
                               6:(1023,522,39,60),
                               7:(1067,522,39,60)}
            
####################################   man  #######################################
        elif self.man:
            self.left_states={ 5:(890,95,33,40),
                               4:(922,95,34,40),
                               3:(956,95,29,40),
                               2:(983,95,34,40),
                               1:(1015,95,30,40),
                               0:(1045,95,34,40)}
            self.right_states={0:(0,95,34,40),
                               1:(34,95,31,40),
                               2:(63,95,34,40),
                               3:(96,95,28,40),
                               4:(123,95,34,40),
                               5:(157,95,34,40)}
            self.upleft_states={3:(696,203,36,40),
                               2:(730,203,40,40),
                               1:(771,203,34,40),
                               0:(810,203,34,40)}
            self.upright_states={0:(235,203,37,41),
                               1:(272,203,37,41),
                               2:(312,203,37,41),
                               3:(352,203,37,41)}
            self.attackleft_states={0:(725,544,37,41),
                                    1:(686,544,37,41),
                                    2:(640,544,37,41)}
            self.attackright_states={0:(318,544,37,41),
                               1:(356,544,37,41),
                               2:(402,544,37,41)}
            self.atupleft_states={0:(1020,1163,41,46),
                               1:(979,1163,41,46),
                               2:(933,1163,41,46),
                               3:(890,1163,41,46),
                               4:(846,1163,35,46),
                               5:(808,1163,35,46),
                               6:(770,1163,41,46)}
            self.atupright_states={0:(19,1163,41,46),
                               1:(61,1163,41,46),
                               2:(107,1163,41,46),
                               3:(153,1163,41,46),
                               4:(200,1163,35,46),
                               5:(235,1163,35,46),
                               6:(270,1163,41,46)}
                
###################################################################################            
        
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


    def update(self,up,right,left,attack,platforms):
################################################################################
############################attack sin mas botones##############################
        if attack:
            if self.facer:
                self.clip(self.attackright_states)
            if self.facel:
                self.clip(self.attackleft_states)
            self.attacking = True
            if not self.onGround:
                if right or self.facer:
                    self.atupright=True
                if left or self.facel:
                    self.atupleft=True
################################################################################
########################### gravedad inicio salto#############################

        if up:
            if self.onGround:
                self.yvel=-30
            if attack and not self.onGround:
                if right or self.facer:
                    self.atupright=True
                if left or self.facel:
                    self.atupleft=True
################################################################################
############################## right/left on ground##############################                
        if right and self.onGround:
            self.facer=True
            self.facel=False
            if not attack:
                self.clip(self.right_states)
            self.xvel= 8
            if attack:
                if self.onGround:
                    self.clip(self.attackright_states)
                if up:
                    self.atupright=True
        if left and self.onGround:
            self.facer=False
            self.facel=True
            if not attack:
                self.clip(self.left_states)
            self.xvel= -8
            if attack:
                if self.onGround:
                    self.clip(self.attackleft_states)
                if up:
                    self.atupleft=True
                    
################################################################################
################################################################################
        if not self.onGround:
            self.yvel+=5
            if self.woman and not attack:
                if self.facer:
                    if self.yvel<-4:
                        self.clip(self.upright_states[0])
                    elif self.yvel<-1:
                        self.clip(self.upright_states[1])
                    elif self.yvel<2:
                        self.clip(self.upright_states[2])
                    elif self.yvel<4:
                        self.clip(self.upright_states[3])
                    elif self.yvel<7:
                        self.clip(self.upright_states[4])
                    elif self.yvel<10:
                        self.clip(self.upright_states[5])
                    elif self.yvel<12:
                        self.clip(self.upright_states[6])
                    elif self.yvel<13:
                        self.clip(self.upright_states[7])
                    elif self.yvel<20:
                        self.clip(self.upright_states[7])
                    elif self.yvel<23:
                        self.clip(self.upright_states[8])
                    if self.yvel>30:
                        self.clip(self.upright_states[10])
                        self.yvel=30
                if self.facel:
                    if self.yvel<-4:
                        self.clip(self.upleft_states[0])
                    elif self.yvel<-1:
                        self.clip(self.upleft_states[1])
                    elif self.yvel<2:
                        self.clip(self.upleft_states[2])
                    elif self.yvel<4:
                        self.clip(self.upleft_states[3])
                    elif self.yvel<7:
                        self.clip(self.upleft_states[4])
                    elif self.yvel<10:
                        self.clip(self.upleft_states[5])
                    elif self.yvel<12:
                        self.clip(self.upleft_states[6])
                    elif self.yvel<13:
                        self.clip(self.upleft_states[7])
                    elif self.yvel<20:
                        self.clip(self.upleft_states[7])
                    elif self.yvel<23:
                        self.clip(self.upleft_states[8])
                    if self.yvel>30:
                        self.clip(self.upleft_states[10])
                        self.yvel=30
            if self.stick and not attack:
                if self.facer:
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
                if self.facel:
                    if self.yvel<-4:
                        self.clip(self.upleft_states[0])
                    elif self.yvel<4:
                        self.clip(self.upleft_states[1])
                    elif self.yvel<12:
                        self.clip(self.upleft_states[2])
                    elif self.yvel<20:
                        self.clip(self.upleft_states[3])
                    if self.yvel>30:
                        self.yvel=30
            if self.man and not attack:
                if self.facer:
                    if self.yvel<-15:
                        self.clip(self.upright_states[0])
                    elif self.yvel<10:
                        self.clip(self.upright_states[1])
                    elif self.yvel<25:
                        self.clip(self.upright_states[2])
                    elif self.yvel<30:
                        self.clip(self.upright_states[3])
                    if self.yvel>30:
                        self.yvel=30
                if self.facel:
                    if self.yvel<-15:
                        self.clip(self.upleft_states[0])
                    elif self.yvel<10:
                        self.clip(self.upleft_states[1])
                    elif self.yvel<25:
                        self.clip(self.upleft_states[2])
                    elif self.yvel<30:
                        self.clip(self.upleft_states[3])
                    if self.yvel>30:
                        self.yvel=30
                    if self.yvel>30:
                        self.yvel=30
############################# atup man ###################################
        if self.man:
            if self.atupright:
                if self.yvel<-20:
                    self.clip(self.atupright_states[0])
                elif self.yvel<-10:
                    self.clip(self.atupright_states[1])
                elif self.yvel<0:
                    self.clip(self.atupright_states[2])
                elif self.yvel<5:
                    self.clip(self.atupright_states[3])
                elif self.yvel<15:
                    self.clip(self.atupright_states[4])
                elif self.yvel<20:
                    self.clip(self.atupright_states[5])
                elif self.yvel<30:
                    self.clip(self.atupright_states[6])
            if self.atupleft:
                if self.yvel<-20:
                    self.clip(self.atupleft_states[0])
                elif self.yvel<-10:
                    self.clip(self.atupleft_states[1])
                elif self.yvel<0:
                    self.clip(self.atupleft_states[2])
                elif self.yvel<5:
                    self.clip(self.atupleft_states[3])
                elif self.yvel<15:
                    self.clip(self.atupleft_states[4])
                elif self.yvel<20:
                    self.clip(self.atupleft_states[5])
                elif self.yvel<30:
                    self.clip(self.atupleft_states[6])
############################## atup stick ###############################
        if self.stick:
            if self.atupright:
                if self.yvel<-10:
                    self.clip(self.atupright_states[0])
                elif self.yvel<5:
                    self.clip(self.atupright_states[1])
                elif self.yvel<15:
                    self.clip(self.atupright_states[2])
                elif self.yvel<20:
                    self.clip(self.atupright_states[3])
                elif self.yvel<30:
                    self.clip(self.atupright_states[4])

            if self.atupleft:
                if self.yvel<-10:
                    self.clip(self.atupleft_states[0])
                elif self.yvel<5:
                    self.clip(self.atupleft_states[1])
                elif self.yvel<15:
                    self.clip(self.atupleft_states[2])
                elif self.yvel<20:
                    self.clip(self.atupleft_states[3])
                elif self.yvel<30:
                    self.clip(self.atupleft_states[4])
############################## atup woman ##############################
        if self.woman:
            if self.atupright:
                if self.yvel<-20:
                    self.clip(self.atupright_states[0])
                elif self.yvel<-10:
                    self.clip(self.atupright_states[1])
                elif self.yvel<0:
                    self.clip(self.atupright_states[2])
                elif self.yvel<5:
                    self.clip(self.atupright_states[3])
                elif self.yvel<15:
                    self.clip(self.atupright_states[4])
                elif self.yvel<20:
                    self.clip(self.atupright_states[5])
                elif self.yvel<25:
                    self.clip(self.atupright_states[6])
                elif self.yvel<30:
                    self.clip(self.atupright_states[7])
            if self.atupleft:
                if self.yvel<-20:
                    self.clip(self.atupleft_states[0])
                elif self.yvel<-10:
                    self.clip(self.atupleft_states[1])
                elif self.yvel<0:
                    self.clip(self.atupleft_states[2])
                elif self.yvel<5:
                    self.clip(self.atupleft_states[3])
                elif self.yvel<15:
                    self.clip(self.atupleft_states[4])
                elif self.yvel<20:
                    self.clip(self.atupleft_states[5])
                elif self.yvel<30:
                    self.clip(self.atupleft_states[6])
                elif self.yvel<30:
                    self.clip(self.atupleft_states[7])
#########################################################################
        if not (right or left):
            self.xvel=0
        if self.onGround and self.xvel==0 and not attack:
            if self.facer:
                self.clip(self.right_states[0])
            elif self.facel:
                self.clip(self.left_states[0])

        self.rect.x+=self.xvel
        self.collide(self.xvel,0,platforms,attack)
        self.rect.y+=self.yvel
        self.onGround=False
        self.atupright=False
        self.atupleft=False
        self.collide(0, self.yvel , platforms,attack)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
    def muerte_proyectil(self, enemigo):
        if pygame.sprite.collide_rect(self, enemigo.proyectil):
            global vivo
            vivo = False
            self.image = pygame.image.load("Images/Others/vacio.png")
    
    def muerte_toque(self, enemigo):
        if pygame.sprite.collide_rect(self, enemigo):
            global vivo
            vivo = False
            self.image = pygame.image.load("Images/Others/vacio.png")
            
    def muerte_oil(self, oils):
        for o in oils:
            if pygame.sprite.collide_rect(self, o):
                global vivo
                vivo = False
                self.image = pygame.image.load("Images/Others/vacio.png")
    def muerte_water(self, wat):
        for w in wat:
            if pygame.sprite.collide_rect(self, w):
                global vivo
                vivo = False
                self.image = pygame.image.load("Images/Others/vacio.png")

    def collide(self, xvel, yvel, platforms,attack):      
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Platform) and not attack:
                    if self.facer:
                        self.clip(self.right_states[0])
                    elif self.facel:
                        self.clip(self.left_states[0])
                    self.choque=True
                elif isinstance(p, Platform) and attack:
                    if self.facer:
                        self.clip(self.attackright_states[0])
                    elif self.facel:
                        self.clip(self.attackleft_states[0])
                    self.choque=True
                if isinstance(p, Water) and not attack:
                    if self.facer:
                        self.clip(self.right_states[0])
                    elif self.facel:
                        self.clip(self.left_states[0])
                elif isinstance(p, Water) and attack:
                    if self.facer:
                        self.clip(self.attackright_states[0])
                    elif self.facel:
                        self.clip(self.attackleft_states[0])
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                        self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround=True
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

#############################################################################
    
class Oil(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/oil.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

    def update(self):
        pass
    
#############################################################################
    
class Valdosa(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/v.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

    def update(self):
        pass
    
#############################################################################
    
class Water(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/w.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

    def update(self):
        pass

#################################################################################
    
def velocidad(pj, burbuja):
    x1 = pj.rect.centerx - burbuja.rect.centerx
    y1 = pj.rect.centery - burbuja.rect.centery
    norm = math.sqrt(x1**2 + y1**2)
    x2 = x1/norm
    y2 = y1/norm
    return x2, y2

#####################################################################   
score=2000
def main(resolution,sprites):
    global score
    fondo='Images/Others/fondo1.png' 
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    fondo1=Fondo('Images/Others/fondo1.png',0,0,resolution)
    fondo2=Fondo('Images/Others/fondo2.png',fondo1.rect.right,0,resolution)
    fondo3=Fondo('Images/Others/fondo3.png',fondo2.rect.right,0,resolution)
    
    x=y=0
    f= file("Maps/1_1.txt")
    level = f.readlines()
    platforms=[]
    burbujas = []
    slimes = []
    oils = []
    val=[]
    wat=[]
    
    entities=pygame.sprite.Group()
    for row in level:
        for col in row:
            if col =="p":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col =="b":
                b = Burbuja(x,y,resolution)
                burbujas.append(b)
                entities.add(b)
                entities.add(b.proyectil)
            if col =="s":
                s = Slime(x,y)
                slimes.append(s)
                entities.add(s)
            if col == "o":
                o = Oil(x,y)
                oils.append(o)
                entities.add(o)
            if col == "w":
                w = Water(x,y)
                wat.append(w)
                entities.add(w)
            if col == "v":
                v = Valdosa(x,y)
                val.append(v)
                entities.add(v)
            if col == "1":
                player = PJ((x,y),sprites)
                
            x += 18
        y += 18
        x = 0
    total_level_width  = len(level[0])*35
    total_level_height = len(level)*35
    camera = Camera(complex_camera, (total_level_width, total_level_height))
    entities.add(player)


    while True:
        
        time=clock.tick(30)
        key=pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if fondo1.rect.right>=0:
            fondo1.mov(player,key,time,fondo2,resolution)
        if fondo1.rect.right<=0:
            fondo1.rect.left=fondo3.rect.right

        if fondo2.rect.right>=0:
            fondo2.mov(player,key,time,fondo3,resolution)
        if fondo2.rect.right<=0:
            fondo2.rect.left=fondo1.rect.right

        if fondo3.rect.right>=0:
            fondo3.mov(player,key,time,fondo1,resolution)
        if fondo3.rect.right<=0:
            fondo3.rect.left=fondo2.rect.right

        for b in burbujas:
            b.update(player, time, platforms, oils,resolution)
            player.muerte_proyectil(b)
            player.muerte_toque(b)
        for s in slimes:
            s.update(player, time, platforms, oils)
            player.muerte_toque(s)
            if s.vivo==False:
                slimes.remove(s)
                score+=250
                
        score-=1    
        player.attacking = False
        player.muerte_oil(oils)
        player.muerte_water(wat)
        
        player.handle_event(key,platforms)
        camera.update(player,resolution)
        background=pygame.image.load(fondo).convert()
        screen.blit(background,(0,0))
        screen.blit(fondo1.image,(fondo1.rect.left,fondo1.rect.top))
        screen.blit(fondo2.image,(fondo2.rect.left,fondo2.rect.top))
        screen.blit(fondo3.image,(fondo3.rect.left,fondo3.rect.top))

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        if vivo==False:
            pass
        if burbuja==False:
            return True
        
        
        
        myfont = pygame.font.SysFont("monospace", 20, bold=True)
        label = myfont.render("Score:"+str(score), 1, (0,0,0))
        screen.blit(label, (380, 10))
        pygame.display.flip()

        
    return 0
