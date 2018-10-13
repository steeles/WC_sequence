# WC_sequence

_A python framework for building recurrently connected Wilson-Cowan neuronal populations,
synaptic weights/ footprints, and basic stimulus features, as well as running simulations 
and visualizing._


Getting started:
Install requirements:
- open a terminal / shell, 
- navigate to this directory 
(i. e., `cd ~/WC_Sequence/` and 
- run 
`pip install -r requirements.txt` )


my new FR (firing rate?) sequence detector

__________________________
### Development notes: 
New branch: a_units_same_stim

the whole sensitivity to \delta f comes from B stimulus being attenuated- 
this only happens because we assume they are getting less inputs from B. 
Which means we're looking at neurons with a best frequency at A.

We will get ITI sensitivity by applying a gate on the inputs based on ITI, ie \cite{Wehr2005} figure 1a

Got the habituator to work! we're going to scale all the a1 inputs by a 
habituation function (it kicks in as soon as stim offsets... maybe it should be activity dependent but 
we can model that later, this equation is basically just the recover from adaptation for SFA I think)
It COULD also be the DECAY of an active sustained NMDA powered INHIBITION, that could explain a really fast 
onset and a slow decay for the ITI gating long lasting inhibitory current I think...

[us 1]
I could make an input A guy take all the inputs and NMDA-inhibit _itself_
now we have habituated inputs and a baby new network

[ us 2]
For everything interesting we want with feature selectivity, each unit has to have its own tuning curve.

[tests]

[us 4]
and we can write arbitrary feature-selective networks

[us 5]
with feature based synaptic footprints

[us 8]
where did all the NMDA go...? i _think_ the S is just sitting around,
waiting to be a source for someone else's current... but I don't know what NMDA current eq is
probably in xj wang somewhere NOPE he's all spiking
https://books.google.com/books?id=YkV5AgAAQBAJ&pg=PA458&lpg=PA458&dq=wilson+cowan+nmda+synaptic+dynamics&source=bl&ots=fiY4P7w4h3&sig=neYbFFeHFuz8mdvqZoaMkaeLgDo&hl=en&sa=X&sqi=2&ved=2ahUKEwiuicKC1oLeAhVQPK0KHfvRCcoQ6AEwBHoECAQQAQ#v=onepage&q=wilson%20cowan%20nmda%20synaptic%20dynamics&f=false
it's a current! eq. 15.90

[us 6]
stimuli superclass

[us 9]
can i describe "attractors" in this system...

[us 10]
eye candy... it would be fun to take xj's image of stimulus selective sustained activity (from working memory papers) 
and create something similar for auditory guys.
add noise?

[us 11]
perturbations... discrete events are a bad idea with uncertain tau (from ch 3, cumhist)
but _periodic_ perterbuations might be a swell deal, ie, if we could do 3/2 period or something like that
<in phase vs out of phase>


____
#### Completed
[us 3]
Which means stim should have an absolute reference, even if it's an index


been having trouble getting packages installed in my virtualenv...
workaround has been to install with pip from python console...
pip.main(['install','-flags', 'package'])
# NOPE! 
it comes down to this terminal being shit. just use git bash,
`source activate alternating_renewal_process`
and pip whatever you want and it'll show up in python console yay

branch 'modularizing':
Author: Sara Steele <sara.steele14@gmail.com>
Date:   Thu Mar 19 12:54:00 2015 -0400

    archived some code, going to start doing the test code for build-and-then (my disinhibitory object-oriented network)


commit fba42cd32d62edc86fa63ca1cdcc6f78b13011cc (HEAD -> with_inhibition, origin/with_inhibition)
Author: Sara Steele <sara.steele14@gmail.com>
Date:   Fri Feb 6 16:34:15 2015 -0500

    did that work?

commit 955e6ec5d4a3c35bbe950a3a6a629751937af837 (HEAD -> nullcline_analysis, origin/nullcline_analysis)
Author: Sara Steele <sara.steele14@gmail.com>
Date:   Mon Feb 9 20:42:14 2015 -0500

    starting the process of modularizing
