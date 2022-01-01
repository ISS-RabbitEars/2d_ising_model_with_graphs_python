1. the parameters which control the simulation can be found 
here (lines 108-116):
#-----PARAMETERS----------------------------
nx=50
ny=50
J=1
kb=1
mo=1
Ti=1
Tf=1
Bi=2
Bm=-2

nx and ny are the dimensions of the system in terms of spin sites.
J is the value for the interaction energy
kb is the Boltzmann Constant (scaled)
mo is the coupling parameter wrt external field interaction
Ti is the initial temperature of the system
Tf is the final temperature of the system
Bi is the initial and final value for the external magentic field (+)
Bm is the midpoint value for the magentic field (-)

*neither Ti nor Tf should be set to zero. they may be set to the same value.

2. if B is constant (Bi=Bm):
	the simulations will produce 3 graphs
	. the model itelf
	. a plot of the system temperature and the external magntic field values wrt time
	. a plot of the specific magnetization and specific internal energy of the system
3. if B is ranged:
	the system will produce 4 graphs
	. the 3 mentioned above, plus
	. a hysteresis loop plot

  
