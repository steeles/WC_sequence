# test_WC 1/23/2015 reappropriating tester code for the WC translated
# ML synfire model- for what parameters is the sequence detected?

# from pylab import *
from numpy import *
from matplotlib.mlab import *
import pdb

execfile('SFA_WC_pop_func.py')
execfile('stim_maker_WC.py')

test_dfs = linspace(3,12,12)
#test_Phis = logspace(.001,.02,5)
#test_Phis = test_Phis[1:]
#test_Phis = array([.0021])#, .0022])

test_ITIs = linspace(.030,.130,12)

detect_map = zeros((len(test_dfs),len(test_ITIs)))
#suppress_map = zeros((len(test_dfs),len(test_ITIs)))

thresh = .5 # threshold to say a pop was activated
#dind = 0 

for dind in xrange(len(test_dfs)):
	#b_sDetect = False
	#b_sSuppress= False

	for ind in xrange(len(test_ITIs)):

		# i think this can be simplified for now

		[tax,E,I,Isyn,stim] = SFA_pop(
			test_dfs[dind], # let's flip that df axis so low dfs at bottom
			test_ITIs[ind])
			#test_ITIs[-ind-1],test_dfs[dind]) # working down from hi to lo iti
			
		# I would like an easy way to test that changing phis doesn't
		#get me spurious stim firing, but i'm lazy right now. 
		#later i can update fxn to eliminate ff weights

		if any(E[2,:]>thresh): #& ~b_sDetect: 		# working down over ITI 
			detect_map[dind,ind] = 1#test_ITIs[-ind-1] # when do we start 
			#b_sDetect = True						# to detect

		#if ~any(V[2,:]>thresh) & b_sDetect & ~b_sSuppress: # if at higher ITI
		#	suppress_map[dind,pind] = test_ITIs[-ind-1]  # we could detect
		#	b_sSuppress = True                            # but now we can't


#np.set_printoptions(precision=2)
figure()
#ext = [test_ITIs[0],test_ITIs[-1],test_dfs[0],test_dfs[-1]]
#xlim(ext[:2])
#ylim(ext[2:])

#ax = axes([test_ITIs[0],test_ITIs[-1],test_dfs[0],
 #	test_dfs[-1]], frameon=False)
#ax.set_axis_off()
#ax.set_xlim(test_ITIs[0],test_ITIs[-1])
#ax.set_ylim(test_dfs[0],test_dfs[-1])
#title('TRT of first detected sequence')
np.set_printoptions(precision=2)
det_plot = imshow(detect_map,interpolation='nearest',cmap='gray',
	origin = 'lower')
#xscale('log')
xlabel('ITI (ms)')
ylabel('df (semitones)')
#colorbar()
xt = ['{:.2f}'.format(i) for i in test_ITIs]
yt = ['{:.2f}'.format(i) for i in test_dfs]
xticks(arange(len(test_ITIs)),xt*1000)
yticks(arange(len(test_dfs)),yt)#,test_ITIs)
#yticks(test_dfs)
show(block=False)



# figure()
# #title('TRT of first suppressed sequence')
# imshow(suppress_map,interpolation='nearest',
# 	extent=[test_Phis[0],test_Phis[-1],test_dfs[0],
# 	test_dfs[-1]],cmap='gray')
# #xscale('log')
# xlabel('ITI')
# ylabel('df')
# colorbar()
# xticks(test_Phis,test_Phis)
# show(block=False)

	#pdb.set_trace()




