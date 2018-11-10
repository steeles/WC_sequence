"""
new network simulation! a few changes-
- the units in the network just provide pars; the network does the computations
- all variables are in arrays comprising all units
- correspondingly we don't need this complicated trace system anymore. we can record all traces at once.
- one thing- i may want to compute all the deltas in one step and apply them in a separate step, cuz R depends on A
and A depends on R- so i don't want the order to matter.
(ie update a before r, now r sees a[t+1
] not a[t]
"""

