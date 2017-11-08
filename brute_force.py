import numpy as np
import time

#   [times played , avg fitness]

class main(object):

    def setup(self,address,number_of_matches,number_of_testing_matches,number_of_outputs,number_of_inputs,environment,run_best,each_output_min,each_output_max,precison_of_output,structure_array,Htan_on,bias_on):
        self.look_up = np.zeros((0), dtype = "str")
        self.number_of_matches = number_of_matches
        self.number_of_testing_matches = number_of_testing_matches
        self.number_of_outputs = number_of_outputs
        self.number_of_inputs = number_of_inputs
        self.environment = environment#.game_class()
        self.run_best = run_best
        self.node_possible_out = (((each_output_max-each_output_min)+1)*(1/precison_of_output))
        self.all_possible_moves = int((((each_output_max-each_output_min)+1)*(1/precison_of_output))**(self.number_of_outputs))

        self.maxfitness = 0
        self.database = np.zeros((0,self.all_possible_moves,2)) #times played , avg fitness
        return

    def invailed_update(self,board,move_ID,moves_played):
        index = np.argwhere(self.look_up== str(board[0]))
        index = int(index[0][0])


        self.database[index][move_ID][0] = "-101"#times played
        self.database[index][move_ID][1] = "-101"#avg fitness
        moves_played = moves_played[:-len(str(board[0])+","+str(move_ID)+"/")]
        return moves_played

    def update_database(self,moves_played,fitness):
        if not(moves_played == ""):
            moves_played = moves_played[:-1]
            moves_played = moves_played.split("/")
            moves_played = np.asarray(moves_played)

            for loop in range(len(moves_played)):
                new_moves_played = moves_played[loop].split(",")

                board = new_moves_played[0]         
                move = int(new_moves_played[1])     

                #index = self.look_up.index(board)
                index = np.argwhere(self.look_up==board)
                index = int(index[0][0])

                self.database[index][move][0] += 1#times played

                temp = self.database[index][move][1]
                temp = ((temp*self.database[index][move][0])+fitness)/(self.database[index][move][0] + 1)
                self.database[index][move][1] = temp#avg fitness
            

        return

    def new_board(self,board):
        self.look_up = np.append(self.look_up,board)
        temp = np.zeros((self.all_possible_moves,2))

        #self.database = np.append(self.database,temp)
        
        temp = [[0,0]]*self.all_possible_moves



        temp_array = np.ones(((len(self.database)+1),self.all_possible_moves,2))

        loop = -1
        for loop in range(len(self.database)):
            temp_array[loop] = self.database[loop]

        temp_array[loop + 1] = temp
        self.database = temp_array

        return

    def move_cal(self,boards,winning_mode):
        #print("boards1 " + str(boards))
        if_every_move_played = True
        boards = str(boards[0])

        if boards in self.look_up:
            
            temp = self.look_up.tolist()
            index = temp.index(boards)
            

            if winning_mode == True:#winning mode
                #print("boards2 " + str(boards))
                largest = 0
                for loop in range(self.all_possible_moves):


                    if not(self.database[index][loop][0] == -101):
                        #print("test")
                        if self.database[index][largest][1] < self.database[index][loop][1]:#avg fitness
                            #print("test")
                            largest = loop#index of largest

                    elif largest == loop:
                       largest = loop +1

                    if self.database[index][loop][0] == 0:
                        if_every_move_played = False

                move_ids = largest


            else:#learning mode
                smallest = 0
                for loop in range(self.all_possible_moves):


                    if not(self.database[index][loop][0] == -101):
                        if self.database[index][smallest][0] > self.database[index][loop][0]:#times played
                            smallest = loop#index of smallest

                    elif smallest == loop:
                       smallest = loop +1

                    if self.database[index][loop][0] == 0:
                        if_every_move_played = False

                move_ids = smallest
        else: #board has not been played
            self.new_board(boards)
            move_ids = 0



        move = self.moveID_to_move(move_ids)
        return move , move_ids , if_every_move_played

    def moveID_to_move(self,moveID):
        move = np.zeros((self.number_of_outputs))
        for loop in range(self.number_of_outputs,0):
            move[loop] = moveID / (self.node_possible_out)**(loop-1)
            moveID = moveID % (self.node_possible_out)**(loop-1)
        move[0] = moveID
        return move
    
    def loop(self,iterations,current_iteration):
        fitness = np.zeros((1))
        turns = np.zeros((1))
        for iterations in range(iterations):


            for loop in range(self.number_of_matches):
                boards , turns = self.environment.start_games([0],turns)
                moves_played = ""
                while True: # loop for all moves 

                     moves, move_ID ,_= self.move_cal(boards,False)


                     if moves_played == "":
                         moves_played = str(boards[0])+","+str(move_ID)+"/"
                     else:
                         moves_played += str(boards[0])+","+str(move_ID)+"/"

                     new_boards , turns , vailded = self.environment.move([0],[moves],self.run_best)
                     finished = self.environment.end_check([0])

                     if vailded == False:
                         
                         moves_played = self.invailed_update(boards,move_ID,moves_played)

                     boards = new_boards
                     if finished == True:
                         break
                     

                fitness = self.environment.get_fitness([0],self.run_best)
                if self.run_best == False:
                    self.update_database(moves_played,fitness)

                if fitness > self.maxfitness :
                    self.maxfitness = fitness
        
        #==========================================================================================
        #work out final fitness
        #print("=================================winning mode")
        fitness = 0
        for loop in range(self.number_of_testing_matches):
            boards , turns = self.environment.start_games([0],turns)
            while True: # loop for all moves 

                moves, move_ID, _ = self.move_cal(boards,True)

                boards , turns , vailded = self.environment.move([0],[moves],self.run_best)
                finished = self.environment.end_check([0])

                if (finished == True) or (vailded == False):
                    break
            fitness += self.environment.get_fitness([0],self.run_best)
        #print(self.look_up)
        #print(self.database)

        return fitness

    def get_memory(self):

        database = self.database.tolist()
        look_up = self.look_up.tolist()

        new_database = np.zeros((len(database),int(self.node_possible_out)), dtype = "str")
        new_database = new_database.tolist()
        new_new_database = np.zeros((len(database)), dtype = "str")
        new_new_database = new_new_database.tolist()

        for loop in range(len(database)):
            for loop2 in range(int(self.node_possible_out)):
                new_database[loop][loop2] = str(database[loop][loop2][0]) + "$" + str(database[loop][loop2][1])
            new_new_database[loop] = "£".join(new_database[loop])

        database = "*".join(new_new_database)

        look_up = ":".join(look_up)

        return str(database)+"<lookup>"+str(look_up)

    def set_memory(self,new_memory,set_self = True):
        
        database = new_memory[:new_memory.index("<")]
        look_up = new_memory[new_memory.index(">")+1:]
        database = database.split("*")
        for loop in range(len(database)):
            database[loop] = database[loop].split("£")
            for loop2 in range(len(database[0])):
                database[loop][loop2] = database[loop][loop2].split("$")


        look_up = look_up.split(":")
        look_up = np.array(look_up)

        if set_self == True:
            self.database = database
            self.look_up = look_up

        return database , look_up