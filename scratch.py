

from collections import namedtuple

Connection=namedtuple("Connection",["source","strength"])
class Unit(object):

# these first two methods just let me set up units and connections:
    def __init__(self,par=1, response=[0], connections=[]):
    	self.par=par
    	self.response=response
    	self.connections=dict()#[]

    def receiveConnection(self,source,strength,label):
    	# source is some other variable, strength is probably fixed but
    	# i'd like it to be able to change, too
    	#cx = Connection(label,source,strength)
    	#self.connections.append(cx)
    	self.connections[label]=Connection(source,strength)

# stuff that gets done iteratively through the sim    	
    def update(self):
    	netInput=0.
    	# based on the value of all the sources and weights right now,
    	for item in self.connections.itervalues():
    		netInput+= item.source[0] * item.strength
    	self.response[0] += self.par * netInput

if __name__=="__main__":
	Unit1 = Unit()
	Unit2 = Unit(response=[1])

	Unit1.receiveConnection(source=Unit2.response,strength=.5,label="U2toU1")
	Unit2.receiveConnection(source=Unit2.response,strength=-.5,label="negativeFeedback")

	for t in xrange(10):
		Unit1.update()
		print 'Unit1:    ' + str(Unit1.response)
		Unit2.update()
		print 'Unit2:    ' + str(Unit2.response)

