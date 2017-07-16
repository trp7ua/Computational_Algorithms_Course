import time
import random

def get_sol(tsp_instance, start_time, cutoff_time):
    
    #create and/or initialize variables to use in program    
    NUM_STOPS = len(tsp_instance) #constant to make program more readible
    trace = []
    bestPath = []
    bestQuality = float('inf')
    k = 0
    myStartTime = time.time()
    
    #loop through until time runs out (also in next loop just in case)
    while time.time() - myStartTime < float(cutoff_time):
        #create new path for this iteration
        currentPath = range(0, NUM_STOPS)
        random.shuffle(currentPath)
        solutionChanged = 1
        
        #find stating quality
        currentQuality = 0
        for i in range(0,NUM_STOPS-1):
            nextEdgeCost = tsp_instance[currentPath[i]][currentPath[i+1]]
            currentQuality += nextEdgeCost
        currentQuality += tsp_instance[currentPath[NUM_STOPS-1]][currentPath[0]]
    
        #add starting quality to trace the first time (assume all future
        #iterations will have starting quality worse than one found prev it.s)
        if k == 0:
            trace.append([time.time() - start_time, currentQuality])
        
        #outermost loop keeps going until the solution is not changed
        while solutionChanged == 1 and time.time() - myStartTime < float(cutoff_time):
            #reset flag
            solutionChanged = 0
            
            #middle loop picks a starting edge to exchange with another edge
            for i in range(0,NUM_STOPS):
                #variables to hold current best values for internal loop
                bestFlipVal = 0
                bestFlipLoc = -1
                
                #innermost loop goes through all other edges looking for best one
                #to flip the starting edge with
                for j in range(0,NUM_STOPS):
                    if i == j:
                        continue
                    
                    #find sum of two edges before and after flip                
                    oldEdgesVals = tsp_instance[currentPath[i]][currentPath[(i+1)%NUM_STOPS]] + \
                        tsp_instance[currentPath[j]][currentPath[(j+1)%NUM_STOPS]]
                    newEdgesVals = tsp_instance[currentPath[i]][currentPath[j]] + \
                        tsp_instance[currentPath[(i+1)%NUM_STOPS]][currentPath[(j+1)%NUM_STOPS]]
                    
                    #calculate if this is an improvement and if it's the best seen
                    #so far
                    improvement = oldEdgesVals - newEdgesVals
                    if improvement > bestFlipVal:
                        bestFlipVal = improvement
                        bestFlipLoc = j
                
                #check to make sure an edge was fliped
                if bestFlipLoc == -1:
                    continue
                else:
                    solutionChanged = 1
                    
                #rearrange the running answer matrix to flip edges
                if i < j:
                    currentPath[i+1:bestFlipLoc+1:1] = currentPath[bestFlipLoc:i:-1]
                else:
                    section1 = currentPath[:bestFlipLoc+1]
                    section2 = currentPath[i+1:]
                    toFlip = section2 + section1
                    toFlip.reverse()
                    currentPath[:bestFlipLoc+1] = toFlip[len(toFlip)-bestFlipLoc-1:]
                    currentPath[i+1:] = toFlip[:len(toFlip)-bestFlipLoc-1]
                        
                #update the quality and/or trace
                currentQuality = findLength(tsp_instance,currentPath)
                if currentQuality < bestQuality:
                    bestQuality = currentQuality
                    bestPath = currentPath
                    trace.append([time.time() - start_time, currentQuality])
        k += 1
    
    #make the solution data
    sol_data = []
    sol_data.append(bestQuality)
    for i in range(NUM_STOPS-1):
        toAdd = [bestPath[i], bestPath[i+1], tsp_instance[bestPath[i]][bestPath[i+1]]]
        sol_data.append(toAdd)
    toAdd = [bestPath[NUM_STOPS-1], bestPath[0],tsp_instance[bestPath[NUM_STOPS-1]][bestPath[0]]]
    sol_data.append(toAdd)
    
    #add total time taken to the trace array
    #trace.insert(0,time.time() - start_time)
    
    #return both
    return [sol_data, trace]

def findLength(tsp_instance,path):
    NUM_STOPS = len(tsp_instance)
    length = 0
    for i in range(0,NUM_STOPS-1):
        nextEdgeCost = tsp_instance[path[i]][path[i+1]]
        length += nextEdgeCost
    length += tsp_instance[path[NUM_STOPS-1]][path[0]]
    return length
                
#for debugging
#if __name__ == '__main__':
#    # run the algorithm on the given instance
#    r1 = [0, 7, 91, 17, 23]    
#    r2 = [7, 0, 41, 3, 19]
#    r3 = [91, 41, 0, 11, 37]
#    r4 = [17, 3, 11, 0, 42]
#    r5 = [23, 19, 37, 42, 0]
#    testArray = [r1, r2, r3, r4, r5]
#    get_sol(testArray)
