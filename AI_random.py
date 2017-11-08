import numpy as np
import random

class main(object):

    def tag_edit(self,tag,line): 
        lenght_of_tag = len(tag)
        text_on_line = str(line[lenght_of_tag:])
        return text_on_line

    def setup(self,address,number_of_matches,number_of_testing_matches,number_of_outputs,number_of_inputs,environment,run_best,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on):

        self.number_of_matches = number_of_matches
        self.number_of_testing_matches = number_of_testing_matches
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.environment = environment#.game_class()
        self.run_best = run_best
        self.each_output_min = each_output_min
        self.each_output_max = each_output_max
        self.precison_of_output = precison_of_output

        return

    def loop(self,iterations,current_iteration):
        fitness = 0
        number_of_matches = 5
        for loop in range(1,number_of_matches+1):#to get better avg
            temp = 0
            for loop2 in range(self.number_of_testing_matches):
                
                boards , turns = self.environment.start_games([0],[0])
                while True: # loop for all moves 
                    move = self.move_cal()

                    new_boards , turns , vailded = self.environment.move([0],[move],self.run_best)
                    finished = self.environment.end_check([0])

                    if finished == True:
                        break
                         

                temp = temp / self.number_of_matches
                temp += self.environment.get_fitness([0],self.run_best)
            fitness = ( (fitness*loop) + temp  )/(loop + 1)
        return fitness
                       
    def move_cal(self):
        move = np.zeros((self.number_of_outputs))

        for loop in range(self.number_of_outputs):
            move[loop] = random.randint(self.each_output_min,self.each_output_max)

        return move

    def set_memory(self,new_memory):


        return

    def get_memory(self):

        return"there is none"
