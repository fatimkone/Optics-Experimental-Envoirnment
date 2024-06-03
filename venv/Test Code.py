import pygame
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode([1000,1000],pygame.RESIZABLE)
pygame.draw.rect(screen, (255,255,255), pygame.Rect(30, 30, 60, 60))
running=True
while running:


    screen.fill((0,0,0))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()