import pygame as pg
from pygame.locals import *
import sys, os
import random



_FPS = 60

def between(valor, liminf, limsup):
    return valor >= liminf and valor <= limsup
    ''' También se puede poner:''' # reuturn liminf <= valor <= limsup

class Raquet(pg.Surface):
    x=0
    y=0
    w= 16
    h= 96
    color=(255, 255, 255)
    velocidad = 5
    diry =1
    sigueA = None
    esComputadora = False
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
        
    def sigue(self, pelota):   #pelota es ball1, una referencia de un objeto que contiene todos los atriubutos, por eso se puede poner después "sigueA.y"
        self.sigueA = pelota
        self.esComputadora = True

    def watch(self):
        if self.sigueA.x >= 100:
            if self.velocidad <= 10:   #ñapa para acelerar
                self.velocidad += 0.5   #ñapa para acelerar
            deltaY = self.sigueA.y - self.y
            if deltaY > 0:
                self.diry = +1
            elif deltaY < 0:
                self.diry = -1   
            else:
                self.diry = 0
            self.avanza()

class Ball(pg.Surface):    #sprite, objetos que se mueven por la pantalla.
    #atributos de Ball:
    x=0
    y=0
    w=16
    h=16
    velocidad = 5
    dirx = 1
    diry = 1
    cuentachoques = 0
    color = (255, 255, 255)  #tupla de 3 colores (RGB)
    
    def __init__(self):
        pg.Surface.__init__(self, (self.w,self.h))
        self.fill(self.color)

        self.sound = pg.mixer.Sound(os.getcwd()+'/assets/sonido.wav') #misma estructura que con font: 
        #            pg.font.Font(os.getcwd()+'/assets/fontUNO.ttf', 48) 
        
    def setColor(self, color):
        self.color = color
        self.fill(self.color)

    def saque(self, ganador):
        self.x = 392
        self.y = 292
        self.diry = random.choice([-1,1])  #elije de forma aleatoria -1 o 1,  hacia arriba o hacia abajo.
        self.cuentachoques = 0
        self.velocidad = 5

        if ganador == 1:
            self.dirx = -1
        else:
            self.dirx = 1

    def avanza(self):
        if self.x >= 784:
         # puntuar 
            self.saque(2)
            return 2

        if self.y >= 584:
            self.diry = -1
     
        if self.x <= 0:
         # puntuar 
           self.saque(1)
           return 1

        if self.y <= 0:
            self.diry = 1

        self.x += self.dirx * self.velocidad
        self.y += self.diry * self.velocidad
        return None

    def choqueBall(self, candidata):    #comprueba si y de la bola (self.y) está entre "y and y+h" de la raqueta
        if (between(self.y, candidata.y, candidata.y+candidata.h) or between(self.y+self.h, candidata.y, candidata.y+candidata.h)) and \
            (between(self.x, candidata.x, candidata.x+candidata.w) or between(self.x+self.w, candidata.x, candidata.x+candidata.w)):
            

            self.dirx = self.dirx * -1
            self.x += self.dirx
            self.sound.play()
            self.cuentachoques += 1

            if self.velocidad <= 14:
                self.velocidad += 0.5

            # es lo mismo que arriba    self.velocidad = min(14, self.velocidad + 0.5)      ##mínimo entre 14 y self.velocidad +0.5  ((el mínimo siempre será 14 =D))          
            print(self.velocidad)
        '''if (candidata.x >= self.x and candidata.x <= self.x+self.w or \
            candidata.x+candidata.w >= self.x and candidata.x+candidata.w <= self.x+self.w) and \
            (candidata.y >= self.x and candidata.y <= self.y+self.h or \
            candidata.y+candidata.h >= self.y and candidata.y+candidata.h <= self.y+self.h):'''
               

