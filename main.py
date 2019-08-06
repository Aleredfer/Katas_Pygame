import pygame as pg
from pygame.locals import *
import sys

FPS = 60

class Ball(pg.sprite.Sprite):    #sprite, objetos que se mueven por la pantalla.
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)    #inicializa 
        self.image = pg.Surface((16, 16))   #tamaño
        self.rect = self.image.get_rect()   #es el rectangulo donde está contenida la imagen.
        
        #posicion:
        self.x = x
        self.y = y

        #color
        self.color = (255, 255, 255)  #tupla de 3 colores (RGB)

        #iniciar la parte gráfica
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.fill(self.color)


'''class OtraBall(pg.surface):
    def __init__(self, x, y):
        pg.Surface.__init__(self, (16,16))
        self.fill((255,255,255))
        self'''


class Game:    # en la clase Game se controlan los eventos
    clock = pg.time.Clock()      #velocidad de refresco
    Velocidad = 5

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display    #coge pg.display (objeto: pantalla) y lo mete en un atributo de la class Game para jugar con el.
        self.screen = self.display.set_mode(self.size)   # crea la pantalla   #set_mode() le dice la resolucion a la pantalla(display) o surface
        self.screen.fill((60,60,60))                    #esto pinta la pantalla "screen" de gris ((60, 60, 60))
        self.display.set_caption("Mi juego")    #título para la ventana.

        self.ball = pg.Surface((16, 16))
        self.ball.fill((255,255,255))
        #self.ball = Ball(392, 292)   #correccion de 8 puntos para que el ''centro esté en el centro''       ## 400 y 300 es el centro de 800x600...
        #self.ball.get_rect.x =392
        #self.ball.get_rect.y =292
        
        #si quiero otra bola:
        self.ball1 = pg.Surface((16, 16))
        self.ball1.fill((255,0,0))       #y la inicializo en start: self.screen.blit(self.ball1, (x+10, y+10))
        
    def start(self):
        x=392
        y=292
        dirx = self.Velocidad 
        diry = self.Velocidad 
        
        #bola 2:
        x1=0
        y1=0

        dirx1 = self.Velocidad 
        diry1 = self.Velocidad

        while True:  #monta un bucle
            self.clock.tick(FPS)   #velocidad de fps
            for event in pg.event.get():  #py.event acumula eventos.    #con get() te da los eventos de esa lista. 
                if event.type == QUIT:  #es una de las 'locals', un evento del tipo "salir"
                    pg.quit()
                    sys.exit()
            #modifica la posicion:
            if x >= 784:
                dirx = -self.Velocidad 
            if y >= 584:
                diry = -self.Velocidad 
            if x <= 0:
                dirx = self.Velocidad 
            if y <= 0:
                diry = self.Velocidad

            if x1 >= 784:
                dirx1 = -self.Velocidad 
            if y1 >= 584:
                diry1 = -self.Velocidad 
            if x1 <= 0:
                dirx1 = self.Velocidad 
            if y1 <= 0:
                diry1 = self.Velocidad


            x += dirx
            y += diry

            x1 += dirx1
            y1 += diry1

            #Pintar los sprites en el screen:
            self.screen.fill((60, 60, 60))   #esto pinta la pantalla "screen" de gris ((60, 60, 60))
            self.screen.blit(self.ball, (x, y))  #Metodo blit()  blit(image, (x, y)) posiciona la imagen. Dibuja una imagen dentro de otra: la bola dentro de la pantalla (o sobre)            
            self.screen.blit(self.ball1, (x1, y1))
            self.display.flip()   #repintar   #ampliando, pasa todo lo anterior a la tarjeta gráfica y lo pinta

if __name__ == '__main__':
    pg.init()   # inicializa pygame
    game = Game(800, 600)   #le da el tamaño, la tupla size.
    game.start()
