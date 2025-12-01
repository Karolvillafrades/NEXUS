#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sept 30 17:36:28 2025

@author: karolvillafradessantos
"""
import pygame
import random
import sys
import math

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Reingreso Aeroespacial, By: KL")
# Cargar logo (PNG con transparencia)
logo = pygame.image.load("logo.png").convert_alpha()

# Escala para que quede chimba
logo = pygame.transform.smoothscale(logo, (180, 180))

# Pantalla
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("NEXUS")

# Colores
NEGRO = (0, 0, 0)
AZUL_PROFUNDO = (10, 10, 40)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
AMARILLO = (255, 255, 0)
GRIS = (150, 150, 150)
NARANJA_FUEGO = (255, 140, 0)
NARANJA_CLARO = (255, 180, 0)
AMARILLO_CLARO = (255, 255, 100)
GRIS_OSCURO = (70, 70, 70)
TURQUESA = (0, 255, 255)
VERDE_EXITO = (0, 180, 0)

# Colores Planetarios Mejorados y más específicos
GRIS_MERCURIO = (100, 100, 100)
GRIS_MERCURIO_CLARO = (150, 150, 150)
NARANJA_VENUS = (200, 150, 50)
AMARILLO_VENUS = (255, 200, 100)
AZUL_TIERRA = (30, 100, 200)
VERDE_TIERRA = (0, 150, 50)
ROJO_MARTE = (150, 80, 0)
ROJO_MARTE_CLARO = (200, 120, 40)
AZUL_JUPITER = (120, 120, 180)
CREMA_JUPITER = (220, 200, 150)
AMARILLO_SATURNO = (200, 180, 50)
AMARILLO_SATURNO_CLARO = (255, 230, 120)
AZUL_URANO = (0, 150, 200)
AZUL_NEPTUNO = (50, 100, 200)

# Constante de la barra superior
BARRA_ALTO = 40
LIMITE_SUPERIOR_JUEGO = BARRA_ALTO + 5

# Fuente
fuente_pequena = pygame.font.SysFont("Arial", 18, bold=True)
fuente = pygame.font.SysFont("Arial", 24, bold=True)
fuente_media = pygame.font.SysFont("Arial", 36, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 48, bold=True)
fuente_enorme = pygame.font.SysFont("Arial", 60, bold=True)
fuente_iconos = pygame.font.SysFont("Arial", 24, bold=True)

# Jugador (cohete)
jugador = pygame.Rect(ANCHO//2, BARRA_ALTO + 20, 30, 60)
velocidad_x, velocidad_y = 0.0, 0.0
gravedad = 0.1

# Planeta inicial (círculo al fondo)
planeta_radio = 150
planeta = pygame.Rect(ANCHO//2 - planeta_radio, ALTO-200, planeta_radio*2, planeta_radio*2)

# Variables para el movimiento del planeta
planeta_dir = 1
PLANETA_VEL = 1

# Estrellas de fondo (pre-generadas)
NUM_ESTRELLAS = 80
estrellas_fondo = [{'pos': [random.randint(0, ANCHO), random.randint(0, ALTO)],
                    'speed': random.uniform(0.1, 0.5),
                    'size': random.randint(1, 3),
                    'color': BLANCO} for _ in range(NUM_ESTRELLAS)]

# Meteoritos, estrellas recolectables, partículas
meteoritos = []
estrellas_comb = []
particulas_propulsion = []
particulas_explosion = []

# Variables de juego
puntaje = 0
nivel = 1
combustible = 100
MAX_VIDAS = 3
vidas = MAX_VIDAS
explosion = False
estado_juego = "MENU"
estado_anterior = "MENU"
resultado = ""
carga_progreso = 0
carga_velocidad = 2
puntaje_final_game_over = 0
nivel_final_game_over = nivel
clock = pygame.time.Clock()

# Límites para listas para evitar crecimiento ilimitado
MAX_METEORITOS = 35
MAX_PARTICULAS_PROP = 120
MAX_PARTICULAS_EXP = 150
MAX_ESTRELLAS_COMB = 6

# Datos de los planetas (8)
PLANETA_COLORES_OCEANO = [
    GRIS_MERCURIO, NARANJA_VENUS, AZUL_TIERRA, ROJO_MARTE,
    AZUL_JUPITER, AMARILLO_SATURNO, AZUL_URANO, AZUL_NEPTUNO
]
PLANETA_NOMBRES = [
    "MERCURIO", "VENUS", "TIERRA", "MARTE",
    "JUPITER", "SATURNO", "URANO", "NEPTUNO"
]

# Surface para dibujar los detalles de los planetas 
planeta_details_surface = pygame.Surface((planeta_radio * 2, planeta_radio * 2), pygame.SRCALPHA)
angulo_rotacion_globo = 0.0
velocidad_rotacion_planeta = 0.003

# Cache para la rotación: no rotar cada frame
ROTATE_EVERY = 2  # rotar cada N frames
_frame_counter = 0
_rotated_cache = None
_last_angle_for_cache = None

#Empiezo a definir funciones
def dibujar_logo_superior():
    # Centrar el logo horizontalmente
    x = ANCHO // 2 - logo.get_width() // 2
    y = 30   # apenas un poquito más abajo

    pantalla.blit(logo, (x, y))

# Nebulosas (pre-generate)
def generar_nebulosas():
    indice_planeta = (nivel - 1) % 8
    colores_nebulosa = [
        (40, 0, 40, 50), (80, 80, 0, 50), (10, 10, 40, 50), (80, 20, 0, 50),
        (50, 50, 150, 50), (100, 0, 0, 50), (0, 80, 80, 50), (0, 0, 100, 50)
    ]
    color_base = colores_nebulosa[indice_planeta]
    nueva_nebulosas = []
    # Reducimos la cantidad para performance
    for _ in range(6):
        x = random.randint(-ANCHO//2, ANCHO*3//2)
        y = random.randint(-ALTO//2, ALTO*3//2)
        radio = random.randint(150, 300)
        nueva_nebulosas.append({'pos': [x, y],
                                 'radio': radio,
                                 'color': color_base,
                                 'speed': random.uniform(0.02, 0.07)})
    return nueva_nebulosas

nebulosas = generar_nebulosas()

def dibujar_detalles_planeta_a_surface():
    """Rellena planeta_details_surface según el planeta actual.
       Se llama cuando cambia el planeta o se reinicia nivel."""
    global planeta_details_surface
    planeta_details_surface.fill((0, 0, 0, 0))

    indice_planeta = (nivel - 1) % len(PLANETA_NOMBRES)
    nombre_mundo = PLANETA_NOMBRES[indice_planeta]

    if nombre_mundo == "MERCURIO":
        for _ in range(20):
            x = random.randint(0, planeta_radio * 2)
            y = random.randint(0, planeta_radio * 2)
            r = random.randint(3, 10)
            pygame.draw.circle(planeta_details_surface, GRIS_MERCURIO_CLARO, (x, y), r)
            pygame.draw.circle(planeta_details_surface, GRIS_OSCURO, (x, y), max(1, r - 2))

    elif nombre_mundo == "VENUS":
        for _ in range(25):
            x = random.randint(0, planeta_radio * 2)
            y = random.randint(0, planeta_radio * 2)
            r = random.randint(10, 24)
            color_nube = random.choice([AMARILLO_VENUS, NARANJA_VENUS])
            # use alpha blending by drawing onto surface with alpha
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_nube + (100,), (r, r), r)
            planeta_details_surface.blit(s, (x - r, y - r))

    elif nombre_mundo == "TIERRA":
        for _ in range(6):
            x_offset = random.randint(0, planeta_radio * 2)
            y_offset = random.randint(0, planeta_radio * 2)
            num_puntos = random.randint(5, 10)
            puntos = []
            for _ in range(num_puntos):
                angle = random.uniform(0, 2 * math.pi)
                r = random.uniform(20, 50)
                puntos.append((x_offset + r * math.cos(angle), y_offset + r * math.sin(angle)))
            if len(puntos) > 2:
                pygame.draw.polygon(planeta_details_surface, VERDE_TIERRA, puntos)

    elif nombre_mundo == "MARTE":
        for _ in range(10):
            x = random.randint(0, planeta_radio * 2)
            y = random.randint(0, planeta_radio * 2)
            r = random.randint(5, 12)
            pygame.draw.circle(planeta_details_surface, ROJO_MARTE_CLARO, (x, y), r)
            pygame.draw.circle(planeta_details_surface, GRIS_OSCURO, (x, y), max(1, r - 3))
        pygame.draw.circle(planeta_details_surface, BLANCO, (planeta_radio, 30), 20)
        pygame.draw.circle(planeta_details_surface, BLANCO, (planeta_radio, planeta_radio*2 - 30), 20)

    elif nombre_mundo == "JUPITER":
        for i in range(10):
            color_banda = CREMA_JUPITER if i % 2 == 0 else AZUL_JUPITER
            y_banda = int((i / 10) * planeta_radio * 2)
            alto_banda = random.randint(15, 25)
            pygame.draw.rect(planeta_details_surface, color_banda, (0, y_banda, planeta_radio * 2, alto_banda))
        pygame.draw.ellipse(planeta_details_surface, ROJO, (planeta_radio - 50, planeta_radio - 20, 80, 40), 0)

    elif nombre_mundo == "SATURNO":
        for i in range(10):
            color_banda = AMARILLO_SATURNO_CLARO if i % 2 == 0 else AMARILLO_SATURNO
            y_banda = int((i / 10) * planeta_radio * 2)
            alto_banda = random.randint(15, 25)
            pygame.draw.rect(planeta_details_surface, color_banda, (0, y_banda, planeta_radio * 2, alto_banda))

    elif nombre_mundo in ("URANO", "NEPTUNO"):
        for _ in range(18):
            x = random.randint(0, planeta_radio * 2)
            y = random.randint(0, planeta_radio * 2)
            r = random.randint(8, 20)
            color_nube = AZUL_URANO if nombre_mundo == "URANO" else AZUL_NEPTUNO
            color_nube = (min(255, color_nube[0]+50), min(255, color_nube[1]+50), min(255, color_nube[2]+50), 80)
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_nube, (r, r), r)
            planeta_details_surface.blit(s, (x - r, y - r))

def dibujar_nebulosas():
    """Dibuja nebulosas; cada una tiene su propia superficie para no repetir tanto."""
    for n in nebulosas:
        # Dibujamos con pasos más grandes para ahorrar trabajo
        s = pygame.Surface((n['radio'] * 2, n['radio'] * 2), pygame.SRCALPHA)
        step = max(6, n['radio'] // 20)
        for i in range(n['radio'], 0, -step):
            alpha = int(255 * (1 - (i / n['radio'])) * 0.5)
            color_c = (n['color'][0], n['color'][1], n['color'][2], alpha)
            pygame.draw.circle(s, color_c, (n['radio'], n['radio']), i)
        n['pos'][0] += n['speed'] * 0.5
        n['pos'][1] += n['speed'] * 0.5
        pantalla.blit(s, (n['pos'][0] - n['radio'], n['pos'][1] - n['radio']))


def dibujar_cohete(x, y, propulsando=False):
    pygame.draw.rect(pantalla, BLANCO, (x-10, y, 20, 40))
    pygame.draw.polygon(pantalla, ROJO, [(x, y-20), (x-12, y), (x+12, y)])
    pygame.draw.polygon(pantalla, ROJO, [(x-10, y+40), (x-20, y+60), (x-10, y+60)])
    pygame.draw.polygon(pantalla, ROJO, [(x+10, y+40), (x+20, y+60), (x+10, y+60)])

    if propulsando:
        pygame.draw.polygon(pantalla, NARANJA_FUEGO, [(x, y+60), (x-8, y+80), (x+8, y+80)])
        pygame.draw.polygon(pantalla, NARANJA_CLARO, [(x, y+65), (x-5, y+75), (x+5, y+75)])

        # Añade partículas, pero limita su número
        if len(particulas_propulsion) < MAX_PARTICULAS_PROP:
            for _ in range(random.randint(1, 2)):
                size = random.randint(2, 6)
                color = random.choice([NARANJA_FUEGO, NARANJA_CLARO, AMARILLO_CLARO, GRIS_OSCURO])
                particulas_propulsion.append({
                    'pos': [x + random.randint(-5, 5), y + 60 + random.randint(0, 10)],
                    'vel': [random.uniform(-1, 1), random.uniform(2, 4)],
                    'size': size, 'lifetime': 30, 'color': color
                })

def dibujar_planeta():
    """Dibuja el planeta con rotación cacheada para no rotar cada frame."""
    global angulo_rotacion_globo, _frame_counter, _rotated_cache, _last_angle_for_cache

    centro_x, centro_y = planeta.center
    indice_planeta = (nivel - 1) % len(PLANETA_NOMBRES)
    color_base_planeta = PLANETA_COLORES_OCEANO[indice_planeta]
    nombre_mundo = PLANETA_NOMBRES[indice_planeta]

    # Rotación controlada
    if nombre_mundo in ("URANO", "NEPTUNO"):
        velocidad_rotacion_planeta_actual = velocidad_rotacion_planeta * 0.5
    else:
        velocidad_rotacion_planeta_actual = velocidad_rotacion_planeta

    angulo_rotacion_globo += velocidad_rotacion_planeta_actual
    if angulo_rotacion_globo >= 2 * math.pi:
        angulo_rotacion_globo -= 2 * math.pi

    # Sólo recalcular rotado cada ROTATE_EVERY frames
    _frame_counter += 1
    angle_degrees = math.degrees(angulo_rotacion_globo)
    if _rotated_cache is None or (_frame_counter % ROTATE_EVERY == 0 and _last_angle_for_cache != angle_degrees):
        rotated_details = pygame.transform.rotate(planeta_details_surface, angle_degrees)
        _rotated_cache = rotated_details
        _last_angle_for_cache = angle_degrees

    # Dibuja los anillos de Saturno (si aplica)
    if nombre_mundo == "SATURNO":
        pygame.draw.ellipse(pantalla, GRIS_OSCURO, (centro_x - planeta_radio*1.6, centro_y - planeta_radio*0.4, planeta_radio*3.2, planeta_radio*0.8), 0)
        pygame.draw.ellipse(pantalla, GRIS, (centro_x - planeta_radio*1.4, centro_y - planeta_radio*0.3, planeta_radio*2.8, planeta_radio*0.6), 0)
        pygame.draw.ellipse(pantalla, BLANCO, (centro_x - planeta_radio*1.2, centro_y - planeta_radio*0.25, planeta_radio*2.4, planeta_radio*0.5), 0)

    temp_surface = pygame.Surface((planeta_radio * 2, planeta_radio * 2), pygame.SRCALPHA)
    pygame.draw.circle(temp_surface, color_base_planeta, (planeta_radio, planeta_radio), planeta_radio)

    if _rotated_cache:
        rect_rotated = _rotated_cache.get_rect(center=(planeta_radio, planeta_radio))
        temp_surface.blit(_rotated_cache, rect_rotated.topleft)

    # Sombreado ligero
    sombreado_surface = pygame.Surface((planeta_radio * 2, planeta_radio * 2), pygame.SRCALPHA)
    for i in range(planeta_radio, 0, -8):
        alpha = int(255 * (1 - (i / planeta_radio)) * 0.6)
        pygame.draw.circle(sombreado_surface, (0, 0, 0, alpha), (planeta_radio, planeta_radio), i)
    temp_surface.blit(sombreado_surface, (0, 0))

    pantalla.blit(temp_surface, (planeta.x, planeta.y))

    texto_tierra = fuente.render(f"{nombre_mundo}", True, BLANCO)
    pantalla.blit(texto_tierra, (planeta.centerx - texto_tierra.get_width()//2, ALTO-100))

def dibujar_game_over():
    # Fondo oscuro 
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    pantalla.blit(overlay, (0, 0))

    # Titulo game over
    font_gameover = pygame.font.Font(None, 100)
    texto_go = font_gameover.render("GAME OVER", True, (255, 50, 50))
    pantalla.blit(texto_go, (ANCHO//2 - texto_go.get_width()//2, 150))

    # Subtítulo estilo aeroespacial
    font_sub = pygame.font.Font(None, 40)
    texto_sub = font_sub.render("Protocolo de misión finalizado", True, (200, 200, 200))
    pantalla.blit(texto_sub, (ANCHO//2 - texto_sub.get_width()//2, 230))

    # Boton continuar
    btn_font = pygame.font.Font(None, 50)
    texto_continuar = btn_font.render("Continuar", True, (255, 255, 255))
    btn_continuar_rect = texto_continuar.get_rect(center=(ANCHO//2, 330))
    pantalla.blit(texto_continuar, btn_continuar_rect)

    # Boton salir
    texto_salir = btn_font.render("Salir", True, (255, 255, 255))
    btn_salir_rect = texto_salir.get_rect(center=(ANCHO//2, 400))
    pantalla.blit(texto_salir, btn_salir_rect)

    return btn_continuar_rect, btn_salir_rect

def mostrar_game_over():
    clock = pygame.time.Clock()

    while True:
        pantalla.fill((0, 0, 0))

        btn_continuar_rect, btn_salir_rect = dibujar_game_over()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Clic del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_continuar_rect.collidepoint(event.pos):
                    return "continuar"   # Regresa al juego
                if btn_salir_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

            # Teclas opcionales
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:   # "c" para continuar
                    return "continuar"
                if event.key == pygame.K_q:   # "q" para salir
                    pygame.quit()
                    exit()

        clock.tick(60)

def reiniciar_juego(mantener_nivel=False, avanzar_nivel=False):
    global jugador, velocidad_x, velocidad_y, meteoritos, estrellas_comb, \
           particulas_propulsion, particulas_explosion, explosion, estado_juego, \
           resultado, combustible, vidas, nivel, angulo_rotacion_globo, puntaje, nebulosas, \
           puntaje_final_game_over, nivel_final_game_over, planeta, planeta_dir

    # Capturar puntaje y nivel para la pantalla de GAME OVER/VICTORY
    puntaje_final_game_over = puntaje
    nivel_final_game_over = nivel

    jugador.x, jugador.y = ANCHO//2, BARRA_ALTO + 20
    velocidad_x, velocidad_y = 0.0, 0.0
    meteoritos.clear()
    estrellas_comb.clear()
    particulas_propulsion.clear()
    particulas_explosion.clear()
    explosion = False
    estado_juego = "JUGANDO"
    resultado = ""
    combustible = 100

    if not mantener_nivel and not avanzar_nivel:
        vidas = MAX_VIDAS
        
    elif avanzar_nivel:
        # Si pasó el nivel, darle una vida extra sin exceder el máximo
        vidas = min(MAX_VIDAS, vidas + 1)

    # REeinciar posicion del planeta, normal
    planeta.x = ANCHO // 2 - planeta_radio
    planeta_dir = random.choice([-1, 1])

    angulo_rotacion_globo = 0.0
    dibujar_detalles_planeta_a_surface()
    nebulosas = generar_nebulosas()

def manejar_click_botones(pos):
    global estado_juego, estado_anterior, nivel, carga_progreso

    BTN_SIZE = 30
    SPACING = 5
    x_offset = 10

    # Botones (Salir, Reiniciar, Pausa) 
    btn_salir_rect = pygame.Rect(x_offset, SPACING, BTN_SIZE, BTN_SIZE)
    x_offset += BTN_SIZE + SPACING
    btn_reiniciar_rect = pygame.Rect(x_offset, SPACING, BTN_SIZE, BTN_SIZE)
    x_offset += BTN_SIZE + SPACING
    btn_pausa_rect = pygame.Rect(x_offset, SPACING, BTN_SIZE, BTN_SIZE)

  # Botones del juego (durante)

    if estado_juego in ("JUGANDO", "PAUSA"):

        if btn_salir_rect.collidepoint(pos):
            pygame.quit()
            sys.exit()

        if btn_reiniciar_rect.collidepoint(pos):
            reiniciar_juego(mantener_nivel=False
                        )

        if btn_pausa_rect.collidepoint(pos):
            if estado_juego == "JUGANDO":
                estado_anterior = "JUGANDO"
                estado_juego = "PAUSA"
            else:
                estado_juego = "JUGANDO"

    # Boton de nivel completado
    elif estado_juego == "NIVEL_COMPLETADO":

        BTN_ANCHO, BTN_ALTO = 200, 50
        BTN_Y = ALTO // 2 + 100
        BTN_SPACING = 30

        btn_siguiente_rect = pygame.Rect(
            ANCHO // 2 - BTN_ANCHO - BTN_SPACING // 2, BTN_Y, BTN_ANCHO, BTN_ALTO
        )
        btn_salir_mision_rect = pygame.Rect(
            ANCHO // 2 + BTN_SPACING // 2, BTN_Y, BTN_ANCHO, BTN_ALTO
        )

        if btn_siguiente_rect.collidepoint(pos):
            estado_juego = "CARGANDO_NIVEL"
            carga_progreso = 0

        if btn_salir_mision_rect.collidepoint(pos):
            pygame.quit()
            sys.exit()

    # Boton de game over
    elif estado_juego == "GAME_OVER":

        BTN_ANCHO, BTN_ALTO = 200, 50
        BTN_Y = ALTO // 2 + 100
        BTN_SPACING = 30

        btn_reintentar_rect = pygame.Rect(
            ANCHO // 2 - BTN_ANCHO - BTN_SPACING // 2, BTN_Y, BTN_ANCHO, BTN_ALTO
        )
        btn_salir_gameover_rect = pygame.Rect(
            ANCHO // 2 + BTN_SPACING // 2, BTN_Y, BTN_ANCHO, BTN_ALTO
        )

        # Reintentar
        if btn_reintentar_rect.collidepoint(pos):
            reiniciar_juego(mantener_nivel=True)   # Mantiene el nivel donde perdió
            estado_juego = "JUGANDO"

        # Salir
        if btn_salir_gameover_rect.collidepoint(pos):
            pygame.quit()
            sys.exit()

def dibujar_carga_suspensiva(progreso):
    global estado_juego, carga_progreso
    nivel_bg = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    nivel_bg.fill((0, 0, 0, 200))
    pantalla.blit(nivel_bg, (0, 0))

    titulo = fuente_grande.render("ESTABILIZANDO DATOS DE MISIÓN...", True, BLANCO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 100))

    BAR_ANCHO, BAR_ALTO = 400, 30
    BAR_X, BAR_Y = ANCHO//2 - BAR_ANCHO//2, ALTO//2 + 20

    pygame.draw.rect(pantalla, GRIS_OSCURO, (BAR_X, BAR_Y, BAR_ANCHO, BAR_ALTO), 3, 5)

    segmento_ancho = 50
    espacio = 15
    offset_animacion = (progreso * (segmento_ancho + espacio) * 0.05) % (segmento_ancho + espacio)

    for i in range(-5, int(BAR_ANCHO / (segmento_ancho + espacio)) + 5):
        x_start = BAR_X + i * (segmento_ancho + espacio) + offset_animacion
        rect_segmento = pygame.Rect(x_start, BAR_Y, segmento_ancho, BAR_ALTO)
        rect_visible = rect_segmento.clip((BAR_X, BAR_Y, BAR_ANCHO, BAR_ALTO))
        if rect_visible.width > 0:
            pygame.draw.rect(pantalla, VERDE_EXITO, rect_visible, 0, 5)

    carga_progreso += carga_velocidad
    if carga_progreso >= 150:
        carga_progreso = 0

        if nivel_final_game_over <= 0:
            reiniciar_juego(mantener_nivel=False)
        else:
            reiniciar_juego(avanzar_nivel=True)

def dibujar_explosion(x, y):
    """Crea y dibuja la explosión; usa globales correctamente y limita partículas."""
    global particulas_explosion, estado_juego, carga_progreso

    if not particulas_explosion:
        for _ in range(40):  # menos partículas para performance
            particulas_explosion.append({
                'pos': [x, y],
                'vel': [random.uniform(-4, 4), random.uniform(-4, 4)],
                'size': random.randint(3, 8),
                'lifetime': random.randint(30, 60),
                'color': random.choice([ROJO, NARANJA_FUEGO, AMARILLO_CLARO, GRIS])
            })
        # cap
        if len(particulas_explosion) > MAX_PARTICULAS_EXP:
            particulas_explosion = particulas_explosion[:MAX_PARTICULAS_EXP]

    for p in particulas_explosion[:]:
        p['pos'][0] += p['vel'][0]
        p['pos'][1] += p['vel'][1]
        p['lifetime'] -= 1
        if p['lifetime'] > 0:
            s = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            alpha = int(255 * (p['lifetime'] / 60))
            color_c = (p['color'][0], p['color'][1], p['color'][2], alpha)
            pygame.draw.circle(s, color_c, (p['size'], p['size']), p['size'])
            pantalla.blit(s, (p['pos'][0] - p['size'], p['pos'][1] - p['size']))
        else:
            particulas_explosion.remove(p)

    # Si terminamos la explosión y estamos en estado TERMINADO, pasamos a cargar nivel
    if estado_juego == "TERMINADO" and not particulas_explosion:
        if nivel_final_game_over <= 0:
            estado_juego = "GAME_OVER"
            carga_progreso = 0

def dibujar_barra_superior():
    """Dibuja la barra de HUD."""
    s = pygame.Surface((ANCHO, BARRA_ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    pantalla.blit(s, (0, 0))
    pygame.draw.line(pantalla, GRIS_OSCURO, (0, BARRA_ALTO - 1), (ANCHO, BARRA_ALTO - 1), 2)

    BTN_SIZE = 30
    SPACING = 5
    x_offset = 10
    y_center = 20

    btn_salir_rect = pygame.Rect(x_offset, SPACING, BTN_SIZE, BTN_SIZE)
    x_offset += BTN_SIZE + SPACING
    btn_reiniciar_rect = pygame.Rect(x_offset, SPACING, BTN_SIZE, BTN_SIZE)
    x_offset += BTN_SIZE + SPACING
    btn_pausa_rect = pygame.Rect(x_offset, SPACING, BTN_SIZE, BTN_SIZE)

    pygame.draw.rect(pantalla, BLANCO, btn_salir_rect, 1)
    pygame.draw.rect(pantalla, BLANCO, btn_reiniciar_rect, 1)
    pygame.draw.rect(pantalla, BLANCO, btn_pausa_rect, 1)

    texto_salir = fuente_iconos.render("X", True, ROJO)
    pantalla.blit(texto_salir, (btn_salir_rect.x + 8, btn_salir_rect.y + 4))

    texto_reiniciar = fuente_iconos.render("R", True, TURQUESA)
    pantalla.blit(texto_reiniciar, (btn_reiniciar_rect.x + 8, btn_reiniciar_rect.y + 4))

    texto_pausa = fuente_iconos.render("||", True, BLANCO if estado_juego == "JUGANDO" else AMARILLO)
    pantalla.blit(texto_pausa, (btn_pausa_rect.x + 8, btn_pausa_rect.y + 4))

    x_actual = ANCHO - 10

    ancho_barra_combustible = 60
    alto_barra_combustible = 15
    y_barra = y_center - alto_barra_combustible // 2

    x_actual -= ancho_barra_combustible
    x_barra = x_actual

    pygame.draw.rect(pantalla, BLANCO, (x_barra, y_barra, ancho_barra_combustible, alto_barra_combustible), 1)

    relleno_ancho = (combustible / 100) * (ancho_barra_combustible - 2)
    color_combustible = (0, 200, 0) if combustible > 20 else ROJO
    pygame.draw.rect(pantalla, color_combustible, (x_barra + 1, y_barra + 1, relleno_ancho, alto_barra_combustible - 2))

    combustible_label = fuente_pequena.render(f"COMBUSTIBLE: {int(combustible)}%", True, BLANCO)
    x_actual -= combustible_label.get_width() + 10
    pantalla.blit(combustible_label, (x_actual, y_center - combustible_label.get_height() // 2))

    vidas_text = fuente_pequena.render(f"VIDAS: {vidas}/{MAX_VIDAS}", True, BLANCO if vidas > 1 else ROJO)
    x_actual -= vidas_text.get_width() + 25
    pantalla.blit(vidas_text, (x_actual, y_center - vidas_text.get_height() // 2))

    puntaje_text = fuente_pequena.render(f"PUNTAJE: {puntaje}", True, AMARILLO)
    x_actual -= puntaje_text.get_width() + 25
    pantalla.blit(puntaje_text, (x_actual, y_center - puntaje_text.get_height() // 2))

    indice_planeta = (nivel - 1) % len(PLANETA_NOMBRES)
    nivel_display = PLANETA_NOMBRES[indice_planeta]
    color_nivel = PLANETA_COLORES_OCEANO[indice_planeta]
    nivel_text = fuente_pequena.render(f"NIVEL: {nivel_display} ({nivel}/{len(PLANETA_NOMBRES)})", True, color_nivel)
    x_actual -= nivel_text.get_width() + 25
    pantalla.blit(nivel_text, (x_actual, y_center - nivel_text.get_height() // 2))


# Inicial
dibujar_detalles_planeta_a_surface()
nebulosas = generar_nebulosas()

# Bucle Principal
while True:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if estado_juego == "MENU" and evento.key == pygame.K_RETURN:
                reiniciar_juego(mantener_nivel=True)

            if estado_juego in ("JUGANDO", "PAUSA") and evento.key == pygame.K_p:
                if estado_juego == "JUGANDO":
                    estado_anterior = "JUGANDO"
                    estado_juego = "PAUSA"
                elif estado_juego == "PAUSA":
                    estado_juego = estado_anterior

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                manejar_click_botones(evento.pos)

    # Lógica del juego
    if estado_juego == "JUGANDO":
        teclas = pygame.key.get_pressed()
        propulsando = False

        # Movimiento horizontal del planeta a niveles avanzados
        if nivel >= 2:
            planeta_velocidad_actual = PLANETA_VEL * (nivel * 0.5)
            planeta.x += planeta_dir * planeta_velocidad_actual

            LIMITE_IZQ = ANCHO * 0.1
            LIMITE_DER = ANCHO * 0.9 - planeta_radio * 2

            if planeta.x < LIMITE_IZQ:
                planeta_dir = 1
            elif planeta.x > LIMITE_DER:
                planeta_dir = -1

        # Movimiento del cohete (consumo)
        if teclas[pygame.K_LEFT] and combustible > 0:
            velocidad_x -= 0.2; combustible -= 0.1
        if teclas[pygame.K_RIGHT] and combustible > 0:
            velocidad_x += 0.2; combustible -= 0.1
        if teclas[pygame.K_UP] and combustible > 0:
            velocidad_y -= 0.3; combustible -= 0.2; propulsando = True

        velocidad_y += gravedad
        jugador.x += int(velocidad_x)
        jugador.y += int(velocidad_y)

        # Límite superior
        if jugador.y - 20 < LIMITE_SUPERIOR_JUEGO:
            jugador.y = LIMITE_SUPERIOR_JUEGO + 20
            velocidad_y = max(0, velocidad_y)

        # Límites de pantalla y pérdida por caída
        if jugador.x < 0:
            jugador.x = 0; velocidad_x = 0
        if jugador.x > ANCHO - jugador.width:
            jugador.x = ANCHO - jugador.width; velocidad_x = 0
        if jugador.y + jugador.height > ALTO:
            vidas -= 1
            if vidas <= 0:
                estado_juego = "TERMINADO"; explosion = True; resultado = "Caída libre fuera del límite de reingreso."; nivel_final_game_over = nivel
            else:
                reiniciar_juego(mantener_nivel=True)

        # Colisión con planeta (aterrizaje)
        if jugador.colliderect(planeta) and not explosion:
            if abs(velocidad_y) < 2 and abs(velocidad_x) < 2:
                puntaje += 100 * nivel
                if nivel < len(PLANETA_NOMBRES):
                    nivel += 1
                    estado_juego = "NIVEL_COMPLETADO"
                else:
                    nivel += 1
                    estado_juego = "TERMINADO"; resultado = "Sistema Solar Conquistado!"; nivel_final_game_over = nivel
            else:
                vidas -= 1
                if vidas <= 0:
                    estado_juego = "TERMINADO"; explosion = True; resultado = "Aterrizaje demasiado rápido. EXPLOSION!"; nivel_final_game_over = nivel
                else:
                    reiniciar_juego(mantener_nivel=True)

        # Actualización partículas de propulsión (movimiento y limpieza)
        for p in particulas_propulsion[:]:
            p['pos'][0] += p['vel'][0]; p['pos'][1] += p['vel'][1]; p['lifetime'] -= 1
            if p['lifetime'] <= 0:
                particulas_propulsion.remove(p)

        # Generación controlada de meteoritos y estrellas recolectables
        if len(meteoritos) < MAX_METEORITOS and random.randint(1, 50) < (nivel + 2):
            meteoritos.append(pygame.Rect(random.randint(0, ANCHO), BARRA_ALTO, 20, 20))
        if len(estrellas_comb) < MAX_ESTRELLAS_COMB and random.randint(1, 120) < 3:
            estrellas_comb.append(pygame.Rect(random.randint(0, ANCHO), BARRA_ALTO, 15, 15))

        # Movimiento meteoritos
        for m in meteoritos[:]:
            m.y += 4 + nivel
            if jugador.colliderect(m):
                vidas -= 1
                try:
                    meteoritos.remove(m)
                except ValueError:
                    pass
                if vidas <= 0:
                    estado_juego = "TERMINADO"; explosion = True; resultado = "Destruido por un meteorito."; nivel_final_game_over = nivel
            elif m.y > ALTO:
                meteoritos.remove(m); puntaje += 10

        # Movimiento estrellas recolectables
        for s in estrellas_comb[:]:
            s.y += 3
            if jugador.colliderect(s):
                combustible = min(100, combustible + 20)
                try:
                    estrellas_comb.remove(s)
                except ValueError:
                    pass
            elif s.y > ALTO:
                estrellas_comb.remove(s)

        if combustible <= 0:
            combustible = 0
            propulsando = False

         # Dibujo según estado del juego
    pantalla.fill(AZUL_PROFUNDO)

    dibujar_logo_superior()
    dibujar_nebulosas()

    # Estrellas de fondo
    for estrella in estrellas_fondo:
        estrella['pos'][1] += estrella['speed']
        if estrella['pos'][1] > ALTO:
            estrella['pos'][1] = 0
            estrella['pos'][0] = random.randint(0, ANCHO)
        pygame.draw.circle(pantalla, estrella['color'],
                           (int(estrella['pos'][0]), int(estrella['pos'][1])),
                           estrella['size'])

    # Estados del juego (importante)
    if estado_juego == "MENU":

        # --- TÍTULO ---
        titulo = fuente_enorme.render("NEXUS", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO/2 - titulo.get_width()/2, 240))

        # --- INSTRUCCIÓN PRINCIPAL ---
        instruccion = fuente_media.render("Presiona [ENTER] para iniciar la misión...", True, BLANCO)
        pantalla.blit(instruccion, (ANCHO/2 - instruccion.get_width()/2, ALTO/2))

        # --- INSTRUCCIONES DE JUEGO ---
        instrucciones = [
            
            "←  →   Mover la nave",
            "↑        Frenar y ascender"
        ]

        y = ALTO/2 + 80
        for linea in instrucciones:
            t = fuente_media.render(linea, True, AMARILLO)
            pantalla.blit(t, (ANCHO/2 - t.get_width()/2, y))
            y += 30


    elif estado_juego == "JUGANDO":

        # Dibujos del juego 
        dibujar_planeta()

        # Dibujar partículas de propulsión
        for p in particulas_propulsion:
            s = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            alpha = int(255 * (p['lifetime'] / 30))
            color_c = (p['color'][0], p['color'][1], p['color'][2], alpha)
            pygame.draw.circle(s, color_c, (p['size'], p['size']), p['size'])
            pantalla.blit(s, (p['pos'][0] - p['size'], p['pos'][1] - p['size']))

        # Explosión o cohete
        if explosion or estado_juego == "TERMINADO":
            dibujar_explosion(jugador.centerx, jugador.centery)
        else:
            dibujar_cohete(jugador.centerx, jugador.y + jugador.height//2 - 20, propulsando)

        # Dibujar meteoritos
        for m in meteoritos:
            pygame.draw.circle(pantalla, GRIS, m.center, m.width//2)

        # Dibujar estrellas recolectables
        for s in estrellas_comb:
            pygame.draw.circle(pantalla, AMARILLO, s.center, 8)

        dibujar_barra_superior()


    elif estado_juego == "PAUSA":

        dibujar_planeta()
        dibujar_cohete(jugador.centerx, jugador.y + jugador.height//2 - 20, False)
        dibujar_barra_superior()

        pausa_bg = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        pausa_bg.fill((0, 0, 0, 150))
        pantalla.blit(pausa_bg, (0, 0))

        pausa_texto = fuente_enorme.render("PAUSA", True, AMARILLO)
        subtitulo = fuente_media.render("Presiona [P] para reanudar", True, BLANCO)

        pantalla.blit(pausa_texto, (ANCHO//2 - pausa_texto.get_width()//2, ALTO//2 - 100))
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, ALTO//2))


    elif estado_juego == "NIVEL_COMPLETADO":

        dibujar_planeta()
        dibujar_barra_superior()

        nivel_bg = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        nivel_bg.fill((0, 0, 0, 150))
        pantalla.blit(nivel_bg, (0, 0))

        idx_siguiente = (nivel - 1) % len(PLANETA_NOMBRES)
        mundo_siguiente_nombre = PLANETA_NOMBRES[idx_siguiente]
        color_siguiente = PLANETA_COLORES_OCEANO[idx_siguiente]

        titulo_desbloqueado = fuente_grande.render("NIVEL COMPLETADO", True, TURQUESA)
        mensaje_bienvenida = fuente_media.render(f"Próxima Misión: {mundo_siguiente_nombre}", True, color_siguiente)

        y_title = ALTO//2 - 150
        pantalla.blit(titulo_desbloqueado, (ANCHO//2 - titulo_desbloqueado.get_width()//2, y_title))
        y_title += titulo_desbloqueado.get_height() + 20
        pantalla.blit(mensaje_bienvenida, (ANCHO//2 - mensaje_bienvenida.get_width()//2, y_title))

        BTN_ANCHO, BTN_ALTO = 200, 50
        BTN_Y = ALTO // 2 + 100
        BTN_SPACING = 30

        btn_siguiente_rect = pygame.Rect(ANCHO // 2 - BTN_ANCHO - BTN_SPACING // 2, BTN_Y, BTN_ANCHO, BTN_ALTO)
        btn_salir_mision_rect = pygame.Rect(ANCHO // 2 + BTN_SPACING // 2, BTN_Y, BTN_ANCHO, BTN_ALTO)

        pygame.draw.rect(pantalla, (0, 150, 0), btn_siguiente_rect, 0, 10)
        pygame.draw.rect(pantalla, BLANCO, btn_siguiente_rect, 2, 10)
        texto_siguiente = fuente.render("Siguiente Misión", True, BLANCO)
        pantalla.blit(texto_siguiente, (btn_siguiente_rect.centerx - texto_siguiente.get_width() // 2,
                                        btn_siguiente_rect.centery - texto_siguiente.get_height() // 2))

        pygame.draw.rect(pantalla, ROJO, btn_salir_mision_rect, 0, 10)
        pygame.draw.rect(pantalla, BLANCO, btn_salir_mision_rect, 2, 10)
        texto_salir_mision = fuente.render("Finalizar Misión", True, BLANCO)
        pantalla.blit(texto_salir_mision, (btn_salir_mision_rect.centerx - texto_salir_mision.get_width() // 2,
                                           btn_salir_mision_rect.centery - texto_salir_mision.get_height() // 2))

    elif estado_juego == "TERMINADO":

        if not particulas_explosion:
            if nivel_final_game_over > len(PLANETA_NOMBRES):
                game_over_text = fuente_enorme.render("VICTORIA", True, TURQUESA)
                subtitulo = fuente.render("Misión completada. Reiniciando...", True, BLANCO)
            else:
                game_over_text = fuente_enorme.render("GAME OVER", True, ROJO)
                subtitulo = fuente.render("Regresando al Nivel 1...", True, BLANCO)

            resultado_final_text = fuente_media.render(resultado, True, BLANCO)
            puntaje_final_text = fuente.render(f"Puntaje Total: {puntaje_final_game_over}", True, AMARILLO)

            y_pos = ALTO//2 - 150

            pantalla.blit(game_over_text, (ANCHO//2 - game_over_text.get_width()//2, y_pos))
            y_pos += game_over_text.get_height() + 10

            pantalla.blit(resultado_final_text, (ANCHO//2 - resultado_final_text.get_width()//2, y_pos))
            y_pos += resultado_final_text.get_height() + 30

            pantalla.blit(puntaje_final_text, (ANCHO//2 - puntaje_final_text.get_width()//2, y_pos))
            y_pos += puntaje_final_text.get_height() + 30

            pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, y_pos))

            pygame.display.flip()

            decision = mostrar_game_over()

            if decision == "continuar":
                nivel = max(1, nivel_final_game_over)
                reiniciar_juego(mantener_nivel=True)
                estado_juego = "JUGANDO"
            else:
                estado_juego = "MENU"


    elif estado_juego == "CARGANDO_NIVEL":
        dibujar_carga_suspensiva(carga_progreso)

    # Fin de estados del juego
    pygame.display.flip()
    clock.tick(60)
