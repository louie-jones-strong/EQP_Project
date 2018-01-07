import gym
import numpy as np

class game_class(object):

    environment = 'CartPole-v1'
    boards = [gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment),gym.make(environment)]
    turns = [0]
    finished = [0]
    fitness = [0]

    def start_games(self,game_IDs,start_firsts):


        boards = np.zeros((np.amax(game_IDs)+1,4))
        self.finished  = np.zeros((np.amax(game_IDs)+1))
        self.fitness  = np.zeros((np.amax(game_IDs)+1))


        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]

            boards[loop] = self.boards[ID].reset()

        self.turns = np.zeros((len(game_IDs)))

        return boards , self.turns

    def move(self,game_IDs,moves,run_best):
        moves = np.abs(moves)
        turns   = np.zeros((len(game_IDs)))
        boards  = np.zeros((len(game_IDs),4))
        vailded = np.zeros((len(game_IDs)), dtype=bool)

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            vailded[loop] = True
            turns[loop] = self.turns[ID]


            action = round( moves[loop][0])
            if action > 0.5:
                action = 1
            else:
                action = 0


            boards[loop], temp, self.finished[ID], _ = self.boards[ID].step(action)
            self.fitness[ID] += temp

            if (run_best == True) and (ID == 0):
                self.boards[ID].render()

        return boards , turns , vailded
    
    def end_check(self,game_IDs):

        finished = np.zeros((len(game_IDs)))

        for loop in range(len(game_IDs)):
            ID = game_IDs[loop]
            finished[loop] = self.finished[ID]

        return finished

    def get_fitness(self,game_IDs,run_best):
        if run_best == True:
            for loop in range(len(game_IDs)):
                self.boards[game_IDs[loop]].render(close=True)

        return self.fitness