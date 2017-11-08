import numpy as np
import random
import ann_runner
import time

class main(object):

    def tag_edit(self,tag,line): 
        lenght_of_tag = len(tag)
        text_on_line = str(line[lenght_of_tag:])
        return text_on_line

    def setup(self,address,number_of_matches,number_of_testing_matches,number_of_outputs,number_of_inputs,environment,run_best,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on,min_population = "test",max_population = "test"):

        self.max_fitness = 0
        self.number_of_matches = number_of_testing_matches
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.environment = environment#.game_class()
        self.run_best = run_best
        self.Htan_on = Htan_on
        self.bias_on = bias_on

        
        file = open(address,"r")

        file.readline()
        if max_population == "test":
            self.max_number_of_population = int(self.tag_edit("max number of population = ",file.readline())) #max number of population
        else:
            self.max_number_of_population = max_population

        if min_population == "test":
            self.min_number_of_population = int(self.tag_edit("min number of population = ",file.readline())) #min number of population
        else:
            self.min_number_of_population = min_population

        file.close()
        if run_best == True:
            self.max_number_of_population = 1
            self.min_number_of_population = 1
        
        temp = structure_array.split(",")
        
        self.structure_array = np.zeros((len(temp)+2) ,dtype = int)
        self.structure_array[0] = self.number_of_inputs

        if not(len(temp) == 1 and int(temp[0]) == 0):

            self.structure_array = np.zeros((len(temp)+2) ,dtype = int)
            self.structure_array[0] = self.number_of_inputs

            for loop in range(len(temp)):
                self.structure_array[loop+1] = temp[loop]

            self.structure_array[loop+2] = self.number_of_outputs
        else:
            self.structure_array = np.zeros((2) ,dtype = int)
            self.structure_array[0] = self.number_of_inputs
            self.structure_array[1] = self.number_of_outputs

        
        
        temp = ann_runner.network_setup(self.structure_array,self.bias_on,["test"])
        self.lenght_of_chromosome = temp[7]

        self.set_memory()

        return

    def loop(self,iterations,current_iteration):

        for loop in range(iterations):
            #===================

            fitness, first_selection_chance = self.fitness_cal(self.number_of_matches)
            if self.run_best == False:
                selection_chance = self.kill(first_selection_chance)

                self.breed(selection_chance)
            #===================

        return fitness
                    
    def split(self,new_size,old_size,mutation_rate):

        temp_array = np.zeros((new_size,self.lenght_of_chromosome))
        
        for loop in range(old_size):
            temp_array[loop] = self.chromosome[loop]

        for loop in range(old_size,new_size):
            temp = random.randint(0,old_size-1)

            temp_array[loop] = self.mutation(self.chromosome[temp],mutation_rate,self.lenght_of_chromosome,1)

        self.chromosome = temp_array
        return
    
    def mutation(self,DNA,mutation_rate,lenght_of_chromosome,mutation_amount):
        new_DNA = np.zeros((lenght_of_chromosome))


        for loop in range(lenght_of_chromosome):
            temp = random.randint(0,1000)/10
            
            if temp < mutation_rate:
                temp2 = random.randint(-10,10)/100
                temp2 = temp2 * 5
                if temp2 < mutation_amount:
                    temp2 = temp2 * 10
                new_DNA[loop] = DNA[loop] + temp2
            else:

                new_DNA[loop] = DNA[loop]
        return new_DNA
    
    def kill(self,selection_chance):

        new_selection_chance = np.zeros((self.min_number_of_population))
        new_DNA = np.zeros((self.min_number_of_population,self.lenght_of_chromosome))

        temp_array = [loop for loop in range(self.max_number_of_population)]

        
        for loop in range(int(self.min_number_of_population)):
            temp = np.random.choice(temp_array, p = selection_chance)
            new_DNA[loop] = self.chromosome[ temp]
            new_selection_chance[loop] = selection_chance[temp]
        
        new_selection_chance = new_selection_chance / np.sum(new_selection_chance)
        self.chromosome = new_DNA
        return new_selection_chance
    
    def breed(self,selection_chance):
        new_DNA = np.zeros((self.max_number_of_population,self.lenght_of_chromosome))
        for loop in range(self.min_number_of_population):
            new_DNA[loop] = self.chromosome[loop]
        temp_array = [i for i in range(self.min_number_of_population)]

        for loop in range(self.min_number_of_population,self.max_number_of_population):
           temp  = np.random.choice(temp_array, p = selection_chance)
           temp2 = np.random.choice(temp_array, p = selection_chance)


           DNA_1 = self.chromosome[temp]
           DNA_2 = self.chromosome[temp2]


           for loop2 in range(self.lenght_of_chromosome):
               temp = random.randint(0,1)
               if temp == 0:
                   new_DNA[loop][loop2] = DNA_1[loop2]
               else:
                   new_DNA[loop][loop2] = DNA_2[loop2]

           
           new_DNA[loop] = self.mutation(new_DNA[loop],5,self.lenght_of_chromosome,0.1)
        self.chromosome = new_DNA
        return 
    
    def fitness_cal(self,number_of_matches):
        #fitness = np.zeros((self.max_number_of_population))
        fitness = np.ones((self.max_number_of_population))

        #fitness += self.tornaments(number_of_matches)
        
        fitness = self.tornaments(number_of_matches)


        if  max(fitness) >= self.max_fitness:
            self.max_fitness = max(fitness)
            self.control_chromosome = self.chromosome[np.argmax(fitness)]

        if np.amin(fitness) < 0:
            selection_chance = fitness + (np.abs(np.amin(fitness)))+1
        else:
            selection_chance = fitness

        selection_chance = pow(selection_chance,3)


        selection_chance = selection_chance / np.amax(selection_chance)

        selection_chance = selection_chance / np.sum(selection_chance)

        return fitness , selection_chance
    
    def tornaments(self,number_of_matches):
            fitness = np.zeros((len(self.chromosome)))
            full_IDs = [i for i in range(len(self.chromosome))]
            for loop in range(number_of_matches):
                game_IDs = full_IDs

                if (loop % 2 == 0):
                    turns = np.ones((len(game_IDs)))
                else:
                    turns = np.zeros((len(game_IDs)))

                boards , turns = self.environment.start_games(game_IDs,turns)

                

                all_finished = False
                while all_finished == False:



                    temp_DNA = np.zeros((len(game_IDs),self.lenght_of_chromosome))
                    if turns[0] == 0:
                        for loop2 in range(len(game_IDs)):
                            temp_DNA[loop2] = self.chromosome[game_IDs[loop2]]
                        moves = self.move_cal(boards,temp_DNA,len(game_IDs))

                    else:
                        for loop2 in range(len(game_IDs)):
                            temp_DNA[loop2] = self.control_chromosome[0]
                        moves = self.move_cal(boards,temp_DNA,len(game_IDs))




                    boards , turns , vailded = self.environment.move(game_IDs,moves,self.run_best)
                    finished = self.environment.end_check(game_IDs)




                    temp = []
                    for loop2 in range(len(game_IDs)):
                        if (finished[loop2] == False) and (vailded[loop2] == True):
                            if len(temp) == 0:
                                temp = [int(game_IDs[loop2])]
                            else:
                                temp = np.append(temp,int(game_IDs[loop2]))

                        elif vailded[loop2] == False:
                             finished[loop2] = True
                    game_IDs = temp




                    if not(False in finished):
                        temp = self.environment.get_fitness(full_IDs,self.run_best)
                        fitness += temp 
                        all_finished = True
            #print(self.chromosome)
            #print(fitness)
            return fitness #/number_of_matches
    
    def move_cal(self,inputs,DNA,number_of_DNA):
        number_of_outputs = self.structure_array[len(self.structure_array)-1]
        outputs = np.zeros((number_of_DNA,self.number_of_outputs))

        for loop in range(number_of_DNA):
           # print(len(inputs[loop]))
            #print(inputs[loop])
            #print(self.structure_array)
            outputs[loop]= ann_runner.main(self.structure_array,self.bias_on,0.1,DNA[loop],inputs[loop],self.Htan_on)
        return outputs   

    def get_memory(self):
        chromosome = str(self.control_chromosome.tolist())
        #print(self.chromosome)
        return chromosome

    def set_memory(self,new_memory = "test"):
        if new_memory == "test":
            self.chromosome = np.ones((1,self.lenght_of_chromosome))
            self.control_chromosome = self.chromosome[0]
            self.split(self.max_number_of_population,1,50)
        else:
            
            new_memory = (new_memory[1:-1])
            new_memory = new_memory.split(",")
            new_memory = np.array(new_memory,dtype = float)
            new_memory = new_memory.tolist()
            new_memory = [new_memory]
            self.chromosome = new_memory
            self.control_chromosome = self.chromosome
            self.split(self.max_number_of_population,len(new_memory),0)
        return