import pygame, obj, random
from consts import *

pygame.init()
screen = pygame.display.set_mode(DISPLAY,  pygame.DOUBLEBUF | pygame.HWSURFACE)
clock = pygame.time.Clock()
Bird = obj.Bird()
running = True
paused = False
pygame.time.set_timer(TICK_EVENT, 15)
pygame.time.set_timer(NEW_PIPES_EVENT, 1500)
score = 0
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 100)
PIXEL_FONT = pygame.font.Font("./assets/DePixelHalbfett.otf", 50)
paused_txt = BIG_FONT.render("PAUSED", True, "black")

rdm_upper_pipe_y = random.randint(-170, -80)
lower_pipe_y = rdm_upper_pipe_y - 260
PIPES = [
    [
        obj.Pipe([DISPLAY_SIZE[0], rdm_upper_pipe_y], UPPER_PIPE_SPRITE),
        obj.Pipe([DISPLAY_SIZE[0], DISPLAY_SIZE[1] + lower_pipe_y], LOWER_PIPE_SPRITE)
    ]
]

background_sprites = [
    [BACKGROUND_SPRITE, [0, 0]],
    [BACKGROUND_SPRITE, [DISPLAY[0], 0]]
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                paused = False
                Bird = obj.Bird()
                score = 0

                rdm_upper_pipe_y = random.randint(-170, -80)
                lower_pipe_y = rdm_upper_pipe_y - 260
                PIPES = [
                    [
                        obj.Pipe([DISPLAY_SIZE[0], rdm_upper_pipe_y], UPPER_PIPE_SPRITE),
                        obj.Pipe([DISPLAY_SIZE[0], DISPLAY_SIZE[1] + lower_pipe_y], LOWER_PIPE_SPRITE)
                    ]
                ]
                background_sprites = [
                    [BACKGROUND_SPRITE, [0, 0]],
                    [BACKGROUND_SPRITE, [DISPLAY[0], 0]]
                ]
                pygame.time.set_timer(TICK_EVENT, 15)
                pygame.time.set_timer(NEW_PIPES_EVENT, 1500)

            elif event.key == pygame.K_p:
                if paused: paused = False
                else: paused = True
        
        if not Bird.is_dead and not paused:
            if event.type == NEW_PIPES_EVENT:
                # Pipes
                rdm_upper_pipe_y = random.randint(-170, -80)
                lower_pipe_y = rdm_upper_pipe_y - 260

                PIPES.append([
                    obj.Pipe([DISPLAY_SIZE[0], rdm_upper_pipe_y], UPPER_PIPE_SPRITE),
                    obj.Pipe([DISPLAY_SIZE[0], DISPLAY_SIZE[1] + lower_pipe_y], LOWER_PIPE_SPRITE)
                ])

                while PIPES[0][0].rect.topleft[0] < 0:
                    PIPES.pop(0)

            if event.type == TICK_EVENT:
                score += 0.2
                Bird.apply_gravity()
                
                # Background
                for i in range(len(background_sprites)):
                    background_sprites[i][1][0] += X_BACKGROUND_VELOCITY
                
                if background_sprites[0][1][0] == -BACKGROUND_SIZE[0]:
                    background_sprites.pop(0)
                    background_sprites.append([BACKGROUND_SPRITE, [DISPLAY[0], 0]])
                    
                
                for pipes in PIPES:
                    pipes[0].rect.topleft = [pipes[0].rect.topleft[0] + X_PIPES_VELOCITY, pipes[0].rect.topleft[1]]
                    pipes[1].rect.topleft = [pipes[1].rect.topleft[0] + X_PIPES_VELOCITY, pipes[1].rect.topleft[1]]

                    bird_mask = pygame.mask.from_surface(Bird.sprite)
                    upper_pipe_mask = pygame.mask.from_surface(pipes[0].sprite)
                    lower_pipe_mask = pygame.mask.from_surface(pipes[1].sprite)
                    
                    if bird_mask.overlap_area(upper_pipe_mask, (pipes[0].rect.topleft[0] - Bird.rect.topleft[0], pipes[0].rect.topleft[1] - Bird.rect.topleft[1])) > 0:
                        Bird.is_dead = True
                    elif bird_mask.overlap_area(lower_pipe_mask, (pipes[1].rect.topleft[0] - Bird.rect.topleft[0], pipes[1].rect.topleft[1] - Bird.rect.topleft[1])) > 0:
                        Bird.is_dead = True


                    #if Bird.rect.colliderect(pipes[0].rect) or Bird.rect.colliderect(pipes[1].rect):
                    #    Bird.is_dead = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                Bird.y_velocity = 10
        elif Bird.is_dead:
            Bird.dead_anim()

    #fps = FONT.render(str(int(clock.get_fps())), True, (255, 255, 255), None)
    score_txt = PIXEL_FONT.render(f"{int(score)}m", True, "white")
    score_txt_rect = score_txt.get_rect(center=(DISPLAY_SIZE[0]//2, 40))

    #screen.blit(BACKGROUND_SPRITE, [0, 0])
    screen.blits(background_sprites)

    for pipes in PIPES:
        screen.blits([
            [pipes[0].sprite, pipes[0].rect.topleft],
            [pipes[1].sprite, pipes[1].rect.topleft]
        ])
    
    screen.blits([
        [Bird.sprite, Bird.rect.topleft],
        [score_txt, score_txt_rect]
    ])
    pygame.display.flip()

    clock.tick_busy_loop(60)

pygame.quit()