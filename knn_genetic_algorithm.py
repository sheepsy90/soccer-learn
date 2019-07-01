import sys

from SoccerAgentKNN import SoccerAgentKNN
from FieldView import FieldView
from Statistics import Statistics
from Logger import Logger
from KNN import KNN

logger = Logger()
statistics = Statistics()
knn = KNN()
sagent = SoccerAgentKNN(logger, statistics, knn)

import cProfile
import re

def multiple():
    for i in range(10000):
        knn.process([1,1,"1#1#1#1",1, 1, 1, 1, 1])

cProfile.run('multiple()')

sys.exit(0)

def evaluate(bol=True):
    for i in xrange(15000):
        sagent.perform(bol)
        if i % 50 == 0:
            sagent.reset_positions()
        if i % 7500 == 0:
            print "Step: " + str(i)
    print sagent.goals

evaluate()

evaluate(False)

"""
fieldview = FieldView(sagent)
sagent.reset_positions()
for i in xrange(100000):
    sagent.perform(learning=False)
    fieldview.draw_now_and_wait(0.01)
    if i % 750 == 0:
        sagent.reset_positions()
"""
