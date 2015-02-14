import unittest
from WC_class import WC_unit

tUnit=WC_unit()
defaultPars=tUnit.__dict__

class WC_assign_tests(unittest.TestCase):

# can user change pars?
	def testWC_userPars(self):  
		tUnit=WC_unit(Iapp=0,the=.5)
		assignedPars=tUnit.__dict__

		self.failIf(assignedPars==defaultPars)

# are the default pars intact?
	def testWC_defaultpars2(self):	
		tUnit=WC_unit(Iapp=0,the=.5)
		tUnit2=WC_unit()
		assignedPars=tUnit2.__dict__
		self.failUnless(assignedPars==defaultPars)

# does assigning with a dictionary work?
	def testWC_dictPars(self):
		dictPars=dict(Iapp=.5,the=.5,ie=.2)
		updatedPars=defaultPars
		updatedPars.update(dictPars)

		tUnit=WC_unit(**dictPars)
		assignedPars=tUnit.__dict__
		
		self.failUnless(assignedPars==updatedPars)


# my first stab at writing a test before a function
class compute_dRtests(unittest.TestCase):
	def testdR(self):
		# I want there to be a function that computes dR for 
		pass

#	def testWC_update(self):
#class WC_integrate_tests(unittest.TestCase):	

#def main():
#	unittest.main()

if __name__=="__main__":
	unittest.main()

