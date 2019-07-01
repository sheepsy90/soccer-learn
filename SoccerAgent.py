import random
import time 

from math import sqrt
 
state_WALL  = 0
state_FIELD = 1
state_BALL  = 2

action_LEFT  = "LEFT"
action_RIGHT = "RIGHT"
action_UP    = "UP"
action_DOWN  = "DOWN"
action_KICK  = "KICK"

# All possible ACTIONS
ACTIONS = [action_RIGHT, action_LEFT, action_UP, action_DOWN, action_KICK]

class SoccerAgent(object):
      
    def __init__(self, logger, statistics): 
        # Bind both paramters to variables
        self.logger = logger
        self.statistics = statistics
    
        # The Current Position of the Agent (x, y)
        self.agent_position = [12, 3]
        # Where the ball lays
        self.ball = [13, 6]
       
        # The State of the agent
        self.update_state(self.agent_position[0], self.agent_position[1])


    #####################################################################
    ### This part is extracting high level features out of the states ###
    #####################################################################

    ## Ball Things

    def get_ball_vector(self):
        """ This method returns a vector with the direction where the ball is """
        x, y = 0, 0
        if self.ball[0] != self.agent_position[0]:
            x = self.sign (self.ball[0] - self.agent_position[0])
        if self.ball[1] != self.agent_position[1]:
            y = self.sign (self.ball[1] - self.agent_position[1])
        return [x,y]
        
    def get_limited_balldistance(self):
        """ This method returns the ball distance as manhatten distance up to 19.
            If it is higher than 19 it still will be 19.
        """
        return [min(9, abs(self.ball[0] - self.agent_position[0]) + abs(self.ball[1]-self.agent_position[1]))]    
        
    def get_manhatten_balldistance(self):
        return abs(self.ball[0]- self.agent_position[0]) + abs(self.ball[1] - self.agent_position[1])
    
    ## Location Things
    
    def get_simplified_position(self):
        """ This method returns the absolute location with a precision of meter as you will """
        return [self.agent_position[0] / 10, self.agent_position[1] / 10]
        
    ## Movement Things
    
    def get_movment_vector(self, xf, yf):
        x, y = self.agent_position
        return [self.sign(x-xf), self.sign(y-yf)]
       
    ## Near Surroundings
    def generate_surrounding(self):
        """ This method returns the string representing the surroundings of the agent
            The idecies are as follows:
            - 0 -
            3 A 1
            - 2 -
            where A is the Agent and 0 to 3 the index positions
        """
        surrounding = [state_FIELD, state_FIELD, state_FIELD, state_FIELD]
        x,y = self.agent_position
        
        # Fill the walls if there are some
        if x == -7: surrounding[3] = state_WALL
        elif x == 45: surrounding[1] = state_WALL
       
        if y == 66: surrounding[0] = state_WALL
        elif y == -7: surrounding[2] = state_WALL
            
        # Fill the ball if there is one
        ballx, bally = self.ball
        if x     == ballx and y+1 == bally: surrounding[0] = state_BALL
        elif x-1 == ballx and y   == bally: surrounding[3] = state_BALL
        elif x+1 == ballx and y   == bally: surrounding[1] = state_BALL
        elif x   == ballx and y-1 == bally: surrounding[2] = state_BALL

        return ["#".join([str(i) for i in surrounding])]
       
    ## Goal stuff
       
    def get_goal_vector(self, down = False):
        """ This method returns the vector to the center of the goal """
        if down == True:
            y = 0
        else:
            y = 60
        
        xgoalcenter, ygoalcenter = 0, 0
        if (self.agent_position[0] - 20) !=0:
            xgoalcenter = self.sign(self.agent_position[0] - 20)
        if (self.agent_position[1] - y) !=0:
            ygoalcenter = self.sign(self.agent_position[1] - y)
        return [xgoalcenter, ygoalcenter]
       
    #####################################
    ### Boolean Flags about the State ###
    #####################################
    
    def is_ball_in_goal(self):
        x,y = self.ball
        return x > 10 and x < 30 and y > 60;
        
    def is_ball_in_rival_goal(self):
        x,y = self.ball
        return x > 10 and x < 30 and y < 0;
               
    def is_ball_outside_field(self):
        """ Returns true if the ball is outside the field """
        return (self.ball[0] < 0 or self.ball[0] > 39 or self.ball[1] < 0 or self.ball[1] > 59)
                  
    def is_ball_adjacent(self):
        """ Returns true if the ball is next to the agent """
        return str(state_BALL) in self.agent_state[2]
        
    def dont_blocked(self, deltax, deltay):
        return not (self.ball[0] == self.agent_position[0]+deltax and self.ball[1] == self.agent_position[1]+deltay)
    
    #######################################
    ### This part is for helper methods ###
    #######################################
    
    
    def update_state(self, former_x, former_y):
        self.agent_state = self.get_ball_vector() 
        self.agent_state += self.generate_surrounding() 
        self.agent_state += self.get_goal_vector() 
        self.agent_state += self.get_limited_balldistance()
        self.agent_state += self.get_movment_vector(former_x, former_y)
    
    def sign(self, nr):
        if nr > 0:
            return 1
        elif nr < 0:
            return -1
        else:
            return 0       


    def ball_to_goal_distance(self, down = False):
        if down == False:
            return abs(self.ball[0] - 30) + abs(self.ball[1] - 60)
        else:
            return abs(self.ball[0] - 30) + abs(self.ball[1] - 0)
            
            
    ##################################################################
    ### Some methods which are important for the reward resolution ###
    ##################################################################
        
    def get_absolute_balldistance_reward(self, formerdistance):
        current = self.get_manhatten_balldistance()
        if (current == 1 and formerdistance == 2) or (current == 2 and formerdistance == 1): 
            return 0
        elif current <= formerdistance: 
            return 10
        else: 
            return -10
        
    def calculate_ball_to_goal_reward(self):
        return max(1, 50 - sqrt((self.ball[0] - 30)**2 + (self.ball[1] - 50)**2))
        
    #########################################################################################
    ### The Part where the choosen action is executed and the reward is beeing calculated ###
    #########################################################################################
    
    def execute_action(self, nextaction):
        """ This method executes the action """
        reward = 0
        if nextaction == action_LEFT:
            if self.agent_position[0] > -7 and self.dont_blocked(-1,0):
                f = self.get_manhatten_balldistance()
                self.agent_position[0] -= 1
                reward = self.get_absolute_balldistance_reward(f)
            else:
                reward = -10
        elif nextaction == action_RIGHT and self.dont_blocked(+1,0):
            if self.agent_position[0] < 45:
                f = self.get_manhatten_balldistance()
                self.agent_position[0] += 1
                reward = self.get_absolute_balldistance_reward(f)
            else:
                reward = -10
        elif nextaction == action_UP and self.dont_blocked(0,+1):
            if self.agent_position[1] < 66:
                f = self.get_manhatten_balldistance()
                self.agent_position[1] += 1
                reward = self.get_absolute_balldistance_reward(f)
            else:
                reward = -10
        elif nextaction == action_DOWN and self.dont_blocked(0,-1):
            if self.agent_position[1] > -7:
                f = self.get_manhatten_balldistance()
                self.agent_position[1] -= 1
                reward = self.get_absolute_balldistance_reward(f)
            else:
                reward = -10
        elif nextaction == action_KICK:
            if self.is_ball_adjacent():
                addition = self.get_ball_vector()
                f = self.ball_to_goal_distance(down=True)
                self.ball[0] += addition[0]*int(3*random.random())+2*addition[0]
                self.ball[1] += addition[1]*int(3*random.random())+2*addition[1]
                reward = self.sign(f - self.ball_to_goal_distance(down=True))*5
                if self.is_ball_in_goal():
                    reward = -1000
                if self.is_ball_in_rival_goal():
                    reward = 1000
            else:
                reward = -10
        else:
            reward = -10      
        return reward
        

    def choose_random_ball_position(self):
        self.ball = [10+int(random.random()*38), 10 + int(random.random()* 58)]
       
    def reset_positions(self):
        """ This method resets the agents and the balls position to random values """
        # Reset the agents position to somewhere on the field
        #self.agent_position =[1+int(random.random()*38), 1 + int(random.random()*58)]
        
        # Resets the ball position to somewhere on the field exept the border and the goal
        self.choose_random_ball_position()
        while (self.agent_position == self.ball) or self.is_ball_in_goal():
            self.choose_random_ball_position()

        # Set the Agent State
        self.update_state(self.agent_position[0], self.agent_position[1])
        
    ###########################
    ### Overridable Methods ###
    ###########################
    
    def perform(self, learning):
        """ This method actually makes all the steps for one iteration """
        raise NotImplementedError()

    def decide_next_action(self, learning):
        """ This method decides which is the next action to perform """
        raise NotImplementedError()

