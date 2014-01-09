import pygame, sys
from pygame.locals import *
a=0

while a<200:
    pygame.init()
    SCREEN_X=32
    SCREEN_Y=60
    #Screen size

    SPRT_RECT_X=(input("insertx"))
    SPRT_RECT_Y=216
    #This is where the sprite is found on the sheet


    LEN_SPRT_X=32
    LEN_SPRT_Y=45
    #This is the lentgh of the sprite

    clock = pygame.time.Clock()
    speed=10

    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Make the screen
    sheet = pygame.image.load('stk_and_soap_mace.png') #Load the sheet

    sheet.set_clip(pygame.Rect(SPRT_RECT_X,SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y))#find the sprite you want
    draw_me = sheet.subsurface(sheet.get_clip()) #grab the sprite you want

    backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #make the whole screen so you can draw on it
    screen.fill((255,255,255))
    screen.blit(draw_me,backdrop)

    pygame.display.flip()
    pygame.display.update
    a+=1
