import numpy as np

class game_class(object):

    #dataset 
    dataset_inputs  = [[1],[2],[3],[4],[5], [6], [7], [8], [9], [10]]
    dataset_outputs = [[2],[4],[6],[8],[10],[12],[14],[16],[18],[20]]


    index = 0

    finished = [0]
    fitness = [0]

    def start_games(self,game_IDs,start_firsts):

        boards = np.zeros((len(game_IDs),1))
        self.finished  = np.zeros((np.amax(game_IDs)+1))
        self.fitness  = np.zeros((np.amax(game_IDs)+1))
        turns = np.zeros((len(game_IDs)))
        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            boards[loop] = self.dataset_inputs[self.index]

        return boards , turns

    def move(self,game_IDs,moves,run_best):

        turns   = np.zeros((len(game_IDs)))
        boards  = np.zeros((len(game_IDs),1))
        vailded = np.ones((len(game_IDs)), dtype=bool)

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            #print("")
            #print("move: " + str(moves[loop]))
            #print("target: " + str(self.dataset_outputs[int(self.index)]))
            if np.round(moves[loop],2) == self.dataset_outputs[int(self.index)]:
                #print("corect")
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
        return 