import pygame
import numpy as np

# Paramètres
GRID_SIZE = 11
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Départ
RED = (255, 0, 0)   # Sortie

# Nouveau labyrinthe
labyrinthe = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("ExitQuest")

# Point de départ et de sortie
labyrinthe[1][1] = 2  # Départ
labyrinthe[9][9] = 3  # Sortie

def draw_grid(labyrinthe):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if labyrinthe[y][x] == 1:  # Mur
                pygame.draw.rect(screen, BLACK, rect)
            elif labyrinthe[y][x] == 2:  # Départ
                pygame.draw.rect(screen, BLUE, rect)
            elif labyrinthe[y][x] == 3:  # Sortie
                pygame.draw.rect(screen, RED, rect)
            else:  # Chemin
                pygame.draw.rect(screen, WHITE, rect)

def main():
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill(BLACK)
        draw_grid(labyrinthe)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
