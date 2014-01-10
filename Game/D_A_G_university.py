import pygame, sys
import Menu
import Main
def Map(level,stage): #Elige mapa de acuerdo a nivel
    return 'Maps/'+str(level)+'_'+str(stage)+'.txt'
def Fondo(level,stage):
    return 'Images/Others/'+str(level)+'_'+str(stage)+'.png'
def Character(level,stage,personaje):   #Elige Personaje y vestimenta de acuerdo a pj y nivel
    if personaje==1:
        return 'Images/Sticks/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==2:
        return 'Images/Woman/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==3:
        return 'Images/Man/'+str(level)+'_'+str(stage)+'.png'
def menu(resolution):    #Despliega menu que solo retorna valores de personje (depende de cuantos sean) y muestra creditos y cierra juego
    pygame.mixer.init()
    pygame.mixer.music.load("Music/Menu.mp3")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(resolution, 0, 32) 
    menu_items_1 = ('Start','Credits','Quit')
    menu_items_2 = ('Stick','Woman','Man','Back')
    pygame.display.set_caption('Game Menu')
    while True:
        gm1 = Menu.GameMenu(screen, menu_items_1,resolution, ((resolution[0])/10)).run()
        if gm1==1:
            pass
        elif gm1==2:
            pass
        elif gm1==3:
            pygame.quit()
            sys.exit()
            break
        gm2 = Menu.GameMenu(screen, menu_items_2,resolution, ((resolution[0])/10)).run()
        if gm2<len(menu_items_2):
            break
    return int(gm2)
def game(vidas,resolution): #Hace correr los codigos
    pygame.init()
    character=menu(resolution)  #Para seleccionar personaje
    Character(1,1,character)   #para seleccionar vestimenta de personaje
    Main.main(resolution,Character(1,1,character))            
game(3,(1024,768))

