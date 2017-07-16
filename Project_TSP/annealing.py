import time
import random
import math
# These variables greatly affect the quality of the solution

# This could be replaced by time cutoff
restart_iterations = 4000

# Temperature function falls at a geometric rate of ar^n
geometric_a = 0.98
geometric_r = 0.75


def get_sol(tsp_instance, start_time, cutoff):
    trace_data = []

    best_quality = float("inf")
    best_tour = []

#    for r in range(0, restart_iterations):
    while float(time.time() - start_time) < float(cutoff):
        epsilon  = .001
        tour_order = range(0, len(tsp_instance))
        random.shuffle(tour_order)
        i = 0
        while(True):
            i += 1
            temperature = geometric_a * (geometric_r ** i)

            if (temperature < epsilon):
                break
        
            # Go to random neighbor state
            switch_index = random.randint(0, len(tsp_instance) - 2)
            new_tour_order = list(tour_order)
            switch_node = new_tour_order[switch_index]
            new_tour_order[switch_index] = new_tour_order[switch_index + 1]
            new_tour_order[switch_index + 1] = switch_node

            # Evaluate the quality of the tours
            tour_quality = 0
            new_tour_quality = 0
            for n in range(0, len(tsp_instance) - 1):
                tour_quality += tsp_instance[tour_order[n]][tour_order[n + 1]]
                new_tour_quality += tsp_instance[new_tour_order[n]][new_tour_order[n + 1]]

            tour_quality += tsp_instance[tour_order[len(tour_order) - 1]][tour_order[0]]
            new_tour_quality += tsp_instance[new_tour_order[len(new_tour_order) - 1]][new_tour_order[0]]

            if (new_tour_quality < best_quality):
                best_tour = new_tour_order
                best_quality = new_tour_quality
                trace_data.append([best_quality, int(time.time() - start_time)])

            probability = 0
            if (new_tour_quality < tour_quality):
                probability = 1
            else:
                # Simulated annealing function
                probability = math.e ** ((tour_quality - new_tour_quality) / temperature)

            if probability > random.random():
                tour_order = new_tour_order

    return [make_sol_data(tsp_instance, best_tour), trace_data]

def make_sol_data(tsp_instance, tour_order):
    quality = 0
    sol_data = []
    for n in range(0, len(tour_order) - 1):

        step_quality = tsp_instance[tour_order[n]] [tour_order[n + 1]]

        sol_data.append([tour_order[n], tour_order[n + 1], step_quality])
        quality += step_quality

    last_step = tsp_instance[tour_order[len(tour_order) - 1]][tour_order[0]]
    sol_data.append([tour_order[len(tour_order) - 1], tour_order[0], last_step])
    quality += last_step

    sol_data.insert(0, quality)
    return sol_data