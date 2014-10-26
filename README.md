2D [Ising Model](http://en.wikipedia.org/wiki/Ising_model) Simulation
==============

Monte Carlo Simulation of Square-lattice Ising model using [Metropolis agorithm](http://en.wikipedia.org/wiki/Ising_model#The_Metropolis_Algorithm)

usage: 
```
python ising.py [-h] [-v] -s [SIZE [SIZE ...]] [-t T] [-i SWEEPS]

optional arguments:
  -h, --help            show this help message and exit
  -v, --visual          If flag is set, the simulation display each sweep
  -s [SIZE [SIZE ...]], --size [SIZE [SIZE ...]]
                        Set size of simulation ( 2 integers )
  -t T, --temp T        Sets temperature
  -i SWEEPS, --sweeps SWEEPS
                        No. of MC sweeps to perform ( Use if visualise flag is
                        not set )
```

eg:
```
python ising.py -s 30 30 -t 4 -v
```
