import math
import random
import heapq
import time

from node import Node

class RescueRoute:

    graph_map = {}

    def __init__(self, rescuer, sequence, victim_coords):
        self.victim_sequence = sequence
        self.victims_coords = victim_coords
        self.distance = 0
        self.normalized_fitness = 0
        self.rescuer = rescuer
        self.calculate_distance()

    def set_normalized_fitness(self, nfit):
        self.normalized_fitness = nfit

    def get_distance(self):
        return self.distance

    def get_fitness(self):
        return 1 / (1 + self.distance)
    
    def get_normalized_fitness(self):
        return self.normalized_fitness
    
    def calculate_distance(self):
        value = 0
        for i in range(len(self.victim_sequence) - 1) :
            dx = self.victims_coords[self.victim_sequence[i + 1]][0] - self.victims_coords[self.victim_sequence[i]][0]
            dy = self.victims_coords[self.victim_sequence[i + 1]][1] - self.victims_coords[self.victim_sequence[i]][1]
            value += min(abs(dx), abs(dy)) * 1.5  # Anda o máximo que pode na diagonal
            value += abs((abs(dx) - abs(dy))) * 1  # Anda o restante na vertical/horizontal

        self.distance = value

    def mutate(self):

        #O rand acrescenta 0,3 sec no tempo final
        index1 = random.randint(0, len(self.victim_sequence) - 1)
        index2 = random.randint(0, len(self.victim_sequence) - 1)

        new_sequence = self.victim_sequence.copy()

        aux = new_sequence[index1]
        new_sequence[index1] = new_sequence[index2]
        new_sequence[index2] = aux

        return RescueRoute(self.rescuer, new_sequence.copy(), self.victims_coords)

    def get_movements(self):
        coords = []
        base_to_first_victim = self.astar(RescueRoute.graph_map, (0, 0), self.victims_coords[self.victim_sequence[0]])
        coords += base_to_first_victim
        for i in range(len(self.victim_sequence) - 1):
            victim_to_victim = self.astar(RescueRoute.graph_map, self.victims_coords[self.victim_sequence[i]], self.victims_coords[self.victim_sequence[i + 1]])
            coords += victim_to_victim
        last_victim_to_base = self.astar(RescueRoute.graph_map, self.victims_coords[self.victim_sequence[len(self.victim_sequence) - 1]], (0, 0))
        coords += last_victim_to_base

        movements = self.translate_coords_to_movements(coords)
        return movements

    def translate_coords_to_movements(self, coords):
        movements = []

        for i in range(len(coords) - 1):
            x1 = coords[i][0]
            y1 = coords[i][1]
            x2 = coords[i + 1][0]
            y2 = coords[i + 1][1]

            mov = (x2 - x1, y2 - y1)
            movements.append(mov)

        return movements


    def distance_between_victims(self, v1, v2):

        result = self.astar(RescueRoute.graph_map, self.victims[v1][0], self.victims[v2][0])
        return self.calculate_cost(result)
        

    def astar(self, graph, start, goal):
        
        open_list = []  # Lista de nós a serem avaliados
        closed_set = set()  # Conjunto de nós já avaliados
        heur = self.get_heuristic_estimate(start[0], start[1])

        start_node = Node(start, None, 0, heur)
        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)

            if current_node.state == goal:
                # Se chegamos ao objetivo, reconstrua o caminho e retorne-o
                return self.build_path(current_node)

            closed_set.add(current_node.state)

            for neighbor, cost in graph[current_node.state]:
                if neighbor not in closed_set:
                    # Cria um novo nó para o vizinho
                    neighbor_node = Node(neighbor, current_node, current_node.cost + cost,
                                         self.get_heuristic_estimate(neighbor[0], neighbor[1]))

                    # Se o vizinho já está na lista aberta com um custo menor, ignore-o
                    if not any(neighbor_node.state == node.state and neighbor_node.cost >= node.cost for node in
                               open_list):
                        heapq.heappush(open_list, neighbor_node)
        # Se não encontramos um caminho, retornamos None
        return None
    
    def get_heuristic_estimate(self, dx, dy):
        # Estima o gasto necessário para voltar para a base a partir da coord atual
        valor = min(abs(dx), abs(dy)) * 1.5  # Anda o máximo que pode na diagonal
        valor += abs((abs(dx) - abs(dy))) * 1 # Anda o restante na vertical/horizontal
        return valor

    def get_estimate_dist(self, start, goal):
        # Estima o gasto necessário para voltar para a base a partir da coord atual
        dx = start[0] - goal[0]
        dy = start[1] - goal[1]
        valor = min(abs(dx), abs(dy)) * 1.5  # Anda o máximo que pode na diagonal
        valor += abs((abs(dx) - abs(dy))) * 1  # Anda o restante na vertical/horizontal
        return valor

    def build_path(self, node):
            # Reconstrói o caminho de volta do objetivo para o início
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            return list(reversed(path))
    
    def calculate_cost(self, best_route):
        cost = 0
        for i in range(len(best_route) - 1):
            x1 = best_route[i][0]
            y1 = best_route[i][1]
            x2 = best_route[i + 1][0]
            y2 = best_route[i + 1][1]

            mov = (x2 - x1, y2 - y1)

            if(mov == (0,1) or mov == (0,-1) or mov == (1,0) or mov == (-1,0)):
                cost += self.rescuer.COST_LINE
            else:
                cost += self.rescuer.COST_DIAG

        return cost
