import numpy as np

class game_class(object):

    boards = [[]] 
    fitness = []
    turns = []
    finished = []

    def start_games(self,game_IDs,start_firsts):
        self.boards = np.zeros((np.amax(game_IDs)+1,9))
        self.fitness = np.zeros((np.amax(game_IDs)+1))
        self.turns = np.zeros((np.amax(game_IDs)+1))
        self.finished = np.zeros((np.amax(game_IDs)+1), dtype=bool)

        boards = np.zeros((len(game_IDs),9))
        turns = np.zeros((len(game_IDs)))

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            turns[loop]    = start_firsts[loop]
            self.turns[ID] = start_firsts[loop]

        return boards , turns
    
    def move(self,game_IDs,moves,run_best):
        turns   = np.zeros((len(game_IDs)))
        vailded = np.zeros((len(game_IDs)), dtype=bool)
        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]

            move = int( round( moves[loop][0] ))

            if move > 8:
                move = 8
            elif move < 0:
                move = 0

            if self.boards[ID][move] == 0:
                vailded[loop] = True
                if self.turns[ID] == 0:
                    turns[loop] = 1
                    self.turns[loop] = 1
                    self.boards[ID][move] = 1
                else:
                    turns[loop] = 0
                    self.turns[loop] = 0
                    self.boards[ID][move] = 2
                if self.turns[ID] == 0:
                    self.fitness[ID] += 1 # vaild
            else:
                turns[loop] = self.turns[ID]
                vailded[loop] = False
                self.finished[ID] = True
                if self.turns[ID] == 0:
                    self.fitness[ID] += -1 # invaild
        return self.boards , turns , vailded

    def end_check(self,game_IDs):
        finished = np.zeros((len(game_IDs)), dtype=bool)

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            if self.finished[ID] == True:
                finished[loop] = True
            else:
                if self.win_check(ID,1) == True:#win
                    finished[loop] = True
                    self.fitness[ID] += 5

                elif self.win_check(ID,2) == True:#loss
                    finished[loop] = True
                    self.fitness[ID] += -3

                elif not(0 in self.boards[ID]):#draw
                    finished[loop] = True
                    self.fitness[ID] += 1

                else:#not finished
                    finished[loop] = False
        return finished

    def get_fitness(self,game_IDs,run_best):

        return self.fitness

    def win_check(self,ID,i):
        if    (self.boards[ID][0] == i and self.boards[ID][1] == i and self.boards[ID][2] == i) \
           or (self.boards[ID][3] == i and self.boards[ID][4] == i and self.boards[ID][5] == i) \
           or (self.boards[ID][6] == i and self.boards[ID][7] == i and self.boards[ID][8] == i) \
           or (self.boards[ID][0] == i and self.boards[ID][3] == i and self.boards[ID][6] == i) \
           or (self.boards[ID][1] == i and self.boards[ID][4] == i and self.boards[ID][7] == i) \
           or (self.boards[ID][2] == i and self.boards[ID][5] == i and self.boards[ID][8] == i) \
           or (self.boards[ID][0] == i and self.boards[ID][4] == i and self.boards[ID][8] == i) \
           or (self.boards[ID][6] == i and self.boards[ID][4] == i and self.boards[ID][2] == i):
            output = True
        else:
            output = False
 
        return output


