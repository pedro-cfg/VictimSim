##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
from genetic import Genetic
import time

## Classe que define o Agente Rescuer com um plano fixo
class Rescuer(AbstractAgent):

    cluster_ready = False
    saved_victims = []
    all_rescuers_known_victims = []

    def __init__(self, env, config_file):
        """ 
        @param env: a reference to an instance of the environment class
        @param config_file: the absolute path to the agent's config file"""

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        self.plan = []              # a list of planned actions
        self.rtime = self.TLIM      # for controlling the remaining time

        self.horizontal = 0 # Incrementa se andar para a direita e decrementa se andar para a esquerda
        self.vertical = 0  # Incrementa se andar para baixo e decrementa se andar para cima

        # Starts in IDLE state.
        # It changes to ACTIVE when the map arrives
        self.body.set_state(PhysAgent.IDLE)
        self.known_map = []
        self.known_victims = []

    def add_saved_victim(self, victim):
        if victim not in Rescuer.saved_victims:
            Rescuer.saved_victims.append(victim)

    def go_save_victims(self):
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)
    
    def receive_map(self, map):
        self.known_map = map

    def wake_up(self):
        self.go_save_victims()

    def set_group(self, group):
        self.known_victims = group[1]

    def get_state(self):
        return self.body.state

    def _planner(self):
        """ A private method that calculates the walk actions to rescue the
        victims. Further actions may be necessary and should be added in the
        deliberata method"""

        # This is a off-line trajectory plan, each element of the list is
        # a pair dx, dy that do the agent walk in the x-axis and/or y-axis

        genetic = Genetic(self.known_map, self)
        victim_coords = [victim[0] for victim in self.known_victims]
        self.plan = genetic.find_route(victim_coords)

    def get_saved_victim(self, coords):

        for victim in self.all_rescuers_known_victims:
            if victim[0] == coords:
                return victim

    def deliberate(self) -> bool:
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """
        
        if not Rescuer.cluster_ready:
            return True

        # No more actions to do
        if self.plan == []:  # empty list, no more actions to do
           return False

        # Takes the first action of the plan (walk action) and removes it from the plan
        dx, dy = self.plan.pop(0)

        # Walk - just one step per deliberation
        result = self.body.walk(dx, dy)
        if result:
            self.horizontal += dx
            self.vertical += dy

        # Rescue the victim at the current position
        if result == PhysAgent.EXECUTED:
            # check if there is a victim at the current position
            seq = self.body.check_for_victim()
            if seq >= 0:
                res = self.body.first_aid(seq) # True when rescued
                if res:
                    victim = self.get_saved_victim((self.horizontal, self.vertical))
                    self.add_saved_victim(victim)

        return True

