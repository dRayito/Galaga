# Importaciones necesarias para el juego
import pygame, random
import os

# TAMAÑO DEL LIENZO
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, 'assets')

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GALAGA')
clock = pygame.time.Clock()

# Clase Bullet (Bala)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Tamaño pequeño para la bala
        self.image.fill(WHITE)  # Color blanco para la bala
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10  # Velocidad hacia arriba

    def update(self):
        self.rect.y += self.speedy
        # Eliminar la bala si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

# Clase Player (Jugador)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'jugador.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10 
        self.speed_x = 0
        self.shoot_delay = 250  # Retardo entre disparos en ms
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3  # Inicializamos con 3 vidas
    
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
    
    def reset_position(self):
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10  # Reinicia la posición de la nave

# Clase Meteor (Asteroide)
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'asteroid.png'))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

# Cargar fondo
background = pygame.image.load(os.path.join(IMAGE_DIR, 'fondo.png')).convert()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear el jugador y añadirlo al grupo de sprites
player = Player()
all_sprites.add(player)

# Crear meteoritos y añadirlos al grupo de sprites
for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

running = True
while running:
    clock.tick(60)  # Limita la tasa de actualización del juego a 60 fotogramas por segundo
    for event in pygame.event.get():  # Escucha eventos del teclado o de la ventana
        if event.type == pygame.QUIT:  # Si el usuario cierra la ventana
            running = False  # Termina el bucle del juego
        elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
            if event.key == pygame.K_SPACE:  # Si se presiona la barra espaciadora
                player.shoot()  # El jugador dispara
    
    all_sprites.update()  # Actualiza todos los sprites
    
    # Colisiones balas-meteoros
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        meteor = Meteor()  # Crea un nuevo meteorito
        all_sprites.add(meteor)  # Lo añade al grupo de sprites
        meteor_list.add(meteor)  # Lo añade al grupo de meteoritos
    
    # Colisiones jugador-meteoros
    hits_player = pygame.sprite.spritecollide(player, meteor_list, True)  # Colisión entre jugador y meteoritos
    for hit in hits_player:
        player.lives -= 1  # Resta una vida al jugador
        player.reset_position()  # Reinicia la posición de la nave
        if player.lives <= 0:  # Si el jugador se queda sin vidas
            running = False  # Termina el juego

    screen.blit(background, [0, 0])  # Dibuja el fondo
    all_sprites.draw(screen)  # Dibuja todos los sprites en la pantalla
    
    # Mostrar las vidas del jugador en la pantalla
    font = pygame.font.SysFont("Arial", 24)  # Establece la fuente para mostrar las vidas
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)  # Crea el texto con las vidas
    screen.blit(lives_text, (10, 10))  # Dibuja las vidas en la esquina superior izquierda
    
    pygame.display.flip()  # Actualiza la pantalla

pygame.quit()  # Sale del juego
 

