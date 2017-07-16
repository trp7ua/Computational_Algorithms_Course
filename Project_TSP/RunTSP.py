#!/usr/bin/python
# CSE6140 TSP Project
# Authors: Jack Mueller, Tanmay Rajpurohit, Yuyu Zhang, Kevin Low 

import time
import sys
import random
import os
import math
import mst_approx
import annealing
import bnb
import nearest_neighbor
import two_opt


def main():
    num_args = len(sys.argv)

    if num_args < 9 or num_args > 9:
        print "error: wrong input arguments\n" + \
              "-inst <filename> -alg [BnB|MSTApprox|Heur|LS1|LS2] -time <cutoff> -seed <seed>"
        exit(1)

    input_file = sys.argv[2]
    algorithm = sys.argv[4]
    cutoff = sys.argv[6]
    seed = sys.argv[8]

    # Set random seed
    random.seed(seed)

    # Read TSP instance input
    tsp_instance = read_file(input_file)

    # Create the filename
    out_file = os.path.basename(os.path.splitext(input_file)[0])
    if algorithm == "LS1" or algorithm == "LS2":
        output_filename = out_file + "_" + algorithm + "_" + cutoff + "_" + seed
    else:
        output_filename = out_file + "_" + algorithm + "_" + cutoff

    # Start the timer
    global start_time
    start_time = time.time()

    # Select algorithm
    if algorithm == "BnB":
        output_data = BnB(tsp_instance, cutoff)
    elif algorithm == "MSTApprox":
        output_data = MSTApprox(tsp_instance)
    elif algorithm == "Heur":
        output_data = Heur(tsp_instance)
    elif algorithm == "LS1":
        output_data = LS1(tsp_instance, cutoff)
    elif algorithm == "LS2":
        output_data = LS2(tsp_instance, cutoff)
    else:
        print "error: -inst argument should be BnB|MSTApprox|Huer|LS1|LS2"
        exit()
    total_time = time.time() - start_time

    sol_data = output_data[0]
    with open("../output/" + output_filename + ".sol", 'w') as sol_file:

        # Write the quality of the best solution
        sol_file.write(str(sol_data[0]) + "\n")
        for line in sol_data[1:]:
            # Write u v c(u,v) for each edge in the tour
            line = map(str, line)
            sol_file.write(" ".join(line) + '\n')

    trace_data = output_data[1]
    with open("../output/" + output_filename + ".trace", 'w') as trace_file:
        for line in trace_data:
            # Write time [partial solution quality]
            trace_file.write('{:.2f},{:d}\n'.format(line[0], line[1]))


# The number in sol_data in the template is just there to make writing output work. This number
# should eventually be the quality of the solution found
def BnB(tsp_instance, cutoff):
    sol_data, trace_data = bnb.getSolBnB(tsp_instance, cutoff)

    return [sol_data, trace_data]


def MSTApprox(tsp_instance):
    sol_data = mst_approx.getSol(tsp_instance)
    time_cost = time.time() - start_time
    trace_data = [[time_cost, sol_data[0]]]

    return [sol_data, trace_data]


def Heur(tsp_instance):
    sol_data = nearest_neighbor.getSol(tsp_instance)
    time_cost = time.time() - start_time
    trace_data = [[time_cost, sol_data[0]]]

    return [sol_data, trace_data]


def LS1(tsp_instance, cutoff):
    return two_opt.get_sol(tsp_instance, start_time, cutoff)


def LS2(tsp_instance, cutoff):
    return annealing.get_sol(tsp_instance, start_time, cutoff)


# Returns tsp problem instance as an adjacency matrix
def read_file(input_file):
    with open(input_file, 'r') as f:
        f.readline()  # NAME
        f.readline()  # COMMENT
        f.readline()  # DIMENSION
        f.readline()  # EDGE_WEIGHT_TYPE
        f.readline()  # NODE_COORD_SECTION
        node_data = []
        for line in f:
            line_data = line.split(" ")
            if len(line_data) == 3:
                line_data[0] = int(line_data[0])
                line_data[1] = float(line_data[1])
                line_data[2] = float(line_data[2])
                node_data.append(line_data)
            else:
                pass  # EOF

    # 2 dimensional array with EUC_2D value entries
    tsp_instance = [[0 for x in range(len(node_data))] for y in range(len(node_data))]

    for i in xrange(0, len(node_data)):
        for j in xrange(0, len(node_data)):
            # Euclidean distance formula
            A = (node_data[i][1] - node_data[j][1]) ** 2
            B = (node_data[i][2] - node_data[j][2]) ** 2
            tsp_instance[i][j] = int(math.sqrt(A + B) + 0.5)
    return tsp_instance


if __name__ == '__main__':
    # run the algorithm on the given instance and write results to file
    main()
