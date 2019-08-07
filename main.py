import pygame as pg
from pygame.locals import *
import sys
import random



_FPS = 60

class Raquet(pg.Surface):
    x=0
    y=0
    w= 16
    h= 96
    color=(255, 255, 255)
    velocidad = 5
    diry =1

    def __init__(self):
        pg.Surface.__init__(self, (self.w, self.h))
        self.fill(self.color)

    def setColor(self, color):
        self.color = color
        self.fill(self.color)

    def avanza(self):
        self.y += self.diry * self.velocidad

        if self.y <= 0:
            self.y = 0

        if self.y >= 504:
            self.y = 504
        
        

class Ball(pg.Surface):    #sprite, objetos que se mueven por la pantalla.
    x=0
    y=0
    w=16
    h=16
    velocidad = 5
    dirx = velocidad
    diry = velocidad

    color = (255, 255, 255)  #tupla de 3 colores (RGB)
    
    def __init__(self):
        pg.Surface.__init__(self, (self.w,self.h))
        self.fill(self.color)

    def setColor(self, color):
        self.color = color
        self.fill(self.color)

    def avanza(self):
        if self.x >= 784:
            self.dirx = -self.velocidad 
        if self.y >= 584:
            self.diry = -self.velocidad 
        if self.x <= 0:
            self.dirx = self.velocidad 
        if self.y <= 0:
            self.diry = self.velocidad

        self.x += self.dirx
        self.y += self.diry

    def choqueBall(self, candidata):    #comprueba con el eje de las X en horizontal y con el eje de las Y comprueba en vertical 
        if (candidata.x >= self.x and candidata.x <= self.x+self.w or \
            candidata.x+candidata.w >= self.x and candidata.x+candidata.w <= self.x+self.w) and \
            (candidata.y >= self.x and candidata.y <= self.y+self.h or \
            candidata.y+candidata.h >= self.y and candidata.y+candidata.h <= self.y+self.h):
            
            self.dirx = self.dirx * -1
            self.x += self.dirx
               

class Game:    # en la clase Game se controlan los eventos
    clock = pg.time.Clock()      #velocidad de refresco

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display    #coge pg.display (objeto: pantalla) y lo mete en un atributo de la class Game para jugar con el.
        self.screen = self.display.set_mode(self.size)   # crea la pantalla   #set_mode() le dice la resolucion a la pantalla(display) o surface
        self.screen.fill((60,60,60))             #esto pinta la pantalla "screen" de gris ((60, 60, 60))
        self.display.set_caption("Mi juego")    #título para la ventana.

        self.ball1 = Ball()
        self.ball1.setColor((255, 0, 0))
        self.ball1.x =random.randrange(800)
        self.ball1.y =random.randrange(600)
        self.ball1.velocidad = random.randrange(2,9)

        self.player1 = Raquet()
        self.player1.x= 768
        self.player1.y= 252

    def start(self):
        while True:  #monta un bucle
            self.clock.tick(_FPS)   #velocidad de fps
            for event in pg.event.get():  #py.event acumula eventos.    #con get() te da los eventos de esa lista. 
                if event.type == QUIT:  #es una de las 'locals', un evento del tipo "salir"
                    pg.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.player1.diry = -1
                        self.player1.velocidad =15
                        self.player1.avanza()

                    if event.key == K_DOWN:
                        self.player1.diry = 1
                        self.player1.velocidad =15
                        self.player1.avanza()

            #Esto se hace para que no haya que darle muchas pulsaciones y poder MANTENER PRESIONADO el K_UP o el K_DOWN
            keys_pressed = pg.key.get_pressed()           #devuelve una lista de todas la teclase que han sido pulsadas (de un ciclo a otro?)
            if keys_pressed[K_UP] == 1:
                self.player1.diry = -1
                if self.player1.velocidad <=15:
                    self.player1.velocidad += 1
                self.player1.avanza()

        
            if keys_pressed[K_DOWN]:     #If... : si es True lo hace, no hace falta == 1
                self.player1.diry = 1
                if self.player1.velocidad <=15:
                    self.player1.velocidad += 1  #incrementa velocidad si se mantiene pulsado pero solo hasta 15
                self.player1.avanza()


            #modifica la posicion:
            self.ball1.avanza()
            self.ball1.choqueBall(self.player1)   # para que cambie de dirección cuando choque con player 1
          

            #Pintar los sprites en el screen:
            self.screen.fill((60, 60, 60))   #esto pinta la pantalla "screen" de gris ((60, 60, 60))
        
            self.screen.blit(self.ball1, (self.ball1.x , self.ball1.y))
            self.screen.blit(self.player1, (self.player1.x , self.player1.y))
            self.display.flip()   #repintar   #ampliando, pasa todo lo anterior a la tarjeta gráfica y lo pinta

if __name__ == '__main__':
    pg.init()   # inicializa pygame
    game = Game(800, 600)   #le da el tamaño, la tupla size.
    game.start()
