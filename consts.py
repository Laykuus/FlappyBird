import pygame

DISPLAY_SIZE = (550, 850)
TICK_EVENT = pygame.USEREVENT + 1
NEW_PIPES_EVENT = pygame.USEREVENT + 2
BACKGROUND_SPRITE = pygame.transform.scale(pygame.image.load("./assets/background.png"), DISPLAY_SIZE)
LOWER_PIPE_SPRITE = pygame.transform.scale(pygame.image.load("./assets/lower_pipe.png"), [80, 450])
UPPER_PIPE_SPRITE = pygame.transform.scale(pygame.image.load("./assets/upper_pipe.png"), [80, 450])
X_PIPES_VELOCITY = -3.6