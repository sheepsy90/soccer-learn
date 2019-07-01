import random
import time 

from SoccerAgent import *
from math import sqrt


class SoccerAgentKNN(SoccerAgent):
      
    def __init__(self, logger, statistics, knn): 
        SoccerAgent.__init__(self, logger, statistics)
        
        self.knn = knn
        self.goals = 0

    ###########################
    ### Overwritten Methods ###
    ###########################

    def decide_next_action(self, learning):
        """ Calculate the output of the neural network """
        if learning:
            if random.random() > 0.8:
                action = ACTIONS[int(len(ACTIONS)*random.random())]
            else:
                index = self.knn.process(self.agent_state)
                action = ACTIONS[index] 
        else:
            index = self.knn.process(self.agent_state)
            action = ACTIONS[index] 
        return action
        
    def perform(self, learning):
        # Determine the next action
        nextaction = self.decide_next_action(learning)
        # Save current state
        current_state = self.agent_state
        # Save the former position
        former_position = self.agent_position
        # Save the current position
        fpx, fpy = self.agent_position
        # Execute it
        reward = self.execute_action(nextaction)  
        # Add the accumulating reward
        self.statistics.add_reward(reward)   
        # Update the state
        self.update_state(fpx, fpy)
        # Save it for learning
        afteraction_state = self.agent_state
        # Try to learn things
        if learning:
            self.knn.learn_with_reward(reward)
        if not learning:
            # Log events
            self.statistics.write_state_to_file(self.is_ball_outside_field(), self.is_ball_in_goal(), self.ball, former_position, current_state, nextaction)
        
        # Check if the ball is still in game
        if self.is_ball_in_goal() or self.is_ball_outside_field():
            self.reset_positions()
            self.statistics.reset()
        return reward
