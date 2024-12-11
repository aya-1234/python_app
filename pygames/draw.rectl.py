import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300)) # Corrected dimensions - remove the period
pygame.display.set_caption("Just Window")
FPSCLOCK = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        SURFACE.fill((255,255,255))
        
        pygame.draw.rect(SURFACE,(255,0,0)),(10,20,100,50)
        
        pygame.draw.rect(SURFACE,(255,0,0),(150,10,100,30).3)