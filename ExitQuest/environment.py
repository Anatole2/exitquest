import pygame

class Environment:
    def __init__(self, grid, cell_size=40):
        self.grid = grid
        self.cell_size = cell_size
        self.size = grid.shape[0]
        self.window = pygame.display.set_mode((self.size * cell_size, self.size * cell_size))

    def display_path(self, path):
        for position in path:
            x, y = position
            self.grid[x][y] = 4  # Marquer le chemin
        self.render()

    def render(self):
        self.window.fill((255, 255, 255))
        for x in range(self.size):
            for y in range(self.size):
                color = (0, 0, 0)  # Mur noir par défaut
                if self.grid[x, y] == 0:
                    color = (255, 255, 255)  # Blanc chemin vide
                elif self.grid[x, y] == 2:
                    color = (0, 255, 0)  # Vert départ
                elif self.grid[x, y] == 3:
                    color = (255, 0, 0)  # Rouge arrivée
                elif self.grid[x, y] == 4:
                    color = (0, 0, 255)  # Bleu chemin emprunté par l'agent
                pygame.draw.rect(self.window, color, 
                                (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()
