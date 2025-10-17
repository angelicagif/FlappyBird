import pygame
from pygame.locals import *
import random
import os
import json

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Kirby')
icon = pygame.image.load('FlappyBird/assets/sprites/player/kirby/kirby2.png')
pygame.display.set_icon(icon)

# define font
font = pygame.font.SysFont('04b_19', 40)
# define colours
white = (255, 255, 255)

# load images
bg = pygame.image.load('FlappyBird/assets/sprites/background/bg_gay.png')
ground_img = pygame.image.load('FlappyBird/assets/sprites/background/ground.png')
start1 = pygame.image.load('FlappyBird/assets/sprites/ui/start1.png')
start2 = pygame.image.load('FlappyBird/assets/sprites/ui/start2.png')
button_restart_img = pygame.image.load('FlappyBird/assets/sprites/ui/restart.png')
end_img = pygame.image.load('FlappyBird/assets/sprites/ui/gameover.png')
scoreboard_img = pygame.image.load('FlappyBird/assets/sprites/ui/score_board.png')
bronze_img = pygame.image.load('FlappyBird/assets/sprites/ui/bronze.png')
silver_img = pygame.image.load('FlappyBird/assets/sprites/ui/silver.png')
gold_img = pygame.image.load('FlappyBird/assets/sprites/ui/gold.png')
platinum_img = pygame.image.load('FlappyBird/assets/sprites/ui/platinum.png')
fail_img = pygame.image.load('FlappyBird/assets/sprites/ui/fail.png')

# load sounds
s = 'FlappyBird/assets/sounds/player'
s_flap = pygame.mixer.Sound(os.path.join(s, 'sfx_flap.wav'))
s_hit = pygame.mixer.Sound(os.path.join(s, 'sfx_hit.wav'))
s_die = pygame.mixer.Sound(os.path.join(s, 'sfx_die.wav'))
s_point = pygame.mixer.Sound(os.path.join(s, 'sfx_point.wav'))


# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
show_start_screen = True
start_time = pygame.time.get_ticks()
current_start_img = start1
special_pipe = None
medal = None

# load highscore
score_path = 'FlappyBird/score.json'
if os.path.exists(score_path):
    with open(score_path, 'r') as file:
        data = json.load(file)
        high_score = data.get("high_score", 0)
else:
    high_score = 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    global scroll_speed, show_start_screen
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    scroll_speed = 4
    score = 0
    show_start_screen = True
    return score


# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img = pygame.image.load(f'FlappyBird/assets/sprites/player/kirby/kirby{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            keys = pygame.key.get_pressed()
            if (pygame.mouse.get_pressed()[0] == 1 or keys[K_SPACE]) and not self.clicked:
                self.clicked = True
                self.vel = -10
                pygame.mixer.Sound.play(s_flap)
            if pygame.mouse.get_pressed()[0] == 0 and not keys[K_SPACE]:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('FlappyBird/assets/sprites/obstacle/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 1.5)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 1.5)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


# Button class
class Button_reset():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# create sprite groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# create restart button
button = Button_reset(screen_width // 2 - 50, screen_height // 2 - 100, button_restart_img)


# medal animation vars
sparkle_alpha = 255
sparkle_direction = -5
medal_visible = True
spinning = False
spin_angle = 0
spin_scale = 1.0

# main loop
run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # assign medals
    if score <= 10:
        medal = fail_img
    elif score >= 11 and score <= 15:    
        medal = bronze_img
    elif score >= 16 and score <=30:
        medal = silver_img
    elif score >= 31 and scre <=60:
        medal = gold_img
    else:
        medal = platinum_img

    # start screen
    if show_start_screen:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 500:
            current_start_img = start2 if current_start_img == start1 else start1
            start_time = current_time
        screen.blit(current_start_img, (screen_width // 2 - 210, screen_height // 2 - 200))
        draw_text("Made by Angelica", font, white, screen_width // 2 - 160, screen_height // 2 + 250)

    screen.blit(ground_img, (ground_scroll, 768))

    # scoring
    if len(pipe_group) > 0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and
                bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and not pass_pipe):
            pass_pipe = True
        if pass_pipe and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score += 1
            pygame.mixer.Sound.play(s_point)
            scroll_speed += 0.05
            pass_pipe = False

    # collisions
    if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0) and not game_over:
        pygame.mixer.Sound.play(s_hit)
        game_over = True

    # when bird hits the ground
    if flappy.rect.bottom >= 768:
        if flying:  # means bird was still moving
            pygame.mixer.Sound.play(s_die)
            flying = False
        game_over = True


    # gameplay
    if not game_over and flying:
        time_now = pygame.time.get_ticks()
        adjusted_frequency = int(pipe_frequency * (4 / scroll_speed))
        if time_now - last_pipe > adjusted_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            if score == high_score - 3 and special_pipe is None:
                special_pipe = btm_pipe
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

        # spinning medal effect
        if special_pipe and special_pipe.alive() and medal_visible:
            medal_rect = medal.get_rect(midbottom=(special_pipe.rect.centerx, special_pipe.rect.top - 50))

            if not spinning:
                # idle medal pulse before spin
                medal_idle = medal.copy()
                medal_idle.set_alpha(sparkle_alpha)
                screen.blit(medal_idle, medal_rect)

                sparkle_alpha += sparkle_direction
                if sparkle_alpha <= 100 or sparkle_alpha >= 255:
                    sparkle_direction *= -1
                    sparkle_alpha = max(100, min(255, sparkle_alpha))

                # start spin when bird passes through medal
                if flappy.rect.left > special_pipe.rect.centerx - 10:
                    spinning = True
                    spin_angle = 0
                    spin_scale = 1.0
            else:
                # 3D spin animation
                spin_angle += 20
                if spin_angle >= 360:
                    spin_angle = 0
                    medal_visible = False
                    spinning = False
                else:
                    spin_scale = abs(pygame.math.Vector2(1, 0).rotate(spin_angle).x)
                    spin_scale = max(0.1, spin_scale)

                    w, h = medal.get_size()
                    scaled_width = max(1, int(w * spin_scale))
                    scaled_medal = pygame.transform.scale(medal, (scaled_width, h))
                    rotated_medal = pygame.transform.rotate(scaled_medal, spin_angle)
                    new_rect = rotated_medal.get_rect(center=medal_rect.center)
                    screen.blit(rotated_medal, new_rect)

        else:
            # reset state
            special_pipe = None
            medal_visible = True
            sparkle_alpha = 255
            sparkle_direction = -5
            spinning = False
            spin_angle = 0
            spin_scale = 1.0

    # game over screen
    if game_over:
        screen.blit(end_img, (screen_width // 2 - 170, screen_height // 2 - 200))
        screen.blit(scoreboard_img, (screen_width // 2 - 225, screen_height // 2 - 50))
        screen.blit(medal, (screen_width // 2 - 160, screen_height // 2 + 36))
        draw_text(str(score), font, white, screen_width // 2 + 140, screen_height // 2 + 25)
        if score > high_score:
            high_score = score
            with open(score_path, 'w') as file:
                json.dump({"high_score": high_score}, file)
        draw_text(str(high_score), font, white, screen_width // 2 + 140, screen_height // 2 + 110)
        if button.draw():
            game_over = False
            score = reset_game()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE)) and not flying and not game_over:
            flying = True
            show_start_screen = False



    pygame.display.update()

pygame.quit()
