import json
import sys

class Statistics(object):

    def __init__(self, path):
        # The goal
        self.reward =[]
        # The Path
        self.PATH = path
        
    def reset(self):
        self.reward = []
       
    def add_reward(self, reward):
        self.reward.append(reward)
        if len(self.reward) % 10000 == 0:
            print "Average: " + str(float(sum(self.reward))/len(self.reward))
            self.reset()

    def write_state_to_file(self, outside, ingoal, ball, position, state, action):
        with open(self.PATH, 'a') as f:
            f.write(str(outside) + ";" + str(ingoal) + ";" + str(ball) + ";" + str(position) + ";" + str(state) + ";" + str(action) + "\n")

    def reset(self):
        with open(self.PATH, 'a') as f:
            f.write("RESET\n")

