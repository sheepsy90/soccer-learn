import matplotlib
import time

matplotlib.interactive(True)

### Some Configuration Values ###


# Saving
SAVE_RESULTS    = False
SAVE_PATH       = "./knns/knn3"

# Loading
LOAD_BEHAVIOUR  = True
LOAD_PATH       = "./knns/knn2"

#Learning
LEARNING        = False
ITERATIONS      = 75000
RESET_AFTER     = 250

#Viewing
VIEW_BEHAVIOUR  = True
VIEW_ITERATIONS = 10000
VIEW_RESET      = 250  
#################################

from SoccerAgentKNN import SoccerAgentKNN
from Statistics import Statistics
from Logger import Logger
from FieldView import FieldView

from neuro.KNN import KNN

logger = Logger()
statistics = Statistics("logs/SoccerAgentKNN_rand.log")
knn = KNN()

sagentknn = SoccerAgentKNN(logger, statistics, knn)


if LEARNING:
    print "[LEARNING] Started"
    learning_start_time = time.time()
    for i in xrange(ITERATIONS):
        # Call the agent with learning set to true
        sagentknn.perform(learning=True)
        # Check if reset is necessary
        if i % RESET_AFTER == 0:
            sagentknn.reset_positions()
        # Print Progress
        if (i % (ITERATIONS/10)) == 0:
            logger.log("[PROGRESS]: %s percent!" % str(100*float(i)/ITERATIONS))
    learning_fin_time = time.time()
    print "[LEARNING] Finished"
    print "[LEARNING] Took %f seconds" % (learning_fin_time-learning_start_time)

if SAVE_RESULTS:
    print "[SAVING] NeuralNetwork to %s" % (SAVE_PATH)
    with open(SAVE_PATH, "w") as f:
        f.write(str(sagentknn.knn.knn.weight0) + "\n" + str(sagentknn.knn.knn.weight1))
    print "[SAVING] Done"

if LOAD_BEHAVIOUR:
    print "[LOADING] NeuralNetwork from %s" % (LOAD_PATH)
    with open(LOAD_PATH, "r") as f:
        lines = f.read().split("\n")
    w0 = eval(lines[0])
    w1 = eval(lines[1])
    # Bring it into the right format
    sagentknn.knn.knn.weight0 = w0
    sagentknn.knn.knn.weight1 = w1
    print "[LOADING] Done"
    
if VIEW_BEHAVIOUR:
    fieldview = FieldView(sagentknn)
    sagentknn.reset_positions()
    sagentknn.accumulated_reward = 0
    for i in xrange(VIEW_ITERATIONS):
        sagentknn.perform(learning=False)
        fieldview.draw_now_and_wait(0.01)
        if i % VIEW_RESET == 0:
            sagentknn.reset_positions()


    





        