class Game:    # en la clase Game se controlan los eventos
    clock = pg.time.Clock()      #velocidad de refresco
    pause = False
    puntuaciones = {1: 0, 2: 0}
    winScore = 15
    
    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display    #coge pg.display (objeto: pantalla) y lo mete en un atributo de la class Game para jugar con el.
        self.screen = self.display.set_mode(self.size)   # crea la pantalla   #set_mode() le dice la resolucion a la pantalla(display) o surface
        self.screen.fill((60,60,60))             #esto pinta la pantalla "screen" de gris ((60, 60, 60))
        self.display.set_caption("Mi juego")    #título para la ventana.

        self.ball1 = Ball()
        self.ball1.setColor((255, 0, 0))

        self.player1 = Raquet()

        self.player1.sigue(self.ball1)
        print(self.player1.esComputadora)
        self.player2 = Raquet()
        

        self.fuente = pg.font.Font(os.getcwd()+'/assets/fontUNO.ttf', 48)    #podemos descargar la fuente de google fonts. Import sys,os.    # 24 es el tamñao
        
        self.iniciodepartida()
        
        
    
    def iniciodepartida(self):
        self.ball1.x = 392
        self.ball1.y = 292
        self.ball1.diry = random.choice([-1,1])  #elije de forma aleatoria -1 o 1,  hacia arriba o hacia abajo.
        self.ball1.dirx = random.choice([-1,1])
        self.ball1.velocidad = 7  #la velocidad sale al azar entre 2 y 9

        self.player1.x= 768
        self.player1.y= 252

        self.player2.x= 32
        self.player2.y= 252

        self.puntuaciones[1] = 0
        self.puntuaciones[2] = 0

        self.winner = None

        self.marcador1 = self.fuente.render(str(self.puntuaciones[1]), 1, (255,255,255))   #se ponenn abajo, en Star:
        self.marcador2 = self.fuente.render(str(self.puntuaciones[2]), 1, (255,255,255))

    def gameover(self):
        pg.quit()
        sys.exit()
     
    def handleevent(self):
        for event in pg.event.get():  #py.event acumula eventos.    #con get() te da los eventos de esa lista. 
            if event.type == QUIT:  #es una de las 'locals', un evento del tipo "salir"
                self. gameover()
                pg.quit()
                sys.exit()
        # Controlamos pulsación de teclas:
            if event.type == KEYDOWN:
                # Controlamos las teclas mantenidas:
                if event.key == K_UP and not self.player1.esComputadora:
                    self.player1.diry = -1
                    self.player1.velocidad =15
                    self.player1.avanza()

                if event.key == K_DOWN and not self.player1.esComputadora:
                    self.player1.diry = 1
                    self.player1.velocidad =15
                    self.player1.avanza()

                if event.key == K_w:
                    self.player2.diry = -1
                    self.player2.velocidad =15
                    self.player2.avanza()

                if event.key == K_s:
                    self.player2.diry = 1
                    self.player2.velocidad =15
                    self.player2.avanza()
                    
                if event.key == K_SPACE:
                    if self.winner:
                        self.iniciodepartida()
                    self.pause = False
                
                
            #Esto se hace para que no haya que darle muchas pulsaciones y poder MANTENER PRESIONADO el K_UP o el K_DOWN
        keys_pressed = pg.key.get_pressed()           #devuelve una lista de todas la teclase que han sido pulsadas (de un ciclo a otro?)
        if not self.player1.esComputadora:
            if keys_pressed[K_UP]:
                self.player1.diry = -1
                if self.player1.velocidad <=15:
                    self.player1.velocidad += 1
                self.player1.avanza()

            
            if keys_pressed[K_DOWN]:     #If... : si es True lo hace, no hace falta == 1
                self.player1.diry = 1
                if self.player1.velocidad <=15:
                    self.player1.velocidad += 1  #incrementa velocidad si se mantiene pulsado pero solo hasta 15
                self.player1.avanza()
        else:
            self.player1.watch()

        if keys_pressed[K_w]:
            self.player2.diry = -1
            if self.player2.velocidad <=15:
                self.player2.velocidad += 1
            self.player2.avanza()

        
        if keys_pressed[K_s]:     #If... : si es True lo hace, no hace falta == 1
            self.player2.diry = 1
            if self.player2.velocidad <=15:
                self.player2.velocidad += 1  #incrementa velocidad si se mantiene pulsado pero solo hasta 15
            self.player2.avanza()

    def recalculate(self):
        #modifica la posicion:
        if not self.pause:
            p = self.ball1.avanza()
            if p:
                self.pause = True
                self.puntuaciones[p] += 1
                
                self.marcador1 = self.fuente.render(str(self.puntuaciones[1]), 1, (255,255,255))
                self.marcador2 = self.fuente.render(str(self.puntuaciones[2]), 1, (255,255,255))
                 
                if self.puntuaciones[1] >= self.winScore or self.puntuaciones[2] >= self.winScore:
                    self.winner = self.fuente.render("Eres el mejor jugador {} !!!".format(p), 1, (255,255,0))
                        
                

        self.ball1.choqueBall(self.player1)   # para que cambie de dirección cuando choque con player 1
        self.ball1.choqueBall(self.player2)

    def render(self):
        #Pintar los sprites en el screen:
        self.screen.fill((60, 60, 60))   #esto pinta la pantalla "screen" de gris ((60, 60, 60))
        
        self.screen.blit(self.ball1, (self.ball1.x , self.ball1.y))
        self.screen.blit(self.player1, (self.player1.x , self.player1.y))
        self.screen.blit(self.player2, (self.player2.x , self.player2.y))
        self.screen.blit(self.marcador2, (16 , 8))
        caja = self.marcador1.get_rect()
        self.screen.blit(self.marcador1, ( 784 -caja.w, 8))
            
        if self.winner:
            rect = self.winner.get_rect()   #recuperacion del rectangulo, posicion y tamaño supongo
            self.screen.blit(self.winner, ((800- rect.w)//2, (600 -rect.h)//2))

        self.display.flip()   #repintar   #ampliando, pasa todo lo anterior a la tarjeta gráfica y lo pinta    


        ''' def movimientoP1(self):
        if self.ball1.y >= 120:
            
            self.player1.y = self.ball1.y - self.player1.h/2'''
            

    def start(self):
        while True:  #monta un bucle
            self.clock.tick(_FPS)   #velocidad de fps
            
            self.handleevent()
            
            self.recalculate()
            
            self.render()

            #self.movimientoP1()

if __name__ == '__main__':
    pg.init()   # inicializa pygame
    game = Game(800, 600)   #le da el tamaño, la tupla size.
    game.start()
