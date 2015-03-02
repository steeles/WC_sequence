''' run and_then_func with certain currents blocked and 
see if it does the right thing; 
plot firing rates for all 3 units, inputs, and syn currents, 
and look at r' vs r '''
from pylab import *
from numpy import *
from matplotlib.mlab import *

from and_then_func import and_then
from plot_and_then import plot_and_then
import pdb

thresh = .5

default_run=and_then()

errCount=0
if max(default_run['E2'])>thresh:
	print 'E2 goes off'
else: 
	print "E2 doesn't fire"; errCount +=1; plot_and_then(**default_run)


no_synapse=and_then(gNMDA=0)

if max(no_synapse['E2'])>thresh:
	print '...without NMDA current'
	errCount +=1
	plot_and_then(**no_synapse)

no_stim=and_then(gInp2=0)

if max(no_stim['E2'])>thresh:
	print '...without input 2'
	errCount +=1
if errCount==0: print ' the logic checks out'


#plot_and_then(**default_run)





