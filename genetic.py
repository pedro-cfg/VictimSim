import math
import random
from rescue_route import RescueRoute
import time
import numpy

class Genetic:

    graph_map = {}

    def __init__(self, map, rescuer):
        self.map = map
        self.population = []
        Genetic.create_graph(self.map, rescuer)
        RescueRoute.graph_map = Genetic.graph_map
        self.rescuer = rescuer

    @staticmethod
    def create_graph(map, rescuer):

        if len(Genetic.graph_map) != 0:
            return
        
        for i, position in enumerate(map):

            Genetic.graph_map[(position[0], position[1])] = []

            for j, coord in enumerate(map):
                
                if i == j:
                    continue

                cost = Genetic.is_neighbour((position[0], position[1]), (coord[0], coord[1]), rescuer)
                if cost is not None:
                    Genetic.graph_map[(position[0], position[1])].append([(coord[0], coord[1]), cost])
        breaking = 1


    @staticmethod
    def is_neighbour(coord1, coord2, rescuer):
        if (coord1[0] - 1, coord1[1]) == coord2:
            return rescuer.COST_LINE
        if (coord1[0], coord1[1] - 1) == coord2:
            return rescuer.COST_LINE
        if (coord1[0] - 1, coord1[1] - 1) == coord2:
            return rescuer.COST_DIAG
        if (coord1[0] + 1, coord1[1]) == coord2:
            return rescuer.COST_LINE
        if (coord1[0], coord1[1] + 1) == coord2:
            return rescuer.COST_LINE
        if (coord1[0] + 1, coord1[1] + 1) == coord2:
            return rescuer.COST_DIAG
        if (coord1[0] + 1, coord1[1] - 1) == coord2:
            return rescuer.COST_DIAG
        if (coord1[0] - 1, coord1[1] + 1) == coord2:
            return rescuer.COST_DIAG
        return None
    
    def verify_possible_routes(self):
        pass

    def find_route(self, victims):
        ini = time.time()
        self.init_route_population(5, victims)
        fim = time.time()
        print(f"Init: {fim - ini}")
        mutation_number = 10
        victim_number = len(victims)
        done = False

        for i in range(mutation_number):
            ini = time.time()
            sum = 0
            new_generation = []
            for individual in self.population:
                sum += individual.calculate_fitness()
            fim = time.time()
            #print(f"For 1: {fim - ini}")

            ini = time.time()
            for individual in self.population:
                individual.set_fitness(individual.calculate_fitness() / sum)
            fim = time.time()
            #print(f"For 2: {fim - ini}")

            ini = time.time()
            #self.population = sorted(self.population, key=lambda individual: individual.get_fitness())
            for individual in self.population:
                selected = self.roulette(self.population)
                selected.mutate()
                new_generation.append(selected)
            fim = time.time()
            print(f"For 3: {fim - ini}")
            #print("\n")
            self.population = new_generation

        best_individual = self.get_best_individual()
        return best_individual.get_movements()

    def get_best_individual(self):
        best_dist = self.population[0].get_total_distance()
        best_ind = self.population[0]
        for ind in self.population:
            if ind.get_total_distance() < best_dist:
                best_dist = ind.get_total_distance()
                best_ind = ind
        return best_ind

    def init_route_population(self, number, victims):

        for i in range(number):
            individual = RescueRoute(self.rescuer)
            individual.init_route(victims)
            self.population.append(individual)

    def roulette(self, population):
        i = 0
        sum = population[i].get_fitness()
        r = random.uniform(0, 1)

        while(sum < r):
            i = i + 1
            sum += population[i].get_fitness()

        return population[i]
