# Team P (Tanmay Rajpurohit, Yuyu Zhang, Kevin R Low, Jack O Mueller)

# Please execute the following command lines, with configurable arguments
# The output files will be in the "output" folder, please do NOT delete the "output" folder

cd code

# Branch and Bound
python RunTSP.py -inst ../data/Atlanta.tsp -alg BnB -time 100 -seed 1

# MST Approximation
python RunTSP.py -inst ../data/Atlanta.tsp -alg MSTApprox -time 100 -seed 1

# Heuristic: Nearest Neighbor Approximation
python RunTSP.py -inst ../data/Atlanta.tsp -alg Heur -time 100 -seed 1

# Local Search: 2-opt exchange hill climbing)
python RunTSP.py -inst ../data/Atlanta.tsp -alg LS1 -time 100 -seed 1

# Local Search: 2-opt exchange simulated annealing)
python RunTSP.py -inst ../data/Atlanta.tsp -alg LS2 -time 100 -seed 1
