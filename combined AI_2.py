import time
import numpy as np
import importlib

class main(object):

    def tag_edit(self,tag,line): 
        lenght_of_tag = len(tag)
        text_on_line = str(line[lenght_of_tag:])
        return text_on_line

    def setup(self,address,number_of_matches,number_of_testing_matches,number_of_outputs,number_of_inputs,environment,run_best,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on):
        import brute_force as BF
        self.BF = BF.main()
        import evo
        self.evo = evo.main()

        self.address = address
        self.environment = environment
        self.run_best = run_best
        self.AI_number = 0
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.precison_of_output = precison_of_output
        self.structure_array = structure_array
        self.Htan_on = Htan_on
        self.bias_on = bias_on
        self.number_of_matches = number_of_matches
        self.number_of_testing_matches = number_of_testing_matches
        self.each_output_min = each_output_min
        self.each_output_max = each_output_max

        file = open(address,"r")
        file.readline()
        self.dataset_start = int(self.tag_edit("learn dataset = ",file.readline())) 
        self.evo_start = int(self.tag_edit("evo = ",file.readline())) 
        self.evo_min_pop = int(self.tag_edit("min population = ",file.readline())) 
        self.evo_max_pop = int(self.tag_edit("max population = ",file.readline())) 
        file.close()


        #setup for brute force 
        address = self.address[:-len("combined AI_2\config.txt")] + "brute force\config.txt"
        self.BF.setup(address,number_of_matches,number_of_testing_matches,number_of_outputs,number_of_inputs,environment,self.run_best,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on)
                           
        return 

    def loop(self,iterations,current_iteration):
        step = 1
        for loop in range(current_iteration,current_iteration + iterations):

            if loop == 0:#brute force
                print("brute force start")
                print("================================================")
                self.AI_number = 0

            elif loop == self.dataset_start:#dataset
                ready = self.set_eviroments_dataset(self.dataset)
                if ready == False:
                    self.dataset_start += 5
                    self.evo_start += 5
                else:
                    print("evo with dataset start")
                    print("================================================")
                    self.AI_number = 1 

            elif loop == self.evo_start:#evo
                if not(self.max_fitness == self.lenght_of_dataset) :
                    self.evo_start += 5
                else:
                    print("evo normal start")
                    print("================================================")
                    address = self.address[:-len("combined AI_2\config.txt")] + "evo\config.txt"
                    self.evo.setup(address,self.number_of_matches,self.number_of_testing_matches,self.number_of_outputs,self.number_of_inputs,self.environment,self.run_best,self.each_output_min,self.each_output_max,self.precison_of_output,self.structure_array,self.Htan_on,self.bias_on, min_population = self.evo_min_pop , max_population = self.evo_max_pop)
                    self.evo.set_memory(self.network_weights)
                    self.AI_number = 2



            if self.AI_number == 0:         #brute force
                fitness = self.BF.loop(step,loop)
                self.dataset = self.BF.get_memory()
                self.memory = self.dataset

            elif self.AI_number == 1:       #nural network
                fitness = self.evo.loop(step,loop)
                self.network_weights = self.evo.get_memory()
                self.memory = self.network_weights

            else:                           #evo
                fitness = self.evo.loop(step,loop)
                self.network_weights = self.evo.get_memory()
                self.memory = self.network_weights

        self.max_fitness = np.amax(fitness)
        return fitness
                       
    def get_memory(self):

        return "need to code"

    def set_memory(self,new_memory):

        #if "<" in new_memory:

        #else:

        return

    def load_dataset_environment(self):
        address_environment = self.address[:-len("AIs\combined AI_2\config.txt")] + "environments\complex dataset\config.txt"
        file = open(address_environment,"r")

        Environment = self.tag_edit("name = ",str(file.readline()[:-1]))
        Environment = importlib.import_module(Environment)
        number_of_matches = int(self.tag_edit("number of matches = ",str(file.readline())))
        number_of_inputs = self.number_of_inputs
        number_of_outputs = self.number_of_outputs
        file.readline()
        file.readline()
        file.readline()
        each_output_min = int(self.tag_edit("min of each output = ",str(file.readline())))
        each_output_max = int(self.tag_edit("max of each output = ",str(file.readline())))
        precison_of_output = self.precison_of_output
        structure_array = self.structure_array
        Htan_on = self.Htan_on
        bias_on = self.bias_on

        file.close()
        return Environment , number_of_matches,number_of_inputs,number_of_outputs,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on

    def set_eviroments_dataset(self,new_memory):

        database , look_up = self.BF.set_memory(new_memory,set_self = False)

       

        inputs_temp = np.zeros((len(look_up),self.number_of_inputs))
        targets_temp = np.zeros((len(look_up),self.number_of_outputs))
        if_every_move_played = np.zeros((len(look_up)), dtype = "bool")
        number_to_use = 0
        for loop in range(len(look_up)):
            temp = look_up[loop]
            temp = temp[1:-1]
            temp = temp.split()
            temp = [float(loop2) for loop2 in (temp)]
            inputs_temp[loop] = temp

            targets_temp[loop], _ ,if_every_move_played[loop] = self.BF.move_cal([look_up[loop]],True)
            #if_every_move_played[loop] = True#remove
            if if_every_move_played[loop] == True:
                number_to_use += 1

        if number_to_use <= int(len(look_up) / 2):
            return False
        inputs = np.zeros((number_to_use,self.number_of_inputs))
        targets = np.zeros((number_to_use,self.number_of_outputs))
        loop2 = 0
        for loop in range(len(look_up)):
            if if_every_move_played[loop] == True:
                inputs[loop2]  = inputs_temp[loop]
                targets[loop2] = targets_temp[loop]
                loop2 += 1

        inputs = inputs.tolist()
        targets = targets.tolist()
        self.dataset_environment , number_of_matches,number_of_inputs,number_of_outputs,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on = self.load_dataset_environment()
       
        self.dataset_environment = self.dataset_environment.game_class()
        self.dataset_environment.set_dataset(inputs,targets)

        number_of_testing_matches = len(inputs)
        self.lenght_of_dataset = number_of_testing_matches
        address = self.address[:-len("combined AI_2\config.txt")] + "evo\config.txt"
        self.evo.setup(address,number_of_matches,number_of_testing_matches,number_of_outputs,number_of_inputs,self.dataset_environment,self.run_best,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on, min_population = self.evo_min_pop , max_population = self.evo_max_pop)
        
        print("=====================================================")
        print(inputs)
        print(targets)
        print("lenght of dataset: " + str(self.lenght_of_dataset))
        return True
