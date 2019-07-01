import random 
import json
import sys 
import matplotlib
import time

matplotlib.interactive(True)

### Some Configuration Values ###


# Saving
SAVE_RESULTS    = False
SAVE_PATH       = "./qmaps/qmap3"

# Loading
LOAD_BEHAVIOUR  = True
LOAD_PATH       = "./qmaps/qmap3"

#Learning
LEARNING        = False    
ITERATIONS      = 7500000
RESET_AFTER     = 250

#Viewing
VIEW_BEHAVIOUR  = True
VIEW_ITERATIONS = 10000
VIEW_RESET      = 250  
#################################

from SoccerAgentQLearn import SoccerAgentQLearn, load_helper
from FieldView import FieldView
from Statistics import Statistics
from Logger import Logger

logger = Logger()
statistics = Statistics("logs/SoccerAgentQLearning.log")
sagent = SoccerAgentQLearn(logger, statistics)

##############################
# Perform the Learning first #
##############################
if LEARNING:
    print "[LEARNING] Started"
    learning_start_time = time.time()
    for i in xrange(ITERATIONS):
        # Call the agent with learning set to true
        sagent.perform(learning=True)
        # Check if reset is necessary
        if i % RESET_AFTER == 0:
            sagent.reset_positions()
        # Print Progress
        if (i % (ITERATIONS/10)) == 0:
            logger.log("[PROGRESS]: %s percent!" % str(100*float(i)/ITERATIONS))
    learning_fin_time = time.time()
    print "[LEARNING] Finished"
    print "[LEARNING] Took %f seconds" % (learning_fin_time-learning_start_time)

if SAVE_RESULTS:
    print "[SAVING] Q-Dictionary to %s" % (SAVE_PATH)
    with open(SAVE_PATH, "w") as f:
        f.write(json.dumps(sagent.Q))
    print "[SAVING] Done"


if LOAD_BEHAVIOUR:
    print "[LOADING] Q-Dictionary from %s" % (LOAD_PATH)
    with open(LOAD_PATH, "r") as f:
        loaded = json.loads(f.read())
    # Bring it into the right format
    sagent.Q = load_helper(loaded)
    print "[LOADING] Done"
   



if VIEW_BEHAVIOUR:
    fieldview = FieldView(sagent)
    sagent.reset_positions()
    sagent.accumulated_reward = 0
    for i in xrange(VIEW_ITERATIONS):
        sagent.perform(learning=False)
        fieldview.draw_now_and_wait(0.01)
        if i % VIEW_RESET == 0:
            sagent.reset_positions()


    





        
