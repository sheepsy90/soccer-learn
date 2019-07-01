import json
import random 

from SoccerAgent import SoccerAgent, load_helper, generate_all_environmental_keys, ACTIONS
from Statistics import Statistics
from KNN import KNN
from Logger import Logger
from SoccerAgentKNN import SoccerAgentKNN
from FieldView import FieldView

all_status_keys = generate_all_environmental_keys()


logger = Logger()
statistics = Statistics()
knn = KNN()

state = [1, 1, '1#1#1#1', -1, -1, 0, 0, 0]

index = knn.process(state)
x = knn.lastoutput

knn.learn_with_reward(10)
knn.learn_with_reward(-10)

index2 = knn.process(state)
y = knn.lastoutput


z = [x[i] > y[i] for i in range(len(x))]

print
print index
print x
print y
print z
print index2
print

for i in range(10):
    knn.learn_with_reward(-10)
    index2 = knn.process(state)
    print "I:\t", index2
    print "L:\t", knn.lastoutput
