import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.mixer.init()
pygame.init()

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
# Instead of a surface, use an image for a better-looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('jet.png').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
    # Move sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
            move_up_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
            move_down_sound.play()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)       
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        # Random starting position
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < 0:
            self.kill()

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load('Apoxode_-_Electric_1.mp3')
# Setting loops to -1 makes the loop never end
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound('Rising_putter.ogg')
move_down_sound = pygame.mixer.Sound('Falling_putter.ogg')
collision_sound = pygame.mixer.Sound('Collision.ogg')

# Define constants for screen H/W
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Create the screen object - you control the surface and 
#   OS controls window borders and title bar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup clock for framerate reasons later
clock = pygame.time.Clock()

# USEREVENT is the last event pygame reserves, so adding 1 ensures its unique
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate player - before this line it is just a rectangle
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# MAIN LOOP
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        # Add new enemy?
        elif event.type == ADDENEMY:
            # Create new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        # Add new cloud?
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    # Get all keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update player sprite based on user keypresses
    player.update(pressed_keys)
    
    # Update enemies and clouds
    enemies.update()
    clouds.update()

    screen.fill((135,206,250))

    # Draw sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # Stop the music
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Exit the window
        running = False

    # Update display
    pygame.display.flip()

    # Ensure 30 fps
    clock.tick(30)