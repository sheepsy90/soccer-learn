
from NeuralNetwork import NeuralNetwork

class KNN(object):
    
    
    def __init__(self):
        self.knn = NeuralNetwork(19, 30, 5)
        self.lastoutput = None
        self.lastinput = None
        self.rewardchain = []
        pass 
                
    def process(self, state):
        ballx = [-1, 1, -1]
        if state[0] == 1:
            ballx = [1, -1, -1]
        elif state[0] == -1:
            ballx = [-1, -1, 1]
            
        bally = [-1, 1, -1]
        if state[1] == 1:
            bally = [1, -1, -1]
        elif state[1] == -1:
            bally = [-1, -1, 1]
            
            
        goalx = [-1, 1, -1]
        if state[3] == 1:
            goalx = [1, -1, -1]
        elif state[3] == -1:
            goalx = [-1, -1, 1]
            
        goaly = [-1, 1, -1]
        if state[4] == 1:
            goaly = [1, -1, -1]
        elif state[4] == -1:
            goaly = [-1, -1, 1]
            
        state = ballx + bally + [int(i) for i in state[2].split("#")] + goalx + goaly + state[5:]
        #print state
        self.lastinput = state
        self.lastoutput = self.knn.calculate(state)
        index = list(self.lastoutput).index(max(list(self.lastoutput)))
        return index
        
        

    def learn_with_reward(self, reward, gamma=0.2):
        # The reward for this action
        # KNN S -> A which results in reward R
        self.rewardchain.append(reward)
        if len(self.rewardchain) > 25:
            self.rewardchain = self.rewardchain[1:]
        
        summed_reward_value = 0
        l = len(self.rewardchain)
        for i in range(len(self.rewardchain)):
            summed_reward_value += self.rewardchain[l-i-1]*gamma**i


        if summed_reward_value > 0:
            index = list(self.lastoutput).index(max(list(self.lastoutput)))
            l = [list(self.lastoutput)[i] for i in range(len(list(self.lastoutput)))]
            l[index] = 1
            self.knn.trainWithDataPair(self.lastinput, l, lernrate = 0.05)

        if summed_reward_value < 0:
            index = list(self.lastoutput).index(max(list(self.lastoutput)))
            l = [list(self.lastoutput)[i] for i in range(len(list(self.lastoutput)))]
            l[index] = 0
            self.knn.trainWithDataPair(self.lastinput, l, lernrate = 0.05)
            
