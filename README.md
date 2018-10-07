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
