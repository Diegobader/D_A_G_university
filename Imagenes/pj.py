import pygame
up=False
left=False
face_l=0
face_r=1
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Pj(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.sheet=pygame.image.load('stk_and_soap_mace.png')
        self.sheet.set_clip(pygame.Rect(0,30,56,70))
        self.image=self.sheet.subsurface(self.sheet.get_clip())
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)

        self.xvel=0
        self.yvel=0
        self.isjump=False


        self.frame=0
        self.left={ 0: (6, 52, 30, 50),
                    1: (49, 52, 30, 50),
                    2: (86, 52, 30, 50),
                    3: (123, 52, 35, 50),
                    4: (167, 52, 35, 50),
                    5: (215, 52, 30, 50)}
        self.upleft={ 0: (16, 216, 32, 45),
                     1: (59, 216, 32, 45),
                     2: (103, 216, 32, 45),
                     3: (145, 216, 32, 45)}

    def get_frame(self,frame_set):
        self.frame+=1
        if self.frame>(len(frame_set)-1):
            self.frame=0
        return frame_set[self.frame]
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    def update(self, up, left):
        global face_l
        global face_r
        if up:
            #saltando
            if self.isjump:
                self.yvel = -16
            else:
                pass
        #izq y no saltar
        if left and not self.isjump:
            animation = self.clip(self.left)
            face_l=1
            face_r=0
            self.xvel = -5
        # bajar del salto
        if self.isjump:
            #only accelerate wit gravity if in the air
            self.yvel +=3
            #max falling sapeed
            if self.yvel > 30:
                self.yvel = 30
        #saltar
        if self.yvel!=0 and self.isjump:
            
           # if right:
            #    animation = self.clip(self.jump_right_states)
             #   face_l=0
              #  face_r=1
               # self.xvel = 5
               
        #saltar izq  
            if left:
                animation = self.clip(self.upleft)
                face_l=1
                face_r=0
                self.xvel = -5
        #a dnd ver luego del salto
        if self.yvel!=0 and not self.isjump and self.xvel==0:
                if face_l==1:
                    animation = self.clip(self.upleft[0])
                #elif face_r==1:
                 #   animation = self.clip(self.jump_sright_states[0])
        elif not (left): #or right):
            if face_l==1:
                animation = self.clip(self.left[0])
            #elif face_r==1:
             #   animation = self.clip(self.right_states[0])
            self.xvel = 0

        # increment in x direction
        self.rect.left+= self.xvel
        # increment in y direction
        self.rect.top +=self.yvel
        # assuming we're in the air
        self.isjump = True
        
screen=pygame.display.set_mode((388,200))
        
while 1:
    pygame.init()
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            up = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            left = True

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            up = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            left = False
       
    player=Pj(20,20)
    player.update(up,left) 
    clock=pygame.time.Clock()
    background=pygame.image.load('fondo1.png').convert()
    screen.blit(background,(0,0))
    screen.blit(player.image, player.rect)

 
    pygame.display.flip()              
    clock.tick(10)
    

