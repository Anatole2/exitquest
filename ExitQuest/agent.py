import numpy as np
import heapq
import random

class HybridAgent:
    def __init__(self, grid, goal, alpha=0.1, gamma=0.9):
        self.grid = grid
        self.goal = goal
        self.position = (0, 0)  # Départ toujours en haut à gauche
        self.q_table = {}  # Q-table initialisée comme un dictionnaire
        self.visited = set()  # Suivi des cases visitées
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur de réduction des récompenses futures

    def get_neighbors(self, pos):
        """Retourne les voisins valides (non-obstacles) autour d'une position donnée."""
        x, y = pos
        neighbors = []
        if x > 0 and self.grid[x - 1, y] != 1:  # Haut
            neighbors.append((x - 1, y))
        if x < self.grid.shape[0] - 1 and self.grid[x + 1, y] != 1:  # Bas
            neighbors.append((x + 1, y))
        if y > 0 and self.grid[x, y - 1] != 1:  # Gauche
            neighbors.append((x, y - 1))
        if y < self.grid.shape[1] - 1 and self.grid[x, y + 1] != 1:  # Droite
            neighbors.append((x, y + 1))
        return neighbors

    def actions_valides(self, state):
        """Retourne toutes les actions valides (voisins possibles)."""
        return self.get_neighbors(state)

    def actionChoisie(self, x, y):
        """Choisit une action basée sur Q-learning ou A* si nécessaire."""
        state = (x, y)
        if state not in self.q_table or random.random() < 0.2:  # Exploration
            return self.a_star_action(state)
        else:  # Exploitation
            return self.meilleure_action(state)

    def meilleure_action(self, state):
        """Retourne la meilleure action possible selon la Q-table."""
        actions = self.q_table.get(state, {})
        if actions:
            return max(actions, key=actions.get)
        return self.a_star_action(state)

    def a_star_action(self, state):
        """Choisit l'action à partir de la première étape du chemin trouvé par A*."""
        path = self.a_star_path(state)
        if len(path) > 1:
            return path[1]  # La première étape après l'état actuel
        return None  # Aucun chemin trouvé

    def a_star_path(self, start):
        """Retourne le chemin trouvé par A* depuis le point de départ."""
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, self.goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == self.goal:
                return self.reconstruct_path(came_from, current)
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return []  # Aucun chemin trouvé

    def reconstruct_path(self, came_from, current):
        """Reconstruit le chemin à partir du dictionnaire came_from."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def heuristic(self, a, b):
        """Heuristique utilisée par A* (distance de Manhattan)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def step(self, state, action):
        """Effectue une étape et retourne le nouvel état, la récompense et si l'épisode est terminé."""
        if action is None:
            return state, -5, True  # Pénalité plus sévère, fin de l'épisode

        self.visited.add(action)
        if action == self.goal:
            return action, 10, True
        elif action not in self.visited:
            return action, -1, False
        else:
            return action, -1, False


    def update_q_table(self, state, action, next_state, reward):
        """Met à jour la Q-table en utilisant l'équation de Bellman."""
        
        if action is None:
            return  # Si action est None, ignorer la mise à jour

        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions_valides(state)}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in self.actions_valides(next_state)}
        
        best_next_action = max(self.q_table[next_state].values(), default=0)
        self.q_table[state][action] += self.alpha * (
            reward + self.gamma * best_next_action - self.q_table[state][action]
        )


    def train(self, episodes):
        """Entraîne l'agent avec Q-learning sur un certain nombre d'épisodes."""
        tn, fp = 0, 0  # Initialisation des comptages TN et FP

        for episode in range(episodes):
            self.position = (0, 0)
            state = self.position
            total_reward = 0
            steps = 0
            done = False

            while not done:
                action = self.actionChoisie(*state)
                next_state, reward, done = self.step(state, action)
                self.update_q_table(state, action, next_state, reward)
                total_reward += reward
                state = next_state
                steps += 1

                # Calcul des vrais négatifs (TN) et faux positifs (FP) pour l'épisode
                if self.grid[state] == 0:  # Case vide
                    if action == state:
                        tn += 1
                    else:
                        fp += 1

                # Visualisation de l'état actuel de l'épisode
                print(f"Episode {episode + 1}, Step {steps}: Position: {state}, Reward: {reward}")
            
            # Résumé de l'épisode
            print(f"Episode {episode + 1} terminé en {steps} étapes avec un total de récompense: {total_reward}")