import pygame
import random
from sys import exit


pygame.init()
clock = pygame.time.Clock()

# Window setting
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 551

center_W = WINDOW_WIDTH // 2
center_H = WINDOW_HEIGHT // 2


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


#색
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#name
pygame.display.set_caption("Flappy bird")

#font
font = pygame.font.SysFont('arial', 30)


# Images
bird_images = [pygame.image.load("assets/bird_1.png"), 
pygame.image.load("assets/bird_2.png"), 
pygame.image.load("assets/bird_3.png")]

ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_1.png")
bottom_pipe_image = pygame.image.load("assets/pipe_2.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

skyline_image_1 = pygame.image.load("assets/background_1.png")
skyline_image_2 = pygame.image.load("assets/background_2.png")
skyline_image_3 = pygame.image.load("assets/background_3.png")

#Sound
pygame.mixer.music.load('assets/bgm.mp3')
pygame.mixer.music.play(-1) 
jump_sound = pygame.mixer.Sound('assets/jump.mp3')
game_over_sound = pygame.mixer.Sound('assets/ending.mp3')

# Game

score = 0
bird_pos = (200, 260)
game_over = True
game_speed= 2

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image      
        self.rect = self.image.get_rect() 
        self.rect.x, self.rect.y = x, y

    def update(self):
        #ground moves (game speed)
        self.rect.x -= game_speed
        if self.rect.x <= -WINDOW_WIDTH:
            self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_pos
        self.image_index = 0
        self.mov = 0
        self.alive = True

    def update(self, u_input):
        # bird's moving
        if self.alive:
            self.image_index += 1
            self.image = bird_images[self.image_index % 3]

        #gravity, bird is moving
        self.mov += 0.5

        #gravity acts until it touches the ground
        if self.rect.y < 570:
            self.rect.y += (self.mov)

        if self.mov > 5:
            self.mov = 5

        #bird's jump when SPACE is pressed
        if u_input[pygame.K_SPACE] and self.alive:
            jump_sound.play()
            if self.rect.y > 0:
                self.mov = -3
                
                


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Move Pipe
        self.rect.x -= game_speed
        if self.rect.x <= -WINDOW_WIDTH:
            self.kill()

        global score

        #counting score
        if bird_pos[0] > self.rect.topleft[0] and bird_pos[0] < self.rect.topright[0]:
            score += 1/50
        

                

def gaming():
    global score

    # initialize bird, pipes, ground Sprite.

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipe_spawn_time = 0
    pipes = pygame.sprite.Group()

    #First ground in game 
    x_pos_ground, y_pos_ground = 0, 600
    ground = pygame.sprite.Group()
    
    ground.add(Ground(x_pos_ground, y_pos_ground))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        
        # Making map change
        score_copy = score 
        
        if score_copy / 30 > 1:
            score_copy = score - 30 * round(score_copy / 30)

        if 0<= score_copy< 10:
            screen.blit(skyline_image_1, (0, 0))
        if 10 <= score_copy <20:
            screen.blit(skyline_image_2, (0, 0))
        if 20 <= score_copy <30:
            screen.blit(skyline_image_3, (0, 0))

        # spawn ground
        if len(ground) <= 2:
            ground.add(Ground(WINDOW_WIDTH, y_pos_ground))
        
        u_input = pygame.key.get_pressed()
        
        pipes.draw(screen)

        #Score interface
        score_text = font.render(f'SCORE: {round(score)}', True, WHITE)
        screen.blit(score_text, (20, 20))

        ground.draw(screen)
        bird.draw(screen)

        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(u_input)

        #Game over
        colli_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        colli_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)

        if colli_pipes or colli_ground:
            #bird die and game stop
            bird.sprite.alive = False

            #game over interface
            screen.blit(game_over_image, (center_W - game_over_image.get_width() // 2,
                                            center_H - game_over_image.get_height() // 2))
            game_over_sound.play()
            if u_input[pygame.K_r]:
                #restart interface
                score = 0
                break

        # making pipes
        if pipe_spawn_time <= 0 and bird.sprite.alive:
            x_top, x_bottom = 700, 700
            y_top = random.randint(-800, -480)
            y_bottom = y_top + random.randint(80, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image))
            pipe_spawn_time = random.randint(60, 180)
        pipe_spawn_time -= 1

        clock.tick(60)
        pygame.display.update()


while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Game start interface
    screen.fill((0, 0, 0))
    screen.blit(skyline_image_1, (0, 0))
    screen.blit(ground_image, Ground(0, 600))
    screen.blit(bird_images[0], (200, 260))
    screen.blit(start_image, (center_W - start_image.get_width() // 2,
                                center_H - start_image.get_height() // 2))

    # keyboard input
    u_input = pygame.key.get_pressed()

    if u_input[pygame.K_SPACE]:
        gaming()


    pygame.display.update()


