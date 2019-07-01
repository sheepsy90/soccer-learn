import numpy as np
import numpy.random as rnd
import copy
import random

class NeuralNetwork(object):
    """
    This Class defines a Neural Network
    The Size of the InputLayer, HiddenLayer and OutputLayer is given in the Constructor
    The ContextlayerSize is equals to the HiddenLayerSize
    There are two matrices - w0 and w1 which safe the weights for the several connections
    """
    
    def __init__(self, n_in, n_hidden, n_out):
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.n_out = n_out
        self.weight0 = [[(random.random()-0.5) for row in range(n_in+1)] for colum in range(n_hidden)]
        self.weight1 = [[(random.random()-0.5) for row in range(n_hidden+1)] for colum in range(n_out)]

    def _integrate(self, vect):
        """ Integrate the Summation of the Neurons with the Sigmoid Function """
        for i in range(len(vect)):
            vect[i] = self.sigmoid(vect[i])
        return vect   

    def sigmoid(self, value):
        return 1.0 / (1.0 + np.exp(-value))

    def vectToMatrix(self, vect):
        inpMatrix = np.zeros(shape=(0,1))
        for i in range(0,len(vect)):
            inpMatrix = np.append(inpMatrix,[[vect[i]]],axis=0)
        return inpMatrix

    def matToVec(self, mat):
        outVec = []
        for i in mat:
            outVec.append(i[0])
        return outVec

    def calculate(self, inpV):
        inputVector = inpV[:]
        #Combine Context to the InputVector
        if(len(inputVector) != (self.n_in)):
            raise Exception('InputVector don\'t fit.', inputVector)
        length = len(inputVector)    
        combine = inputVector
        combine.append(1)
        #Turn Combine-Vector into a Matrix
        inpMatrix1 = self.vectToMatrix(combine)
        #Start Calculation1
        out1 = np.dot(self.weight0,inpMatrix1)
        outVec1 = self.matToVec(out1)
        #Start Calculation2
        inp2 = self._integrate(outVec1)
        inp2.append(1)
        inpMatrix2 = self.vectToMatrix(inp2)
        out2 = np.dot(self.weight1,inpMatrix2)
        outVec2 = self.matToVec(out2)
        outVec2 = self._integrate(outVec2)
        #combine2Matrix = self.vectToMatrix(out)
        #result = self.calcStep(self.weight1, combine2Matrix)
        return outVec2

#### Learning Part #####


    def calculateLearn(self, inpV):
        inputVector = inpV[:]
        learnResult = []
        #Combine Context to the InputVector
        #print "Starting pure Calculation"
        if(len(inputVector) != (self.n_in)):
            raise Exception('InputVector don\'t fit.', inputVector)
        length = len(inputVector)   
        combine = inputVector
        combine.append(1)
        #Turn Combine-Vector into a Matrix
        inpMatrix1 = self.vectToMatrix(combine)
        #Start Calculation1
        out1 = np.dot(self.weight0,inpMatrix1)
        #Turn OutputMatrix to vector
        outVec1 = self.matToVec(out1)
        cp = outVec1[:]
        outVecIntegrated1 = self._integrate(outVec1)
        learnResult.append(cp)
        ###Start Calculation2
        #Build Input Vector
        inp2 = outVecIntegrated1
        inp2.append(1)
        #Change it to Matrix
        inpMatrix2 = self.vectToMatrix(inp2)
        #Calculate Input \cdot Matrix
        out2 = np.dot(self.weight1,inpMatrix2)
        #Make the Matrix to a Vector
        outVec2 = self.matToVec(out2)
        #Integrate the Vector
        learnResult.append(outVec2[:])
        outVecIntegrated2 = self._integrate(outVec2)
        return learnResult

    def differential(self, vect):
        return self.sigmoid(vect)*(1-self.sigmoid(vect))


    def random_mutation(self):
        if random.random() > 0.5:
            i = int(random.random()*self.n_in)
            j = int(random.random()*self.n_hidden)
            self.weight0[j][i] = random.random()-0.5
        else:
            i = int(random.random()*self.n_hidden)
            j = int(random.random()*self.n_out)
            self.weight1[j][i] = random.random()-0.5

    def trainWithDataPair(self, inputvalues, target, lernrate = 0.6):
        #First step is to propagate the input forward to the network
        erg = self.calculateLearn(inputvalues)
        #Calculate the deltas for the Output Layer
        dk_output = []
        for i in range(self.n_out):
            y = erg[1][i]
            form = (target[i] - self.sigmoid(y)) * self.differential(y)
            dk_output.append(form)
        
        #Calculate the deltas for the Hidden Layer Sigmoid Neurons   
        dk_hidden = []
        #Do it for all Neurons in the Result Set
        for i in range(self.n_hidden):
            net = self.differential(erg[0][i])
            summe = 0
            for k in range(self.n_out):
                summe += dk_output[k]*self.getWeight(i,k,1)
            res = net*summe
            dk_hidden.append(res)
        summe = 0
        for k in range(self.n_out):
                summe += dk_output[k]*self.getWeight(self.n_hidden,k,1)
        dk_hidden.append(summe)


        for i in range(self.n_hidden):
            for k in range(self.n_out):
                self.setWeight(i,k,1,self.getWeight(i,k,1)+(lernrate*self.sigmoid(erg[0][i])* dk_output[k]))

        for k in range(self.n_out):
            self.setWeight(self.n_hidden,k,1,self.getWeight(self.n_hidden,k,1)+(lernrate*1* dk_output[k]))


        for i in range(self.n_in):
            for k in range(self.n_hidden):
                self.setWeight(i,k,0,self.getWeight(i,k,0)+(lernrate*inputvalues[i]* dk_hidden[k]))
        
        for k in range(self.n_hidden):
            self.setWeight(self.n_in,k,0,self.getWeight(self.n_in,k,0)+(lernrate*1* dk_hidden[k]))
        
#### End Of Learning ####


    # Returns the Weight of a Neuron at Position frm in the Layer layer 
    # to the Neuron at Position to in layer+1
    def getWeight(self, frm, to, layer):
        if layer == 0:
            return self.weight0[to][frm]
        elif layer == 1:
            return self.weight1[to][frm]
        else:
            print "This else tree should not be entered"
            return 0

    def setWeight(self, frm, to, layer, weight):
        if layer == 0:
            self.weight0[to][frm] = weight
        elif layer == 1:
            self.weight1[to][frm] = weight
        else:
            print "This else tree should not be entered"
            return 0

    # Shows a Matrix on a Console
    def _show(self, matrix):
        for row in matrix:
            print np.ravel(row)

    # This Method is for Debugging and Developing
    def printStats(self):
        print "WeightLayer0:"
        self._show(self.weight0), "\n"
        print "WeightLayer1:"
        self._show(self.weight1), "\n"
