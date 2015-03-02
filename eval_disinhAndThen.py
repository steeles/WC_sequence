''' test script to outline conditions for disinhibition circuit;
inp1-inp2 should result in E1, fastInh, E2 go off, slowInh does not.
inp2 only should result in slowInh goes off, E2 does not  
plot firing rates for all 3 units, inputs, and syn currents, 
and look at r' vs r '''

import pylab as pl 
import numpy as np 
import matplotlib.mlab as plt 


from pylab import *
from numpy import *
from matplotlib.mlab import *

from disinhAndThen_func import disinhAndThen
from plotUnits import plotUnits, plotNullclines # this is going to need to be reworked

thresh = .5

default_run= disinhAndThen()
print ('Running system defaults- 2 inputs, ' 
'2 excitatory units with an NMDA synapse between them')

errCount=0

if max(default_run['E1'])>thresh:
	print 'E1 fires'

if max(default_run['fastInh'])>thresh:
	print 'Fast feedback inhibition kicks in'

if max(default_run['slowInh'])<thresh:
	print 'Slow feedforward inhibition never makes it'
else:
	print 'WARNING: Feedforward inhibition is engaged'

if max(default_run['E2'])>thresh:
	print 'E2 goes off'
else: 
	print "E2 doesn't fire"; errCount +=1; plotUnits(**default_run)



Inp2_only=and_then(gInp1=0)
'Delivering only the second input'

if max(inp2_only['slowInh'])>thresh:
	print 'Slow feedforward inhibition kicks in'
else:
	print 'WARNING: no feedback inhibition'

if max(inp2_only['E2'])<thresh:
	print 'Unit 2 does not fire'
else:
	'Unit 2 goes off without synaptic input from unit 1!'
	errCount +=1
	plot_and_then(**inp2_only)

no_stim=and_then(gInp2=0)

if max(no_stim['E2'])>thresh:
	print 'Unit 2 fires ...without input 2'
	errCount +=1
if errCount==0: print ' the logic checks out'


plot_and_then(**default_run)




