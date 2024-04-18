import pygame
import os
import time

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
MAX_BULLETS = 1
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'bg.jpg')), (WIDTH, HEIGHT))


GUN_SOUND_YELLOW = pygame.mixer.Sound('./Assets/Gun+Silencer.mp3')
GUN_SOUND_RED = pygame.mixer.Sound('./Assets/Gun+Silencer.mp3')


def draw_window(red, yellow, red_health, yellow_health, countdown, can_shoot):
    WIN.blit(SPACE, (0, 0))

    WIN.blit(YELLOW_SPACESHIP, (10, HEIGHT - SPACESHIP_HEIGHT - 10))
    WIN.blit(RED_SPACESHIP, (WIDTH - SPACESHIP_WIDTH - 10, HEIGHT - SPACESHIP_HEIGHT - 10))

    countdown_text = FONT.render(
        "Countdown: " + str(countdown), 1, WHITE)
    WIN.blit(countdown_text, (WIDTH/2 - countdown_text.get_width()/2, 10))

    if can_shoot:
        shoot_text = FONT.render("SHOOT WHEN READY!", 1, WHITE)
        WIN.blit(shoot_text, (WIDTH/2 - shoot_text.get_width()/2, HEIGHT - shoot_text.get_height() - 10))

    pygame.display.update()


def handle_bullets(yellow, red, yellow_last_fire, red_last_fire):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RCTRL] and time.time() - yellow_last_fire > 0.5:
        yellow_last_fire = time.time()
        GUN_SOUND_YELLOW.play()  

    if keys[pygame.K_LCTRL] and time.time() - red_last_fire > 0.5:
        red_last_fire = time.time()
        GUN_SOUND_RED.play()  

    return yellow_last_fire, red_last_fire


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    red = pygame.Rect(WIDTH - SPACESHIP_WIDTH - 10, HEIGHT - SPACESHIP_HEIGHT - 10, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(10, HEIGHT - SPACESHIP_HEIGHT - 10, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    countdown = 3
    countdown_start = time.time()

    yellow_last_fire = 0
    red_last_fire = 0

    can_shoot = False  

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if countdown > 0:
            if time.time() - countdown_start >= 1:
                countdown -= 1
                countdown_start = time.time()

        elif countdown == 0:
            can_shoot = True  
            yellow_last_fire, red_last_fire = handle_bullets(yellow, red, yellow_last_fire, red_last_fire)

            if yellow_last_fire < red_last_fire:
                draw_winner("Yellow Wins!")
                break
            elif red_last_fire < yellow_last_fire:
                draw_winner("Red Wins!")
                break
            
            

        draw_window(red, yellow, 0, 0, countdown, can_shoot)

    main()


if __name__ == "__main__":
    main()
