import matplotlib.pyplot as plt
import math


class Element(object):

    def __init__(self, line):
        self.restline = False
        if line == "RESET":
            self.restline = True
            return

        a = line.split(";")
        self.bool1 = 1 if a[0] == "True" else False
        self.bool2 = 1 if a[1] == "True" else False
        self.pos1 = eval(a[2])
        self.pos2 = eval(a[3])
        self.state = eval(a[4])
        self.action = a[5]

        #print self.bool1, self.bool1, self.pos1, self.pos2, self.state, self.action

    def get_goal_distance(self):
        return math.sqrt((self.pos1[1] - 0)**2 + (self.pos1[0] - 30)**2)

    def is_in_goal(self):
        return self.bool2

    def agent_distance_to_ball(self):
        return math.sqrt((self.pos1[0] - self.pos2[0])**2 + (self.pos1[1] - self.pos2[1])**2)

    def is_resetline(self):
        return self.restline


class Analyser():


    def __init__(self, fignum, logfile):
        # Set the Figurenumber
        self.fignum = fignum
        # Load the Data
        self.load_data(logfile)
        # analyse it
        self.analyzeComplete()
        # analyze Chunks
        self.analyzeChunks()

    def analyzeComplete(self):

        btgd = [e.get_goal_distance() for e in self.elements]
        ibig = [e.is_in_goal()/2.0 for e in self.elements]
        rset = [e.is_resetline()*10 for e in self.elements]
        adtb = [e.agent_distance_to_ball() for e in self.elements]

        num_goals = len([i for i in ibig if i >= 10.0])
        if num_goals != 0:
            goals_per_tick = (float(num_goals) / float(len(ibig)))
        else:
            goals_per_tick = 0
        sum_ball_to_goal_distance = sum(btgd) / float(len(btgd))


        variance = [btgd[i] - sum_ball_to_goal_distance for i in xrange(len(btgd))]

        variance_left = [i for i in variance if i < 0]
        variance_right = [i for i in variance if i >= 0]

        variance_left = sum(variance_left) / len(variance_left)
        variance_right = sum(variance_right) / len(variance_right)


        print "\tNumber of Goals: %i" % num_goals
        print "\tNumber of Ticks: %i" % len(btgd)

        print "\tGoals per Tick: %f" % goals_per_tick
        print "\tAverage Ball Distance to Goal: %f" % sum_ball_to_goal_distance
        print "\tAverage Ball Distance to Goal Variance Left: %f" % variance_left
        print "\tAverage Ball Distance to Goal Variance Right: %f" % variance_right

        print "\tAverage Agent Distance to Ball: %f" % (sum(adtb) / len(adtb))
        print

        fig = plt.figure(self.fignum)
        ax = fig.add_subplot(111)
        ax.plot(range(len(btgd)), btgd, 'r-')
        ax.plot(range(len(ibig)), ibig, 'bo', markersize=5)
        ax.plot(range(len(adtb)), adtb, 'g-')
        ax.plot(range(len(rset)), rset, 'y-')


    def analyzeChunks(self):
        print "\tNumber of Chunks: %i" % len(self.chunks)
        fig = plt.figure(self.fignum+1)
        ax = fig.add_subplot(111)
        for chu in self.chunks:
            if len(chu) > 0:
                c = [e.get_goal_distance() for e in chu]
                m = max(c)
                c = [i/m for i in c]

                adtb = [e.agent_distance_to_ball() for e in chu]
                adtb_max = max(adtb)
                adtb = [a/adtb_max for a in adtb]

                ax.plot(range(len(c)), c, 'r-')
                ax.plot(range(len(adtb)), adtb, 'b-')


    def load_data(self, logfile):
        with open(logfile, 'r') as f:
            input = f.read()
            lines = input.split("\n")
            print "[LOADING] File: %s" % logfile
            print "[LOADING] Numbers of Lines: %i" % (len(lines)-1)
            self.elements = [Element(l) for l in lines if len(l) > 0]
            self.elements = [e for e in self.elements if not e.is_resetline()]
            # Loading Chunks
            self.chunks = []
            chunk = []
            for l in lines:
                if len(l) > 0:
                    e = Element(l)
                    if e.is_resetline():
                        self.chunks.append(chunk)
                        chunk = []
                    else:
                        chunk.append(e)




a1 = Analyser(1, "./logs/SoccerAgentKNN.log")
a2 = Analyser(3, "./logs/SoccerAgentQLearning.log")
a2 = Analyser(5, "./logs/SoccerAgentKNN_rand.log")

# Call that for showing the graphs
plt.show()



