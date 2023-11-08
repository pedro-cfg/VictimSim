##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

from rescuer import Rescuer
from physical_agent import PhysAgent
from kmeans import KMeans
import csv

## Classe que define o Agente Rescuer com um plano fixo
class RescuerMaster(Rescuer):

    cluster_ready = False

    def __init__(self, env, config_file):
        """ 
        @param env: a reference to an instance of the environment class
        @param config_file: the absolute path to the agent's config file"""

        super().__init__(env, config_file)
        self.rescuers = []
        self.explorers = []

    def merge_maps(self, path, victims):

        for i, coord in enumerate(path):
            if coord not in self.known_map:
                self.known_map.append(coord)

        for i, victim in enumerate(victims):
            if victim not in self.known_victims:
                self.known_victims.append(victim)

    def set_explores_and_rescuers_list(self, explorers, rescuers):
        self.explorers = explorers
        self.rescuers = rescuers
    
    def clusterize(self):
        print("Clustering...")
        cluster = KMeans()
        groups = cluster.execute(self.known_victims, 4)
        Rescuer.all_rescuers_known_victims = self.known_victims.copy()

        for i, rescuer in enumerate(self.rescuers):
            rescuer.set_group(groups[i])
            self.write_group_csv(groups[i], i + 1)

        self.set_group(groups[len(groups) - 1])
        self.write_group_csv(groups[len(groups) - 1], len(groups))

        Rescuer.cluster_ready = True

    def write_group_csv(self, group, group_number):
        # Specify the filename for your CSV file
        filename = f'cluster{group_number}.csv'

        # Open the CSV file in write mode and create a CSV writer
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')

            # Write the data to the CSV file
            for row in group[1]:
                csv_writer.writerow([row[1][0], row[0][0], row[0][1], row[1][7]])

        print(f'Data has been written to {filename}')

    def explorers_finished(self):
        
        for explorer in self.explorers:
            if explorer.get_state() == PhysAgent.ACTIVE:
                return False
        
        return True

    def rescuers_finished(self):
        for rescuer in self.rescuers:
            if rescuer.get_state() == PhysAgent.ACTIVE:
                return False

        return True

    def notify_rescuers_to_plan(self):
        
        super()._planner()
        
        for rescuer in self.rescuers:
            rescuer.wake_up()
            rescuer.receive_map(self.known_map)
            rescuer._planner()

    def write_saved_victims_csv(self):
        # Specify the filename for your CSV file
        filename = 'salvas.csv'

        # Open the CSV file in write mode and create a CSV writer
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')

            # Write the data to the CSV file
            saved_victims = Rescuer.saved_victims
            for row in saved_victims:
                csv_writer.writerow([row[1][0], row[0][0], row[0][1], row[1][7]])

        print(f'Data has been written to {filename}')

    def deliberate(self) -> bool:
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """
        
        if Rescuer.cluster_ready == False:

            if self.explorers_finished():
                self.clusterize()
                self.notify_rescuers_to_plan()
            else:
                return True
            
        # No more actions to do
        if self.plan == []:  # empty list, no more actions to do
            if self.rescuers_finished():
                self.write_saved_victims_csv()
                return False
            else:
                return True

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

