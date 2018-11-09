# disinhibition circuit in WC
from numpy import *

def f_exc(x, k = .1, theta = .3):
	return 1/(1+exp(-(x-theta)/k)) - 1/(1+exp(theta/k))

def f_Iff(x, k = .1, theta = .4):
	return 1/(1+exp(-(x-theta)/k))

def f_NMDA(x,k,theta):

t_in_ms = 2000
dt = 1
t_tot = int(t_in_ms/dt)
tax = linspace(dt,t_in_ms,t_tot)

E1 = zeros(t_tot) # excitatory unit receiving the first input
E2 = zeros(t_tot) # excitatory unit receiving second input
Iff = zeros(t_tot) # feedforward inhibitory unit
# Ir = zeros(t_tot) # recurrent inhibitory unit

S_NMDA_1 = zeros(t_tot) # synaptic variable for input 1

stim_length = 30 # ms
stim_strength = .2
SOA = 100

Inp1 = zeros(t_tot)
Inp1[:stim_length/dt] = stim_strength
Inp2 = zeros(t_tot)
Inp2[SOA:SOA+stim_length] = stim_strength

for t in xrange(t_tot-1):
	S_NMDA_1[t+1] = S_NMDA_1[t] + 
		(-S_NMDA_1[t]/tau_s + (1-S_NMDA_1[t]) * Inp1)*dt # NMDA gating for FF input

	S_NMDA_2[t+1] = S_NMDA_2[t] +
		(-S_NMDA_2[t]/tau_s + (1-S_NMDA_2[t]) * Inp2)*dt

			* gamma * f(x1[t+1])/1000) * dt