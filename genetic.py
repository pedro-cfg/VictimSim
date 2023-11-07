import math
import random
from rescue_route import RescueRoute

class Genetic:

    graph_map = {}

    def __init__(self, map):
        self.map = map
        self.population = []
        Genetic.create_graph(self.map)
        RescueRoute.graph_map = Genetic.graph_map
        

    @staticmethod
    def create_graph(map):

        if len(Genetic.graph_map) != 0:
            return
        
        for i, position in enumerate(map):

            Genetic.graph_map[(position[0], position[1])] = []

            for j, coord in enumerate(map):
                
                if i == j:
                    continue

                cost = Genetic.is_neighbour((position[0], position[1]), (coord[0], coord[1]))
                if cost != None:
                    Genetic.graph_map[(position[0], position[1])].append([(coord[0], coord[1]), cost])
    
    @staticmethod
    def is_neighbour(coord1, coord2):
        if (coord1[0] - 1, coord1[1]) == coord2:
            return 1
        if (coord1[0], coord1[1] - 1) == coord2:
            return 1
        if (coord1[0] - 1, coord1[1] - 1) == coord2:
            return 1.5
        if (coord1[0] + 1, coord1[1]) == coord2:
            return 1
        if (coord1[0], coord1[1] + 1) == coord2:
            return 1
        if (coord1[0] + 1, coord1[1] + 1) == coord2:
            return 1.5
        if (coord1[0] + 1, coord1[1] - 1) == coord2:
            return 1.5
        if (coord1[0] - 1, coord1[1] + 1) == coord2:
            return 1.5
        return None
    
    def verify_possible_routes(self):
        pass

    def find_route(self, victims):
        self.init_route_population(10, victims)

    def init_route_population(self, number, victims):

        for i in range(number):
            individual = RescueRoute()
            individual.init_route(victims)
            self.population.append(individual)
        
        sum = 0

        for individual in self.population:
            sum += individual.calculate_fitness()

        for individual in self.population:
            individual.set_fitness(individual.calculate_fitness()/sum)

        for individual in self.population:
            selected = self.roulette(self.population)
            selected.mutate()


        breakzin = 1

    def roulette(self, population):
        
        population = sorted(population, key=lambda individual: individual.get_fitness())

        i = 1
        sum = population[i].get_fitness()
        r = random.uniform(0, 1)

        while(sum < r):
            i = i + 1
            sum += population[i].get_fitness()

        return population[i]