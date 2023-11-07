import math
import random
import heapq

from node import Node

class RescueRoute:

    graph_map = {}

    def __init__(self):
        self.victim_sequence = []
        self.distance = -1
        self.victims = []
        self.fitness = 0

    def calculate_fitness(self):
        return 1 /(1 + self.distance) 
    
    def get_fitness(self):
        return self.fitness
    
    def set_fitness(self, fit):
        self.fitness = fit
    
    def init_route(self, victims):
        self.victims = victims
        order = list(range(len(victims)))
        random.shuffle(order)
        self.victim_sequence = order

        self.distance = self.total_distance()

    def total_distance(self):
        
        distance = 0

        result = self.astar(RescueRoute.graph_map, (0,0), self.victims[self.victim_sequence[0]][0])
        distance += self.calculate_cost(result)

        for i in range(len(self.victim_sequence) - 1):
            distance += self.distance_between_victims(self.victim_sequence[i], self.victim_sequence[i + 1], RescueRoute.graph_map)

        result = self.astar(RescueRoute.graph_map, self.victims[self.victim_sequence[len(self.victim_sequence) - 1]][0], (0,0))
        distance += self.calculate_cost(result)

        return distance
    
    def mutate(self):
        index1 = random.randint(0, len(self.victim_sequence) - 1)
        index2 = random.randint(0, len(self.victim_sequence) - 1)

        aux = self.victim_sequence[index1]
        self.victim_sequence[index1] = self.victim_sequence[index2]
        self.victim_sequence[index2] = aux

        self.distance = self.total_distance()

    def distance_between_victims(self, v1, v2, graph_map):

        result = self.astar(graph_map, self.victims[v1][0], self.victims[v2][0])
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
                cost += 1
            else:
                cost += 1.5

        return cost