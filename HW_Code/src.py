"""."""

import matplotlib.pyplot as plt
import numpy as np
import math
import time
import sys
import os

def main():

        filenames = next(os.walk('./data'))[2] # reads the files from './data' directory
        dc_runtime=[]
        dp_runtime=[]

        for input_file in filenames:
            print input_file

#  Divide and Conquer
            output_file = './output/trajpurohit3_output_dc_'+input_file  #the name and path to store output
            data=np.loadtxt('./data/'+input_file,delimiter=',',skiprows=1)
            output=[]
            for i in range(len(data)):
                start_time=time.time()
                res=divide_and_conquer(data[i],1,len(data[i])) # Call the function that implements the  divide-and-conquer algorithm
                res.append(round((time.time()-start_time)*1000,2)) # Add the computation time in the end
                output.append(res) #append the result
            dc_runtime.append([int(open('./data/'+input_file).readline().split(',')[0]),np.array(output)[:,-1].mean()]) # create list of input_size and average running time

        # Storing the output file
            of = open(output_file, 'w')
            for l in output:
                of.write(str(l)[1:-1]+"\n")

# Dynamic Programming
            output_file = './output/trajpurohit3_output_dp_'+input_file
            data=np.loadtxt('./data/'+input_file,delimiter=',',skiprows=1)
            output=[]
            for i in range(len(data)):
                start_time=time.time()
                res=dynamic_programming(data[i]) # Call the function that implements the  dynamic programming algorithm
                res.append(round((time.time()-start_time)*1000,2))# Add the computation time in the end
                output.append(res)  #append the result
            dp_runtime.append([int(open('./data/'+input_file).readline().split(',')[0]),np.array(output)[:,-1].mean()])

        # Storing the output file
            of = open(output_file, 'w')
            for l in output:
                of.write(str(l)[1:-1]+"\n")

# Plot result and save fig
        dcRun=np.array(dc_runtime)
        dcRun=dcRun[dcRun[:,0].argsort()]
        dpRun=np.array(dp_runtime)
        dpRun=dpRun[dpRun[:,0].argsort()]
        plt.plot(dcRun[:,0],dcRun[:,1],'bo-',label='Divide-and-Conquer')
        plt.plot(dpRun[:,0],dpRun[:,1],'ro-',label='Dynamic Programming')
        plt.xlabel('Input size (n)')
        plt.ylabel('Run Time')
        plt.legend(loc='upper left')
        plt.savefig('runtime')  #Save the plot
        plt.show()    #Show the plot


'''This Function implements the divide-and-conquer algorithm'''

def divide_and_conquer(days,idxI,idxJ):

    n= idxJ-idxI
    if n==0:
        return [max(0,round(days[idxI-1],2)),idxI,idxI] # retun the terminal recursion
    else:
        m=idxI+(n/2)

        crossValArrayL=np.array(list(days[i:m].sum() for i in range(idxI-1,m))) #Compute the Left half sum
        crossValArrayR=np.array(list(days[m:j+1].sum() for j in range(m,idxJ))) #Compute the right half sum

        startCross=crossValArrayL.argmax()+idxI #Start index for corss interval
        endCross=crossValArrayR.argmax()+m+1    #End index for cross interval
        CrossVal=crossValArrayL.max()+crossValArrayR.max() #Max value for crossing midpoint
        left=divide_and_conquer(days,idxI,m)     #Recursive call
        right=divide_and_conquer(days,m+1,idxJ)  #Recursive call

#Compare the max interest sum and return the output

        if CrossVal>max(left[0],right[0]):
            return [round(CrossVal,2),startCross,endCross]
        elif left[0]>right[0]:
            return left
        else:
            return right


'''This Function implements the dynamic programming algorithm'''

def dynamic_programming(days):

    B=[0] #initialize

#Compute the list B[j] using bottom-up approach
    for i in range(len(days)):
        B.append(max(0,B[i]+days[i]))

# Find the max value as well as its index
    maxVal= max(B)
    idxJ = B.index(max(B))

#Travese the list backward to find out the start day
    tmpVal=0
    idxI=idxJ
    while tmpVal+0.00001<maxVal:
        tmpVal=tmpVal+days[idxI-1]
        idxI=idxI-1

#Return the output
    return [round(maxVal,2),idxI+1,idxJ]


if __name__ == "__main__":
    main()
