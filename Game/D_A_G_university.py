import pygame, sys
import Menu
import l1s1

#############Clase para el launcher###########
class Start:
    
    def __init__(self):
        pass
    def Go(self,ArcadeServiceInterface):
        try:
            return 0
        except Exception:
            return -1
###############################################


def Map(level,stage): #Elige mapa de acuerdo a nivel
    return 'Maps/'+str(level)+'_'+str(stage)+'.txt'
def Fondo(level,stage):
    return 'Images/Others/'+str(level)+'_'+str(stage)+'.png'
def Character(level,stage,personaje):   #Elige Personaje y vestimenta de acuerdo a pj y nivel
    if personaje==3:
        return 'Images/Sticks/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==1:
        return 'Images/Woman/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==2:
        return 'Images/Man/'+str(level)+'_'+str(stage)+'.png'
def menu(resolution):    #Despliega menu que solo retorna valores de personje (depende de cuantos sean) y muestra creditos y cierra juego
    pygame.mixer.init()
    pygame.mixer.music.load("Music/Menu.mp3")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(resolution, 0, 32) 
    menu_items_2 = ('Woman','Man','Stick','Quit')
    pygame.display.set_caption('D_A_G')
    while True:
        Menu.GameMenu(screen,resolution, ((resolution[0])/10)).run()
        gm2 = Menu.CharMenu(screen, menu_items_2,resolution, ((resolution[0])/10)).run()
        if gm2<len(menu_items_2):
            break
        elif gm2==len(menu_items_2):
            pygame.quit()
    return int(gm2)
def game(resolution): #Hace correr los codigos
    pygame.init()
    character=menu(resolution)  #Para seleccionar personaje
    Character(1,1,character)   #para seleccionar vestimenta de personaje
    pygame.mixer.music.load("Music/Shower.mp3")
    pygame.mixer.music.play(-1)
    if l1s1.main(resolution,Character(1,1,character))==True:
        screen.blit(clear,(resolution[0]*1/4,resolution[1]*1/2))
        pygame.time.delay(2000)
    else:
        pygame.quit()

game((500,500))

