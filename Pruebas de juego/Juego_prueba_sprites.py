import pygame, sys
import math
from pygame import *

WIN_WIDTH = 400
WIN_HEIGHT = 300
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
FLAGS = 0
Resolution = 32
face_l=0
face_r=1
v=1
stk_sprites='Imagenes/stk_and_soap_mace.png'
def game():
    pygame.init()
    screen = display.set_mode(DISPLAY, FLAGS, Resolution)
    display.set_caption("Vidas: 3 ")
    timer = time.Clock()

    up = down = left = right = False
    bg=Surface((DISPLAY))
    bg.convert()
    bg.fill(Color("white"))
    entities = pygame.sprite.Group()
    stk = Stk(20,20)
    platforms = []

    x = y = 0
    level = [
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                              P",
    "W                                                                                                              W",
    "W                             p                                                                                W",
    "W                          p     p                                                                             W",
    "D                  ppppp            p                  X                                                       W",
    "                                                                                                               W",
    "GGGGGGGGGGGGGGGGGGGGGLLLLLLLLLLLLLLGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    ]

    #builds the level
    for row in level:
        for col in row:
            if col =="p":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col =="D":
                D = Door(x, y)
                platforms.append(D)
                entities.add(D)
            if col =="G":
                G = Ground(x, y)
                platforms.append(G)
                entities.add(G)
            if col =="W":
                W = Wall(x, y)
                platforms.append(W)
                entities.add(W)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if col == "X":
                X = LevelBlock(x, y)
                platforms.append(X)
                entities.add(X)
            if col == "L":
                Death = LavaBlock(x, y)
                platforms.append(Death)
                entities.add(Death)
            if col == "P":
                P = Border(x, y)
                platforms.append(P)
                entities.add(P)
            if col == "T":
                T = Dirt(x, y)
                platforms.append(T)
                entities.add(T)
            x += 18
        y += 18
        x = 0
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(stk)

    while 1:
        timer.tick(3)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
                #raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                #raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True


            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        #draw bg
        for y in range(18):
            for x in range(18):
                screen.blit(bg, (x * 18, y * 18))
        camera.update(stk)

        #update player, draw everything else
        stk.update(up, down, left, right, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.flip()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Stk(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.sheet = pygame.image.load(stk_sprites)
        self.sheet.set_clip(pygame.Rect((252,4), (32,41 )))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = ( x, y)
        self.frame = 0
        res = self.reset(50, 300)
        self.ghost_face ={0: (0,0, 30, 40)}
        self.left_states = { 0: (0, 0, 28, 41),
                             1: (225, 5, 27, 41),
                             2: (192, 5, 32, 41),
                             3: (141, 5, 24, 41),
                             4: (107, 5, 31, 41),
                             5: (79, 5, 27, 0 ) }
        self.right_states = { 0: (5, 52, 31, 55),
                             1: (46, 52, 31, 55),
                             2: (83, 52, 31, 55),
                             3: (119, 52, 31, 55),
                             4: (162, 52, 31, 55),
                             5: (211, 52, 31, 55 ),
                             6: (248, 52, 31, 55),
                             7: (282, 52, 31, 55)}
        self.up_states = { 0: (284, 81, 29, 43),
                           1: (312, 81, 29, 43),
                           2: (225, 81, 29, 43) }
        self.down_states = { 0: (252, 81, 29, 43),
                             1: (225, 81, 29, 43),
                             2: (312, 81, 29, 43) }
        self.jump_sright_states = { 0:(282, 48, 29, 37)}
        self.jump_sleft_states = {0: (249, 52, 27,29)}
        self.jump_left_states = { 0: (206, 47, 36, 34)}
        self.jump_right_states = { 0: (318 ,48, 36, 34)}

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
    def reset(self,x,y):
        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y)

    def update(self, up, down, left, right, platforms):
        global face_l
        global face_r
        if up:
            #only jump if on the ground
            if self.onGround:
                self.yvel = -16
            else:
                pass
        if down:
            animation = self.clip(self.down_states)
            pass
        if left and self.onGround:
            animation = self.clip(self.left_states)
            face_l=1
            face_r=0
            self.xvel = -5
        if right and self.onGround:
            animation = self.clip(self.right_states)
            face_l=0
            face_r=1
            self.xvel = 5
        if not self.onGround:
            #only accelerate wit gravity if in the air
            self.yvel +=3
            #max falling sapeed
            if self.yvel > 30:
                self.yvel = 30
        if self.yvel!=0 and self.onGround:
            if right:
                animation = self.clip(self.jump_right_states)
                face_l=0
                face_r=1
                self.xvel = 5
            elif left:
                animation = self.clip(self.jump_left_states)
                face_l=1
                face_r=0
                self.xvel = -5
        if self.yvel!=0 and not self.onGround and self.xvel==0:
                if face_l==1:
                    animation = self.clip(self.jump_sleft_states[0])
                elif face_r==1:
                    animation = self.clip(self.jump_sright_states[0])
        elif not (left or right):
            if face_l==1:
                animation = self.clip(self.left_states[0])
            elif face_r==1:
                animation = self.clip(self.right_states[0])
            self.xvel = 0

        # increment in x direction
        self.rect.left+= self.xvel
        # x-axis collisions
        self.collide(self.xvel, 0 , platforms)
        # increment in y direction
        self.rect.top +=self.yvel
        # assuming we're in the air
        self.onGround = False;
        # y-axis collisions
        self.collide(0, self.yvel, platforms)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    def collide(self, xvel, yvel, platforms):
        global animation
        global v
        global arthur_sprites
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, Ground):
                    if face_l==1:
                        animation = self.clip(self.left_states[0])
                    elif face_r==1:
                        animation = self.clip(self.right_states[0])
                if isinstance(p, Dirt):
                    if face_l==1:
                        animation = self.clip(self.left_states[0])
                    elif face_r==1:
                        animation = self.clip(self.right_states[0])
                if isinstance(p, Platform):
                    if face_l==1:
                        animation = self.clip(self.left_states[0])
                    elif face_r==1:
                        animation = self.clip(self.right_states[0])
                if isinstance(p, ExitBlock):
                    event.post(event.Event(QUIT))
                elif isinstance(p, Door):
                    event.post(event.Event(QUIT))
                elif isinstance(p, LavaBlock):
                    v=v-1
                    display.set_caption("Vidas: "+str(v))
                    if v==0:
                        arthur_sprites='Imagenes/ghost_face.png'                        
                    self.rect.x=50
                    self.rect.y=300
                elif isinstance(p, LevelBlock):
                    display.set_caption("Pasaste de nivel!!")
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                        self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                   # Player.rect.top =  Player.rect.top
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
        self.image = pygame.image.load("Imagenes/sandblock.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

        def update(self):
            pass

class Border(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/wall.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class Ground(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/ground.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class Dirt(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/dirt.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class Door(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/door.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class Wall(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/wall.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class LavaBlock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/lava.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class LevelBlock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Imagenes/portal.png")
        self.image.convert()
        self.rect = Rect(x, y, 18,18)

        def update(self):
            pass
class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))



game()
