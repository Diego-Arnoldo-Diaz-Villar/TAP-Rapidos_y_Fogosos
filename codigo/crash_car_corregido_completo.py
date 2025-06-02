
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_y, K_n
import random
import os

pygame.init()

# Crear la ventana
ancho = 500
alto = 500
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Juego de Carros')

# Colores
gris = (100, 100, 100)
verde = (76, 208, 56)
rojo = (200, 0, 0)
blanco = (255, 255, 255)
amarillo = (255, 232, 0)

# Tamaños de la carretera y marcas
ancho_carretera = 300
ancho_marca = 10
alto_marca = 50

# Coordenadas de carriles
carril_izquierdo = 150
carril_centro = 250
carril_derecho = 350
carriles = [carril_izquierdo, carril_centro, carril_derecho]

carretera = (100, 0, ancho_carretera, alto)
marca_lateral_izquierda = (95, 0, ancho_marca, alto)
marca_lateral_derecha = (395, 0, ancho_marca, alto)
mover_marca_y = 0

jugador_x = 250
jugador_y = 400

reloj = pygame.time.Clock()
fps = 120
juego_terminado = False
velocidad = 2
puntuacion = 0

class Vehiculo(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        escala_imagen = 45 / imagen.get_rect().width
        nuevo_ancho = imagen.get_rect().width * escala_imagen
        nuevo_alto = imagen.get_rect().height * escala_imagen
        self.image = pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class VehiculoJugador(Vehiculo):
    def __init__(self, x, y):
        ruta_imagen = os.path.join(os.path.dirname(__file__), 'carros', 'car.png')
        if not os.path.exists(ruta_imagen):
            raise FileNotFoundError(f"No se encontró la imagen del jugador en {ruta_imagen}")
        imagen = pygame.image.load(ruta_imagen)
        super().__init__(imagen, x, y)

def iniciar_juego():
    global juego_terminado, velocidad, puntuacion

    grupo_jugador = pygame.sprite.Group()
    grupo_vehiculos = pygame.sprite.Group()

    jugador = VehiculoJugador(jugador_x, jugador_y)
    grupo_jugador.add(jugador)

    nombres_imagenes = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
    imagenes_vehiculos = []
    for nombre_imagen in nombres_imagenes:
        ruta = os.path.join(os.path.dirname(__file__), 'carros', nombre_imagen)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró la imagen del vehículo: {ruta}")
        imagen = pygame.image.load(ruta)
        imagenes_vehiculos.append(imagen)

    ruta_colision = os.path.join(os.path.dirname(__file__), 'carros', 'crash.png')
    if not os.path.exists(ruta_colision):
        raise FileNotFoundError(f"No se encontró la imagen de colisión en {ruta_colision}")
    colision = pygame.image.load(ruta_colision)
    rect_colision = colision.get_rect()

    corriendo = True
    while corriendo:
        reloj.tick(fps)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                corriendo = False
            if evento.type == KEYDOWN:
                if evento.key == K_LEFT and jugador.rect.center[0] > carril_izquierdo:
                    jugador.rect.x -= 100
                elif evento.key == K_RIGHT and jugador.rect.center[0] < carril_derecho:
                    jugador.rect.x += 100
                for vehiculo in grupo_vehiculos:
                    if pygame.sprite.collide_rect(jugador, vehiculo):
                        juego_terminado = True
                        if evento.key == K_LEFT:
                            jugador.rect.left = vehiculo.rect.right
                        elif evento.key == K_RIGHT:
                            jugador.rect.right = vehiculo.rect.left
                        rect_colision.center = [jugador.rect.center[0], jugador.rect.center[1]]

        pantalla.fill(verde)
        pygame.draw.rect(pantalla, gris, carretera)
        pygame.draw.rect(pantalla, amarillo, marca_lateral_izquierda)
        pygame.draw.rect(pantalla, amarillo, marca_lateral_derecha)

        global mover_marca_y
        mover_marca_y += velocidad * 2
        if mover_marca_y >= alto_marca * 2:
            mover_marca_y = 0
        for y in range(alto_marca * -2, alto, alto_marca * 2):
            pygame.draw.rect(pantalla, blanco, (carril_izquierdo + 45, y + mover_marca_y, ancho_marca, alto_marca))
            pygame.draw.rect(pantalla, blanco, (carril_centro + 45, y + mover_marca_y, ancho_marca, alto_marca))

        grupo_jugador.draw(pantalla)

        if len(grupo_vehiculos) < 2:
            añadir_vehiculo = True
            for vehiculo in grupo_vehiculos:
                if vehiculo.rect.top < vehiculo.rect.height * 1.5:
                    añadir_vehiculo = False
            if añadir_vehiculo:
                carril = random.choice(carriles)
                imagen = random.choice(imagenes_vehiculos)
                vehiculo = Vehiculo(imagen, carril, alto / -2)
                grupo_vehiculos.add(vehiculo)

        for vehiculo in grupo_vehiculos:
            vehiculo.rect.y += velocidad
            if vehiculo.rect.top >= alto:
                vehiculo.kill()
                puntuacion += 1
                if puntuacion > 0 and puntuacion % 5 == 0:
                    velocidad += 1

        grupo_vehiculos.draw(pantalla)

        fuente = pygame.font.Font(pygame.font.get_default_font(), 16)
        texto = fuente.render('Puntuación: ' + str(puntuacion), True, blanco)
        rect_texto = texto.get_rect(center=(50, 400))
        pantalla.blit(texto, rect_texto)

        if pygame.sprite.spritecollide(jugador, grupo_vehiculos, True):
            juego_terminado = True
            rect_colision.center = [jugador.rect.center[0], jugador.rect.top]

        if juego_terminado:
            pantalla.blit(colision, rect_colision)
            pygame.draw.rect(pantalla, rojo, (0, 50, ancho, 100))
            texto = fuente.render('Juego terminado. ¿Jugar de nuevo? (Y o N)', True, blanco)
            rect_texto.center = (ancho / 2, 100)
            pantalla.blit(texto, rect_texto)

        pygame.display.update()

        while juego_terminado:
            reloj.tick(fps)
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    juego_terminado = False
                    corriendo = False
                if evento.type == KEYDOWN:
                    if evento.key == K_y:
                        juego_terminado = False
                        velocidad = 2
                        puntuacion = 0
                        grupo_vehiculos.empty()
                        jugador.rect.center = [jugador_x, jugador_y]
                    elif evento.key == K_n:
                        juego_terminado = False
                        corriendo = False

    pygame.quit()

if __name__ == "__main__":
    iniciar_juego()
