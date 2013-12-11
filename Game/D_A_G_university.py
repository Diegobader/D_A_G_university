import pygame, sys
import Menu
def Map(level,stage): #Elige mapa de acuerdo a nivel
    return 'Maps/'+str(level)+'_'+str(stage)+'.txt'
def Character(level,stage,personaje):   #Elige Personaje y vestimenta de acuerdo a pj y nivel
    if personaje==1:
        return 'Imagenes/Sticks/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==2:
        return 'Imagenes/Woman/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==3:
        return 'Imagenes/Man/'+str(level)+'_'+str(stage)+'.png'
def menu():    #Despliega menu que solo retorna valores de personje (depende de cuantos sean) y muestra creditos y cierra juego
    resolution=(800,500)
    screen = pygame.display.set_mode(resolution, 0, 32) 
    menu_items_1 = ('Start','Credits','Quit')
    menu_items_2 = ('Stick','Woman','Man','Back')
    pygame.display.set_caption('Game Menu')
    while True:
        gm1 = Menu.GameMenu(screen, menu_items_1,resolution).run()
        if gm1==1:
            pass
        elif gm1==2:
            pass
        elif gm1==3:
            pygame.quit()
            sys.exit()
            break
        gm2 = Menu.GameMenu(screen, menu_items_2,resolution).run()
        if gm2<len(menu_items_2):
            break
    return int(gm2)
def game(vidas): #Hace correr los codigos
    pygame.init()
    character=menu()  #Para seleccionar personaje
    Character(1,1,character)   #para seleccionar vestimenta de personaje


  

game(3)

