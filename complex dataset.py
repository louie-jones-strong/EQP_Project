import numpy as np
import os

class game_class(object):

    #flower dataset
    file = open(os.getcwd() + "\\info\\environments\\complex dataset\\dataset_1.txt")

    lenght_of_dataset = int(int(file.readline())/2)

    temp = file.readline().split(",")
    temp = [float(i) for i in temp]
    number_of_inputs = len(temp)
    dataset_inputs  = np.zeros((lenght_of_dataset,number_of_inputs))
    dataset_inputs[0]  = temp

    temp = file.readline().split(",")
    temp = [float(i) for i in temp]
    number_of_outputs = len(temp)
    dataset_outputs = np.zeros((lenght_of_dataset,number_of_outputs))
    dataset_outputs[0] = temp

    for loop in range(1,lenght_of_dataset):

        temp = file.readline().split(",")
        temp = [float(i) for i in temp]
        dataset_inputs[loop]  = temp

        temp = file.readline().split(",")
        temp = [float(i) for i in temp]
        dataset_outputs[loop] = temp
    file.close()
    index = 0
    finished = [0]
    fitness = [0]

    def start_games(self,game_IDs,start_firsts):

        boards = np.zeros((len(game_IDs),self.number_of_inputs))
        self.finished  = np.zeros((np.amax(game_IDs)+1))
        self.fitness  = np.zeros((np.amax(game_IDs)+1))
        turns = np.zeros((len(game_IDs)))
        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            boards[loop] = self.dataset_inputs[self.index]

        return boards , turns

    def move(self,game_IDs,moves,run_best):
        turns   = np.zeros((len(game_IDs)))
        boards  = np.zeros((len(game_IDs),self.number_of_inputs))
        vailded = np.ones((len(game_IDs)), dtype=bool)

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]

            #print("board: " + str(self.dataset_inputs[int(self.index)]))
            #print("move: " + str(moves[loop]))
            #print("target: " + str(self.dataset_outputs[int(self.index)]))
            #print("")
            if np.round(moves[loop],2) == self.dataset_outputs[int(self.index)]:
                #print("tick")
                temp = 1
            else:
                temp = 0
            
            self.fitness[ID] += temp

            self.finished[ID] = True

            boards[loop] = self.dataset_inputs[int(self.index)]

        if self.index < len(self.dataset_inputs)-1:
            self.index += 1
        else:
            self.index = 0
        return boards , turns , vailded
    
    def end_check(self,game_IDs):

        finished = np.zeros((len(game_IDs)))

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            finished[loop] = self.finished[ID]

        return finished

    def get_fitness(self,game_IDs,run_best):

        return self.fitness

    def get_dataset(self):

        return self.dataset_inputs ,self.dataset_outputs

    def set_dataset(self,new_inputs,new_outputs):
        self.dataset_inputs = new_inputs
        self.dataset_outputs = new_outputs

        self.number_of_inputs = len(self.dataset_inputs[0])
        self.lenght_of_dataset = len(self.dataset_inputs)
        self.number_of_outputs = len(self.dataset_outputs[0])
        return 