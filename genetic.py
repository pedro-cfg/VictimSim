import math
import random
from rescue_route import RescueRoute
import time
import numpy

POPULATION = 1000
MUTATION = 70

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
    
    def population_score(self):
        sum = 0

        for individual in self.population:
            sum += individual.get_distance()

        return sum / len(self.population)

    def find_route(self, victims_coords):
        print("Generating routes for rescuer!")
        init = time.time()
        self.create_initial_population(victims_coords)

        initial_average = self.population_score()
        final_average = 0

        for i in range(MUTATION):
            
            new_generation = []

            for j in range(POPULATION):
                individual = self.roulette(self.population)
                new_individual = individual.mutate()
                new_generation.append(new_individual)

            self.population = self.population + new_generation
            self.population = self.select_outliers(self.population)

        best_individual = self.get_best_individual()
        end = time.time()

        final_average = self.population_score()

        print(f"    Population 1 distance average = {initial_average}m")
        print(f"    Population {MUTATION} distance average = {final_average}m")
        print(f"Completed! -> {end - init}")
        print("")

        return best_individual.get_movements()

    def get_best_individual(self):

        best_dist = self.population[0].get_distance()
        best_ind = self.population[0]
        for ind in self.population:
            if ind.get_distance() < best_dist:
                best_dist = ind.get_distance()
                best_ind = ind
        return best_ind
    
    def select_outliers(self, population):
        return sorted(population, key=lambda individual: individual.get_fitness(), reverse=True)[:POPULATION]


    def create_initial_population(self, victims_coords):

        victims_sequence = [i for i in range(len(victims_coords))]

        for i in range(POPULATION):
            random.shuffle(victims_sequence)
            individual = RescueRoute(self.rescuer, victims_sequence.copy(), victims_coords)
            self.population.append(individual)

    def normalize_fitness(self, population):
        sum = 0
        for individual in population:
            sum += individual.get_fitness()

        for individual in population:
            individual.set_normalized_fitness(individual.get_fitness() / sum)

    def roulette(self, population):

        self.normalize_fitness(population)

        i = 0
        sum = population[i].get_normalized_fitness()
        r = random.uniform(0, 1)

        while(sum < r):
            i = i + 1
            sum += population[i].get_normalized_fitness()

        return population[i]
