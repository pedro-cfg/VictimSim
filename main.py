import random
import sys
import os
import time


## importa classes
from environment import Env
from explorer import Explorer
from rescuer import Rescuer
from rescuer_master import RescuerMaster

def main(data_folder_name):
   
    # Set the path to config files and data files for the environment
    current_folder = os.path.abspath(os.getcwd())
    data_folder = os.path.abspath(os.path.join(current_folder, data_folder_name))
    
    # Instantiate the environment
    env = Env(data_folder)
    
    # config files for the agents
    rescuer_file = os.path.join(data_folder, "rescuer_config.txt")
    explorer_file = os.path.join(data_folder, "explorer_config.txt")
    
    resc_list = []

    # Instantiate agents rescuer and explorer
    resc1 = Rescuer(env, rescuer_file)
    resc_list.append(resc1)
    resc2 = Rescuer(env, rescuer_file)
    resc_list.append(resc2)
    resc3 = Rescuer(env, rescuer_file)
    resc_list.append(resc3)
    resc_master = RescuerMaster(env, rescuer_file)

    exp_list = []

    # Explorer needs to know rescuer to send the map
    exp1 = Explorer(env, explorer_file, resc_master, ['E', 'N', 'S', 'W', 'NE', 'NW', 'SW', 'SE'])
    exp_list.append(exp1)
    exp2 = Explorer(env, explorer_file, resc_master, ['N', 'W', 'E', 'S', 'NW', 'NE', 'SE', 'SW'])
    exp_list.append(exp2)
    exp3 = Explorer(env, explorer_file, resc_master, ['W', 'S', 'N', 'E', 'SW', 'SE', 'NE', 'NW'])
    exp_list.append(exp3)
    exp4 = Explorer(env, explorer_file, resc_master, ['S', 'E', 'W', 'N', 'SE', 'NE', 'NW', 'SW'])
    exp_list.append(exp4)


    resc_master.set_explores_and_rescuers_list(exp_list, resc_list)

    # Run the environment simulator
    env.run()
    
        
if __name__ == '__main__':
    """ To get data from a different folder than the default called data
    pass it by the argument line"""
    
    if len(sys.argv) > 1:
        data_folder_name = sys.argv[1]
    else:
        data_folder_name = os.path.join("datasets", "data_teste_tarefa2")
        
    main(data_folder_name)
