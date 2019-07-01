
class Logger():
    
    def __init__(self):
        self.counter = 0
        self.last = "Initial Message"

    def log(self, message):
        if self.last != message:
            print self.last + " (%i)" % self.counter
            self.last = message
            self.counter = 1
        else:
            self.counter +=1
