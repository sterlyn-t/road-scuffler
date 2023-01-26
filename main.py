import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define variables
# Colours
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Fighter Clone")

# Loading images
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Loading audio
pygame.mixer.music.load('assets/audio/music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound('assets/audio/sword.wav')
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound('assets/audio/magic.wav')
magic_fx.set_volume(0.75)



# Defining number of frames in each sheet
WARRIOR_ANIMATION_FRAMES = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_FRAMES = [8, 8, 1, 8, 8, 3, 7]

# Defining font
count_font = pygame.font.Font('assets/fonts/turok.ttf', 80)
score_font = pygame.font.Font('assets/fonts/turok.ttf', 30)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Drawing background
def draw_background():
    scaled_background = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_background, (0, 0))

# Drawing health bars
def draw_health_bars(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


run_game = True

# Create fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_FRAMES, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_FRAMES, magic_fx)

while run_game:
    clock.tick(FPS)
    draw_background()
    draw_health_bars(fighter_1.health, 20, 20)
    draw_health_bars(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    if intro_count <= 0:
        # Move fighters
        fighter_1.move(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, surface=screen, target=fighter_2, round_over=round_over)
        fighter_2.move(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, surface=screen, target=fighter_1, round_over=round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Checking for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else: 
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_FRAMES, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_FRAMES, magic_fx)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    
    # Updating display
    pygame.display.update()

pygame.quit()