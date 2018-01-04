import numpy as np
import time
import pygame
import os
import importlib
from common_code import tag_edit

class main(object):
    
    def main_code(self):
        iterations = 0
    
        if self.auto_train == True:#auto train
            start_time_mark = time.time()
            for self.AI_number in range(self.number_of_AIs):
                for self.env_number in range(self.number_of_envs):
                    start_time_mark_2 = time.time()

                    successful = self.AI_env_read_in()
                    if successful == False:
                        continue
    
                    iterations = 0
                    while iterations+1 <= self.max_iterations:
                        time_mark = time.time()
                        fitness = self.AI.loop(self.step,iterations)
                        iterations += self.step
                        time_mark = time.time() - time_mark

                        self.save_fitness(fitness,iterations,time_mark,time.time() - start_time_mark_2,False)
                        self.output(fitness,time_mark,start_time_mark,iterations,self.step)

                        memory = self.AI.get_memory()
                        address = self.address_main + "\\data\\memory\\" + str(self.Title)
                        self.save_memory(memory,address,"\\" + str(self.Title) +  "_" + str(iterations) + ".txt")
                        
                    memory = self.AI.get_memory()
                    address = self.address_main + "\\data\\memory\\" + str(self.Title)
                    self.save_memory(memory,address,"\\" + str(self.Title) + "_final.txt")

        else:# user input
            start_time_mark = time.time()
            while True:
                pygame.mixer.music.play()
                temp = time.time()
                user_input = int(input("number of iterations: "))
                temp = time.time() - temp
                start_time_mark = start_time_mark + temp

                self.max_iterations = iterations + user_input
                while iterations+1 <= self.max_iterations:
                     time_mark = time.time()
                     if iterations + self.step > self.max_iterations:
                         fitness = self.AI.loop(self.max_iterations - iterations,iterations)
                         iterations += self.max_iterations - iterations
                     else:
                        fitness = self.AI.loop(self.step,iterations)
                        iterations += self.step

                     time_mark = time.time() - time_mark
    
                     self.output(fitness,time_mark,start_time_mark,iterations,self.step)
                     self.save_fitness(fitness,iterations,time_mark,time.time() - start_time_mark,True)

                     memory = self.AI.get_memory()
                     address = self.address_main + "\\data\\memory\\" + str(self.Title)
                     self.save_memory(memory,address,"\\" + str(self.Title) + "_user_input.txt")
    
        return
    
    def setup(self):
        os.system("title "+"Back Bone Code")

        # setup veriables 
        self.AI_number = 0
        self.env_number = 0
        self.run_best = 0
        #start config
        self.address_main = os.getcwd() + "\\info"

        file = open(self.address_main + "\\config.txt")
        self.max_iterations = int(tag_edit("iterations = ",str(file.readline()[:-1])))
        self.step = int(tag_edit("step = ",str(file.readline()[:-1])))
        self.clear = bool(int(tag_edit("clear = ",str(file.readline()[:-1]))))
        file.close()

        self.address_sound = self.address_main + "\\sounds\\ring.ogg"
        pygame.mixer.init()
        pygame.mixer.music.load(self.address_sound)

        user_input = int(input("auto[0] pick[1] render[2]:"))
        if user_input == 1:
            self.auto_train = False
            self.pick_AI_and_evo()

        elif user_input == 2:
            self.auto_train = False
            self.render_run()
        else:
            self.auto_train = True
            temp = os.listdir(self.address_main + "\\AIs\\")
            self.number_of_AIs = len(temp)

            temp = os.listdir(self.address_main + "\\Environments\\")
            self.number_of_envs = len(temp)
            self.AI_env_read_in()
            

        self.main_code()
        return
    
    def output(self,fitness,time_mark,start_time_mark,iterations,step):
        fitness = np.sort(fitness)
        
        if self.clear == True:
            os.system("cls")


        print("current iterations: " + str(iterations))
        print("fitness: " + str(fitness))
        print("time of one: " + str(time_mark/step))
        print("full time: " + str(time_mark))
        print("time since start: " + str(time.time() - start_time_mark))
        print("")
        return
    
    def load_memory(self,epoch):
        address = self.address_main + "/data/memory/" + self.Title + "/" + self.Title + "_" + epoch + ".txt"
        file = open(address,"r")
        memory = file.read()
        file.close()

        return memory
    
    def save_memory(self,memory,address_folder,address_file):

        address = address_folder
        if not os.path.exists(address):#makes floder if doesn't exists
            os.makedirs(address)

        address += address_file
        file = open(address,"w")
        file.write(str(memory))
        file.close()
        return

    def save_fitness(self,fitness,iterations,time_taken,start_time_mark,user_input):
        time_taken = round( time_taken,2)
        fitness = np.sort(fitness)
        if user_input == True:#floder to put it in
            address = self.address_main + "\\data\\fitness_user_input\\"+str(self.Title)+".csv"
        else:
            address = self.address_main + "\\data\\fitness\\"+str(self.Title)+".csv"

        if iterations == self.step:
            file = open(address,"w")
            file.writelines("iterations,fitness,time taken,time since start,fitness array" + "\n")
        else:
            file = open(address,"a")
        file.writelines(str(iterations) + "," + str(np.amax(fitness)) + "," + str(time_taken) + "," + str(start_time_mark) + "," + str(fitness.tolist()) + "\n")

        file.close()
        return

    def pick_AI_and_evo(self): # for users to pick withc aI and evo to use
        successful = False
        while successful == False:
            self.auto_train = False
            #AI read in
            temp = os.listdir(self.address_main + "\\AIs\\")
            self.number_of_AIs = len(temp)
            for loop in range(len(temp)):
                print("["+str(loop)+"] = " + str(temp[loop]))
            self.AI_number = int(input("the number of the AI to use: "))
            print("")

            #Environment read in
            temp = os.listdir(self.address_main + "\\Environments\\")
            number_of_envs = len(temp)
            for loop in range(len(temp)):
                print("["+str(loop)+"] = " + str(temp[loop]))
            self.env_number = int(input("the number of the Environment to learn: "))

            successful = self.AI_env_read_in()

        return

    def AI_env_read_in(self):#once picked
        
        
        #AI config
        self.address_AI = self.address_main + "\\AIs\\"
        temp = os.listdir(self.address_AI)
        self.address_AI = self.address_AI + temp[self.AI_number] + "\\config.txt"
        file = open(self.address_AI,"r")
        self.AI = tag_edit("name = ",str(file.readline()))
        AI_name = self.AI[:-1]
        self.AI = importlib.import_module(AI_name)
        self.AI = self.AI.main()
        file.close()
    
    
        #Environment config
        self.address_environment = self.address_main + "\\Environments\\"
        temp = os.listdir(self.address_environment)
        self.address_environment = self.address_environment + temp[self.env_number] + "\\config.txt"

        file = open(self.address_environment,"r")
        Environment_name = tag_edit("name = ",str(file.readline()[:-1]))
        self.Environment = importlib.import_module(Environment_name)
        self.Environment = self.Environment.game_class()
        self.number_of_matches = int(tag_edit("number of matches = ",str(file.readline())))
        self.number_of_testing_matches = int(tag_edit("number of testing matches = ",str(file.readline())))
        self.number_of_inputs = int(tag_edit("number of inputs = ",str(file.readline())))
        self.number_of_outputs = int(tag_edit("number of outputs = ",str(file.readline())))
        self.each_output_min = int(tag_edit("min of each output = ",str(file.readline())))
        self.each_output_max = int(tag_edit("max of each output = ",str(file.readline())))
        self.precison_of_output = float(tag_edit("precision of each output = ",str(file.readline())))
        self.structure_array = tag_edit("structure array = ",str(file.readline()))
        Htan_on = int(tag_edit("Htan_on = ",str(file.readline())))
        bias_on = int(tag_edit("bias_on = ",str(file.readline())))

        file.close()

        os.system("cls")

        if  str(self.AI) == "neural network" and not(self.Environment == "simple dataset" or self.Environment == "complex dataset"): # check it is dataset
            print("can't run this!!!!!")
            print("")
            return False
        else:
            self.Title = str(AI_name) + "+" + str(Environment_name)
            os.system("title "+ self.Title)
            
            #setup
            self.AI.setup(self.address_AI,self.number_of_matches,self.number_of_testing_matches,self.number_of_outputs,self.number_of_inputs,self.Environment,self.run_best,self.each_output_min,self.each_output_max,self.precison_of_output,self.structure_array,Htan_on,bias_on)
            
            memory = self.AI.get_memory()
            address = self.address_main + "\\data\\memory\\" + str(self.Title)
            self.save_memory(memory,address,"\\" + str(self.Title) +  "_untrained.txt")

            return True

    def render_run(self):# add error checking (low need)
        self.run_best = True
        while True:
            pygame.mixer.music.play()
            user_input = int(input("run worst[0] best[1] user_input[2]: "))

            self.pick_AI_and_evo()

            if user_input == 0:     #run worst
                new_memory = self.load_memory("untrained")
                
            elif user_input == 1:   #run best
                new_memory = self.load_memory("final")

            else:                   #user_input
                new_memory = self.load_memory("user_input")

            self.AI.set_memory(new_memory)
            start_time_mark = time.time()
            for loop in range(5):
                time_mark = time.time()
                fitness = self.AI.loop(1,0)
                time_mark = time.time() - time_mark
                self.output(fitness,time_mark,start_time_mark,loop,1)

        return fitness


main = main()
main.setup()