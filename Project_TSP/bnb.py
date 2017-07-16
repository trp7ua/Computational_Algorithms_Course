"""."""

import numpy as np
import time
import heapq as hp

def getSolBnB(tsp_instance,cutoff=2000):
	
	start_time=time.time()
	final_time=start_time+int(cutoff)

	CostMat= np.array(tsp_instance,np.float)

	CostMat[CostMat==0]=float('inf')

	N=len(tsp_instance)

	UB=float('inf')

	trace_data = []

	pq=[]
	
	for i in range(1,N):
		tmpMat=np.delete(CostMat[1:],i,1)
		tmpCost=tsp_instance[0][i]+tmpMat.min(axis=1).sum()\
		    +(tmpMat-tmpMat.min(axis=1,keepdims=True)).min(axis=0).sum()
		hp.heappush(pq,(N-2,tmpCost,[0,i]))
	
	while len(pq) != 0:
		if time.time()>final_time:
			break

		node=hp.heappop(pq)
		cost=node[1]
		sol=node[2]
	
		if cost<UB:
			if len(sol)< N:

					nodesleft=[x for x in range(N) if x not in sol]

					for d in nodesleft :
						solnew= sol+[d]

						costPartial=sum([CostMat[solnew[i],solnew[i+1]] for i in range(len(sol))])

						reduceMat = np.delete(np.delete(CostMat,solnew[1:],1),solnew[:-1],0)

						reduceCost=reduceMat.min(axis=1).sum()+(reduceMat\
							-reduceMat.min(axis=1,keepdims=True)).min(axis=0).sum()

						costnew=costPartial+reduceCost

						hp.heappush(pq,(N-len(solnew),costnew,solnew))

			else:
				UB=cost
				CurrentSol=sol
				trace_data.append([time.time()-start_time,int(UB)])

	if np.isinf(UB):
		UB=sum([tsp_instance[i%N][(i+1)%N] for i in range(N+1)])
		sol_data=[UB]+list([i%N,(i+1)%N,\
			tsp_instance[i%N][(i+1)%N]] for i in range(N+1))
		trace_data.append([time.time()-start_time,UB])

	else:
		CurrentSol.append(CurrentSol[0])
		sol_data=[int(UB)]+list([CurrentSol[i],CurrentSol[i+1],\
			tsp_instance[CurrentSol[i]][CurrentSol[i+1]]] for i in range(N))

	return [sol_data, trace_data]

if __name__ == "__main__":
	getSolBnB()
