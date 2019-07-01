import random
import time 

from math import sqrt
from sys import getsizeof
 
from SoccerAgent import *
        
class SoccerAgentQLearn(SoccerAgent):
      
    def __init__(self, logger, statistics): 
        SoccerAgent.__init__(self, logger, statistics)   
        
        # The Q-Learning Structure
        self.init_Q()
        
    def init_Q(self):
        all_status_keys = generate_all_environmental_keys()
        self.Q = {}
        # Direction - Ball X-Coordinate
        for i in [-1, 0, 1]:
            self.Q[i] = {}
            # Direction - Ball Y-Coordinate
            for j in [-1, 0, 1]:
                self.Q[i][j] = {}
                # Key for the Surrounding States
                for k in all_status_keys:
                    self.Q[i][j][k] = {}
                    for u in [-1, 0, 1]:
                        self.Q[i][j][k][u] = {}
                        for v in [-1, 0, 1]:
                            self.Q[i][j][k][u][v] = {}
                            for t in range(10):
                                self.Q[i][j][k][u][v][t] = {}
                                for q in [-1, 0, 1]:
                                    self.Q[i][j][k][u][v][t][q] = {}
                                    for p in [-1, 0, 1]:
                                        self.Q[i][j][k][u][v][t][q][p] = {}
                                        for action in ACTIONS:
                                            self.Q[i][j][k][u][v][t][q][p][action] = random.random()
       
       
    def helper_maximum(self, nextstate):
        x, y, key, u, v, f, q, p = nextstate
        return max(list(self.Q[x][y][key][u][v][f][q][p].values()))
       
    def reset_reward(self):
        self.accumulated_reward = 0
       
    def helper_max_next_action(self):
        x, y, key, u, v, f, q, p = self.agent_state
        dic = self.Q[x][y][key][u][v][f][q][p]
        v=list(dic.values())
        k=list(dic.keys())
        return k[v.index(max(v))]
        
    def helper_max_next_action_outside(self, dic):
        v=list(dic.values())
        k=list(dic.keys())
        return k[v.index(max(v))]
       
    def perform_q_learning(self, current, action, reward, nextstate, alpha=0.2, gamma=0.9):
        #print "Learning with: %s -> %s with reward %i and action %s" % (str(current), str(nextstate), reward, action)
        x, y, key, u, v, f, q, p = current
        self.Q[x][y][key][u][v][f][q][p][action] = (1 - alpha)*self.Q[x][y][key][u][v][f][q][p][action] + alpha * (reward + gamma * self.helper_maximum(nextstate))

    def decide_next_action(self, learning):
        if learning:
            action = ACTIONS[int(len(ACTIONS)*random.random())]
            if random.random() > 0.2:
                action = self.helper_max_next_action()
            return action
        else:
            action = self.helper_max_next_action()
            if random.random() > 0.95:
                action = ACTIONS[int(len(ACTIONS)*random.random())]
            return action
        
    def perform(self, learning):
        # Determine the next action
        nextaction = self.decide_next_action(learning)
        if learning == False:
            print nextaction
        # Save current state
        current_state = self.agent_state
        # Save the current position
        xf, yf = self.agent_position
        # Execute it
        reward = self.execute_action(nextaction)  
        # Add the accumulating reward
        self.statistics.add_reward(reward)    
        # Update the state
        self.update_state(xf, yf)
        # Save it for learning
        afteraction_state = self.agent_state
        # Try to learn things
        if learning:
            self.perform_q_learning(current_state, nextaction, reward, afteraction_state)
        if not learning:
            # Log events
            self.statistics.write_state_to_file(self.is_ball_outside_field(), self.is_ball_in_rival_goal(), self.ball, [xf,yf], current_state, nextaction)
        
        
        # Check if the ball is still in game
        if self.is_ball_in_goal() or self.is_ball_outside_field():
            self.reset_positions()
            self.statistics.reset()


def generate_all_environmental_keys():
    """ This method generates all possible keys for representing the near environment """
    possibles = [state_WALL, state_FIELD, state_BALL]
    lst =[]
    for s1 in possibles:
        for s2 in possibles:
            for s3 in possibles:
                for s4 in possibles:
                    st ="#".join([str(s1),str(s2),str(s3),str(s4)])
                    lst.append(st)
    return lst


def load_helper(loaded):
    #Redefine Q
    # Direction - Ball X-Coordinate
    # Direction - Ball X-Coordinate
    Q = {}
    for i in [-1, 0, 1]:
        Q[i] = {}
        # Direction - Ball Y-Coordinate
        for j in [-1, 0, 1]:
            Q[i][j] = {}
            # Key for the Surrounding States
            for k in generate_all_environmental_keys():
                Q[i][j][k] = {}
                for u in [-1, 0, 1]:
                    Q[i][j][k][u] = {}
                    for v in [-1, 0, 1]:
                        Q[i][j][k][u][v] = {}
                        for t in range(10):
                            Q[i][j][k][u][v][t] = {}
                            for q in [-1, 0, 1]:
                                Q[i][j][k][u][v][t][q] = {}
                                for p in [-1, 0, 1]:
                                    Q[i][j][k][u][v][t][q][p] = {}
                                    for action in ACTIONS:
                                        Q[i][j][k][u][v][t][q][p][action] = loaded[str(i)][str(j)][k][str(u)][str(v)][str(t)][str(q)][str(p)][action]
    return Q


