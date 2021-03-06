from pylab import *
import matplotlib.animation as animation
from argparse import ArgumentParser

def energy(l):
	return  -2*( (l[:,1:]*l[:,:-1]).sum() + (l[1:,:]*l[:-1,:]).sum() + (l[0,:]*l[-1,:]).sum() + (l[:,0]*l[:,-1]).sum() )

def random_lattice(shape):
	return random_integers(0, 1, shape)*2-1

def alt_lattice(shape):
	l = -ones(shape, dtype=integer)
	# l[::2,::2] = -1
	# l[1::2,1::2] = -1
	return l

def draw_lattice(lattice):
	imshow(lattice, cmap='Greys', interpolation='nearest')
	
nbrs = ones(4, dtype=int)
def random_location(l):
	loc = tuple([randint(0, n) for n in l.shape])
	neighbors = array([
		l[loc[0]+1 if loc[0]+1 < l.shape[0] else 0, loc[1]],
		l[loc[0], loc[1]+1 if loc[1]+1 < l.shape[1] else 0],
		l[loc[0]-1, loc[1]],
		l[loc[0], loc[1]-1]
	])

	return loc, neighbors

def correlation_function(l, l0):
	N = product(l.shape)
	return ( 1.*l*l0/N - (1.*l0/N)**2 ).sum()

Energy = []
correlation = []
magnetisation = []
iterations = 0

def sample_lattice(l):
	global iterations
	Energy.append(energy(l))
	magnetisation.append(l.sum())
	correlation.append(correlation_function(l, lattice0))
	iterations += 1

def update(*args):
	location, neighbors = random_location(lattice)

	# Flip a spin
	lattice[location] *= -1

	dE = -4*(lattice[location]*neighbors).sum()

	if dE > 0 and rand() >= exp(-dE/T):
		# flip it back
		lattice[location] *= -1

def sweep(*args):
	N = product(lattice.shape)
	for i in xrange(1, N):
		update()

	sample_lattice(lattice)

	if len(args) > 0:
		draw_lattice(lattice)

def parseCmdArgs():
	parser = ArgumentParser()
	
	parser.add_argument("-v", "--visual", 	action="store_true", dest="visualise", help="If flag is set, the simulation display each sweep")
	parser.add_argument("-s", "--size", nargs="*", action="store", required=True, dest="size", type=int, help="Set size of simulation ( 2 integers )")
	parser.add_argument("-t", "--temp", action="store", dest="T", default=5, type=float, help="Sets temperature")
	parser.add_argument("-i", "--sweeps", action="store", dest="sweeps", default=1000, type=int, help="No. of MC sweeps to perform ( Use if visualise flag is not set )")

	return parser.parse_args()

if __name__ == '__main__':

	args = parseCmdArgs()

	visualise = args.visualise
	sweeps = args.sweeps
	size = args.size
	T = args.T # Temperature

	V = product(size) # Volume

	# lattice = random_lattice(size)
	lattice = alt_lattice(size) # min. energy lattice
	lattice0 = lattice.copy()

	sample_lattice(lattice)

	if visualise:
		try:
			print "Close window to stop simmulation"
			fig = figure(1)
			anim = animation.FuncAnimation(fig, sweep, interval=5)
			show()
		except:
			pass
	else:
		while iterations < sweeps:
			sweep()

	index = find(abs(array(correlation)) < 0.01)
	index = index[0] if len(index) > 0 else 0
	print "Energy per unit volume = %f"%(average(Energy[index:])/V)
	print "Specific heat capacity = %f"%(var(Energy[index:])/V)
	print "Magnetisation          = %f"%(average(magnetisation[index:])/V)

	# plot(magnetisation[index:], '-')
	plot(Energy[index:], '-')
	show()
