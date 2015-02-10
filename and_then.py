# andthen in WC
from pylab import *
from numpy import *
from matplotlib.mlab import *

def f_exc(x, k = .1, theta = .2):
	return 1/(1+exp(-(x-theta)/k)) - 1/(1+exp(theta/k))

def f_S(x,k=.1,theta=.8):
	return 1/(1+exp(-(x-theta)/k)) - 1/(1+exp(theta/k))

t_in_ms = 500
dt = 1
t_tot = int(t_in_ms/dt)
tax = linspace(dt,t_in_ms,t_tot)

E1 = zeros(t_tot) # excitatory unit receiving the first input
E2 = zeros(t_tot) # excitatory unit receiving second input
Isyn = zeros(t_tot)
Iext = zeros(t_tot)
S_NMDA_1 = zeros(t_tot) # synaptic variable activated by unit 1

stim_length = 30 # ms
stim_strength = 1
SOA = 100
Inp1 = zeros(t_tot)
Inp1[:stim_length/dt] = stim_strength
Inp2 = zeros(t_tot)
Inp2[SOA:SOA+stim_length] = stim_strength

tau_NMDA = 100
tau_r = 10

gee = .56
G = .641
gNMDA = .02
gExc = .0#2
gInp1 = .07
for i in xrange(1):
	gNMDA /=1.
	gExc /=1.
	for t in xrange(t_tot-1):
 

 		E1[t+1] = E1[t] + \
 			(-E1[t] + f_exc(gInp1 * Inp1[t] + gee*E1[t])) * dt/tau_r
		S_NMDA_1[t+1] = S_NMDA_1[t] + \
			(-S_NMDA_1[t]/tau_NMDA + (1-S_NMDA_1[t]) *G* f_S(E1[t+1]))*dt # NMDA gating for FF input

		Isyn[t+1] = gNMDA*S_NMDA_1[t+1]
		Iext[t+1] = gExc*Inp2[t+1]

		E2[t+1] = E2[t] + \
			(-E2[t] + f_exc(Isyn[t+1] + Iext[t+1] + gee*E2[t]))*dt/tau_r 

	figure()
	title(str(gNMDA) + '; max(Isyn)=' + str(Isyn.max()))
	plot(tax,Isyn,'c')
	plot(tax,E2,'b')
	plot(tax,Iext,'g')
	plot(tax,gInp1*Inp1,'y')
	plot(tax,E1,'m')

	plot(tax,S_NMDA_1,'k')
	show(block=False)