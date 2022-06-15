from operator import le
from unicodedata import name
from numpy import conjugate
from ortools.linear_solver import pywraplp
from ortools.linear_solver import pywraplp
from datetime import datetime
import random
import pandas as pd

# 20 customer -> 1.1 minute
# 30 customers -> 5 minute    1.69 minutes
# 40                          2.45 min
# 50 customer -> 160 minute


df= pd.read_csv("data_fin.csv")

def discreteTime(timeWindow,intervalSize):   # O(lenghtOftimeWindow/size)
    tw = [] 
    currtime = timeWindow[0]
    endtim=timeWindow[1]
    currtime=currtime-(currtime%10)
    endtim=endtim-(endtim%10)
    while ( currtime <= endtim ): 
        tw.append(currtime)
        currtime=currtime+intervalSize
    return tw
def getNodesandCustomer(nodeCount,variables,x,edges,discreteTimeWindows,vehicleReq,timeWindows):
    goodVariables =[]
    visited = []
    goodEdges = []

    for j in range(variables):
            if(x[j].solution_value() > 0 and j<len(edges)):
                goodVariables.append(j)

    print("good var:",goodVariables)
    print()            

    for i in range(0,len(goodVariables)):
        visited.append(0)
        goodEdges.append(edges['x[%i]' % goodVariables[i]])

    print("good edges :",goodEdges)
    print (timeWindows)
    for i in range(0,vehicleReq):
        nextFirstNode = 0
        flag = 0
        NodesInPath = []
        while(nextFirstNode != -1):
            for j in range(0,len(goodEdges)):
                if(visited[j] == 0 and flag == 0):
                    nextFirstNode = goodEdges[j][-1]
                    NodesInPath.append(goodEdges[j][0])
                    visited[j] = 1
                    flag = 1
                elif(nextFirstNode == -1):
                    NodesInPath.append(-1)
                    break
                elif(visited[j] == 0 and goodEdges[j][0] == nextFirstNode):
                    nextFirstNode = goodEdges[j][-1]
                    NodesInPath.append(goodEdges[j][0])
                    visited[j] = 1

        print("path ",i," ",NodesInPath)   
        for j in range(1,len(NodesInPath)):
            currNode = NodesInPath[j]
            if(currNode != -1):
                for k in range(0,len(nodeCount)):
                    if(currNode in nodeCount[k]):
                        time = discreteTimeWindows[k][nodeCount[k].index(currNode)]
                        print("Customer :",(k+1)," Time :",time ,"     valid time window",timeWindows[k])
                        break

        print()






    
    # for i in range(0,vehicleReq):
    #     path = []
    #     prev = -2
    #     for j in range(0,len(goodVariables)):
    #         if(visited[j]==0 and prev == -2):
    #             prev = edges['x[%i]' % goodVariables[j]][1]
    #             visited[j] = 1
    #             path.append(edges['x[%i]' % goodVariables[j]][0])
    #         if(visited[j]==0 and edges['x[%i]' % goodVariables[j]][0] == prev):
    #             visited[j] = 1
    #             prev = edges['x[%i]' % goodVariables[j]][1]
    #             path.append(edges[ 'x[%i]' % goodVariables[j]][0])
    #         if(prev== -1):
    #             path.append(-1)
    #             break
    #     cust = []
    #     time = []
    #     for i in range(1,len(path)-1):
    #         for j in range(0,len(nodeCount)):
    #             for k in range(0,len(nodeCount[j])):
    #                 if(path[i] == nodeCount[j][k]):
    #                     cust.append(j)
    #                     time.append(discreteTimeWindows[j][k])
    #                     break
                    
    #     for i in range(0,len(cust)):
    #         print("Customer:",cust[i]," Time:",time[i])

    #     print(path)

    
            
            
                 
               

    return 0
def main():
    customers = 10

    timeWindows = [] 
    for i in range(0,customers):
        st = df['st'][i+1]
        et = df['et'][i+1]
        tw = [st,et]
        timeWindows.append(tw)

    print("time Windows ",timeWindows)
    print()

    discreteTimeWindows = []
    for i in timeWindows:
        discreteTimeWindows.append(discreteTime(i,10))
    
    print("discreteTimeWindows",discreteTimeWindows)
    print()
    

    timeMatrix = []
    for i in range(1,customers+1):
        timeMatrix.append([0]*customers)
    for i in range(0,customers):
        for j in range(1,customers+1):
            if(i==j):
                timeMatrix[i-1][j-1] = 0
            elif (i<j):
                c= abs(df['x'][i]-df['x'][j])+abs(df['y'][i]-df['y'][j])
                timeMatrix[i-1][j-1] =c-(c%10)
                timeMatrix[j-1][i-1] = timeMatrix[i-1][j-1]

    print("timeMatrix",timeMatrix)
    print(len(timeMatrix))

    count = 0
    nodeCount =[]  # assigns a number to node using count and stores its value
    
    for i in range(0,len(discreteTimeWindows)):
        c = []
        for j in range(0,len(discreteTimeWindows[i])):
            c.append(count+1)
            count+=1
        nodeCount.append(c)

    # print("Node Count b4 s",nodeCount)
    # print()

    with open('timeNodes.txt','w') as f:
        f.write("Time \n")
        f.write(str(timeMatrix))
        f.write("\n Nodes \n")
        f.write(str(nodeCount))

    
    edgeFlows = {}
    edgeNumber = 0
    x = {}
    edges = {}
    edgesList = [] # stores edge number going out of ith node
    edgesList.append([]) # for s
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # out of s
    e =[]
    for i in range(0,len(nodeCount)):
        # for j in range(0,len(nodeCount[i])):
            e.append(edgeNumber)
            x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
            edges['x[%i]' % edgeNumber] = (0,nodeCount[i][0])
            edgeFlows[edgeNumber] = (0,nodeCount[i][0])
            edgeNumber+=1
    edgesList[0]=e
    # joining the edges of each customer
    for i in range(0, len(nodeCount)):
        for j in range(0, len(nodeCount[i])-1):
            e = []
            x[edgeNumber] = solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
            edges['x[%i]' % edgeNumber] = (nodeCount[i][j], nodeCount[i][j+1])
            edgeFlows[edgeNumber] = (nodeCount[i][j], nodeCount[i][j+1])
            # add edge number in edge list
            e.append(edgeNumber)
            edgesList.append(e)
            edgeNumber += 1
        edgesList.append([])
    print("Edges List:", edgesList)

                      
                
    # print("edgelist")
    # for i in range(0,len(discreteTimeWindows)):
    #     print(len(discreteTimeWindows[i]))
    #     for j in range(0,len(discreteTimeWindows[i])-1):    # j th node
    #         u = nodeCount[i][j]
    #         print(u)
    #         utime = discreteTimeWindows[i][j]
    #         e = []  # stores edges reachable from u
    #         x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
    #         edges['x[%i]' % edgeNumber] = (u,nodeCount[i][j+1]) # u -> v reachable
    #         edgeFlows[edgeNumber] = (u,nodeCount[i][j+1])
    #         e.append(edgeNumber)
    #         edgeNumber += 1
    #         # edgesList[u]=e
    #         edgesList.append(e)
    #     print()
    #     e = [] 
    #     # edgesList[nodeCount[i][len(discreteTimeWindows[i])-1]]=e
    #     edgesList.append(e)
    # print(len(edgesList))
    # print("edgeslist[15]",edgesList[15])
    # count=0;
    count=0;
    for i in range(0,len(discreteTimeWindows)):
        # for j in range(0,len(discreteTimeWindows[i])): 
            for k in range(0,len(discreteTimeWindows)):
                # for l in range(len(discreteTimeWindows[k])-1,-1,-1): # l th node
                #     v = nodeCount[k][l]
                #     vtime = discreteTimeWindows[k][l]
                    # print(utime,vtime)
                    # # print('time from',u,'to',v,'is',timeMatrix[i][k])
                    # print()
                
                
                        
                if (i!=k and discreteTimeWindows[i][-1]+timeMatrix[i][k]<discreteTimeWindows[k][0]):
                        print("1")
                        e=[]
                        u = nodeCount[i][-1]
                        v=nodeCount[k][0]
                        x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
                        edges['x[%i]' % edgeNumber] = (u,v) # u -> v reachable
                        edgeFlows[edgeNumber] = (u,v)
                        e.append(edgeNumber)
                        # edgesList[int(count+len(discreteTimeWindows[i]))].append(edgeNumber)
                        edgesList[u].extend(e)
                        edgeNumber += 1
                elif(i!=k and discreteTimeWindows[i][-1]+timeMatrix[i][k]==discreteTimeWindows[k][0]):
                        print("2")
                        e=[]
                        u = nodeCount[i][-1]
                        v=nodeCount[k][0]
                        x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
                        edges['x[%i]' % edgeNumber] = (u,v) # u -> v reachable
                        edgeFlows[edgeNumber] = (u,v)
                        e.append(edgeNumber)
                        # edgesList[int(count+len(discreteTimeWindows[i]))].append(edgeNumber)
                        edgesList[u].extend(e)
                        edgeNumber += 1
                elif(i!=k and (discreteTimeWindows[k][0]-timeMatrix[i][k])<=discreteTimeWindows[i][len(discreteTimeWindows[i])-1] and (discreteTimeWindows[k][0]-timeMatrix[i][k])>=discreteTimeWindows[i][0] ):
               [nodeCount[i][l]].extend(e)
               
                        intime= (discreteTimeWindows[k][0]-timeMatrix[i][k])
                        # print(intime)
                        # print(intime-discreteTimeWindows[i][0])
                        
                        n=0
                        
                        # print("time window (i) :", discreteTimeWindows[i])
                        # print("time window (j):", discreteTimeWindows[k])
                        for m in range(int((intime-discreteTimeWindows[i][0])/10),len(discreteTimeWindows[i])):
                            if(n<len(discreteTimeWindows[k])-1):
                                # print("m:",m)
                                # print(n)
                                e=[]
                                u = nodeCount[i][m]
                                # u = nodeCount[i][int(intime-discreteTimeWindows[i][0])]
                                v=nodeCount[k][n]
                                x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
                                edges['x[%i]' % edgeNumber] = (u,v) # u -> v reachable
                                edgeFlows[edgeNumber] = (u,v)
                                # print(count+intime-discreteTimeWindows[i][0])
                                # edgesList[int(count+intime-discreteTimeWindows[i][0])].append(edgeNumber)
                                e.append(edgeNumber)
                                edgesList[u].extend(e)
                                # edgesList[int(count+m)].append(edgeNumber)
                                edgeNumber += 1
                                n=n+1
                                print(e)
            count=count+len(discreteTimeWindows[i])
       
    
    
    # print('edge list b4 s t',edgesList)
    print()
    
    # into t (except s)
    e=[]
    for i in range(0,len(nodeCount)):
        # for j in range(0,len(nodeCount[i])):
            x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
            edges['x[%i]' % edgeNumber] = (nodeCount[i][-1],-1)
            edgeFlows[edgeNumber] = (nodeCount[i][-1],-1)
            #add edge number in edge list 
            edgesList[nodeCount[i][-1]].append(edgeNumber)
            edgeNumber+=1
    edgesList.append([])
    # print("Node Count after s and t:",nodeCount)
    print()
    

    offse = edgeNumber   # if I add it to  0 edge i'll get flow for 1 at the same edge  , add to 1 customer 2 customer 
    # print("edge flows:",edgeFlows[0])
    print(len(edgeFlows))
    print(edgeNumber)
    print(len(edgesList))
    flows = [0]*customers
    for i in range(customers):
        flows[i] = edgeFlows.copy()
        keys = edgeFlows.keys()
        # print(keys)
        for j in keys: # stores key values of edgeflows i.e 0 1 2
            x[edgeNumber] = solver.NumVar(0,1,'x[%i]' % edgeNumber) # making variable
            # remove key and replace it by edge
            t = flows[i].pop(j)
            # print(t)
            # flows[i][j] = t
            flows[i][edgeNumber] = t 
            edgeNumber+=1
    # print(flows[0][0])
    
    # print("flows",flows[0][0])    
    print('Number of variables =', solver.NumVariables())
    print(edgeNumber)
    with open('edgeList.txt','w') as f:
        f.write("Edge List \n")
        f.write(str(edgesList))
    with open('edges.txt','w') as f:
        f.write("Edges \n")
        f.write(str(edges))       

    print('edge list',edgesList)
    print()
    print("edges",edges)
    print()
    print('edge number',edgeNumber)
    print()

    data = {}

 
    data['constraint_coeffs'] = []
    data['bounds'] = [] # inclusive

    # contraint for outgoing flow for a customer
   
    for i in range(0,len(nodeCount)): # choose one list from nodeCount
        contraint = [0] * (edgeNumber)
        for j in range(0,len(nodeCount[i])-1): # se
            node = nodeCount[i][j]
            for k in range(1,len(edgesList[node])):
                e = edgesList[node][k]
                contraint[e] = 1
        node=nodeCount[i][len(nodeCount[i])-1]
        for k in range(0,len(edgesList[node])):
            e = edgesList[node][k]
            contraint[e] = 1
       
                
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1u')
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1l')

    # print(data['constraint_coeffs'])
    # print(data['bounds'])   

    # constraint for incoming for a customer
    incomingEdgeList =[]
    for i in range(0,len(edgesList)):
        incomingEdgeList.append([]) # adding lists in a list
    for i in edges:
        v = edges[i][1]  # u -> v

        edge_no = int(i[2:-1])
        incomingEdgeList[v].append(edge_no)

    print("incoming edge list: ",incomingEdgeList)
    # print()

    for i in range(0,len(nodeCount)):
        contraint = [0] * (edgeNumber) # indicates number of edges
        for j in range(1,len(nodeCount[i])):
            node = nodeCount[i][j]
            
            for k in range(1,len(incomingEdgeList[node])):
                # print(k)
                e = incomingEdgeList[node][k]
                contraint[e] = 1
        node=nodeCount[i][0]
        for k in range(0,len(incomingEdgeList[node])):
            e = incomingEdgeList[node][k]
            contraint[e] = 1
            
                
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1u')
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1l')

    # print(data['constraint_coeffs'])
    # print(data['bounds'])   

    # # constraint for a node incoming = outgoing
    for i in range(0,len(nodeCount)):
        for j in range(0,len(nodeCount[i])):
            contraint = [0] * (edgeNumber)
            node = nodeCount[i][j]
            for k in range(0,len(incomingEdgeList[node])):
                e = incomingEdgeList[node][k]
                contraint[e] = 1
            for k in range(0,len(edgesList[node])):
                e = edgesList[node][k]
                contraint[e] = -1
            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('0u')
                

    # # # print(data['constraint_coeffs'])
    # # # print(data['bounds']) 

    # # # constraints for incoming = 1

    # # print("offset",offset)
    # # # print("flows",flows)
    
    # # #  0<= xij - fij <= 1    
    for j in range(len(flows)):
            diff = offse*j+offse
            print(flows[j].keys())
            for k in flows[j].keys():
                contraint = [0]*edgeNumber
                # contraint[(j+1)*k] = -1
                # contraint[k] = 1
                contraint[k] = -1
                contraint[k-diff] = 1
                data['constraint_coeffs'].append(contraint)
                data['bounds'].append('1u')
                # data['constraint_coeffs'].append(contraint)
                # data['bounds'].append('0l')
    
    # # # constraint for incoming flow for a particular customer = 1 
    for customer in range(customers):
        addn = offse*customer+offse
        for i in range(0,len(nodeCount)):
            contraint = [0] * (edgeNumber) # indicates number of edges
            
         # indicates number of edges
            for j in range(1,len(nodeCount[i])):
                node = nodeCount[i][j]
                for k in range(1,len(incomingEdgeList[node])):
                
                    e = incomingEdgeList[node][k]
                    contraint[e+addn] = 1
            node=nodeCount[i][0]
            for k in range(0,len(incomingEdgeList[node])):
                e = incomingEdgeList[node][k]
                contraint[e+addn] = 1 

    
            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('1u')
            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('1l')


    # # flow conservation for node
    for c in range(customers):
        addn = offse*c+offse
        for i in range(0,len(nodeCount)):
            for j in range(0,len(nodeCount[i])):
                contraint = [0] * (edgeNumber)
                node = nodeCount[i][j]
                for k in range(0,len(incomingEdgeList[node])):
                    e = incomingEdgeList[node][k]
                    contraint[e+addn] = 1
                for k in range(0,len(edgesList[node])):
                    e = edgesList[node][k]
                    contraint[e+addn] = -1
                data['constraint_coeffs'].append(contraint)
                data['bounds'].append('0u')


    # objective function minimize outgoing flow from 0 node
    objectiveCoefficients = [0] * (edgeNumber)
    for i in range(0,len(edgesList[0])):
        objectiveCoefficients[edgesList[0][i]]=1
    data['obj_coeffs'] = objectiveCoefficients

    # print(objectiveCoefficients)

   
    data['num_vars'] = edgeNumber
    data['num_constraints'] = len(data['constraint_coeffs'])

    for i in range(data['num_constraints']):
        if(data['bounds'][i][-1]=='u'):
            constraint = solver.RowConstraint(0, int(data['bounds'][i][:-1]), '')
        else:
            constraint = solver.RowConstraint(int(data['bounds'][i][:-1]),solver.infinity(), '')
        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
    print('Number of constraints =', solver.NumConstraints())
   

    objective = solver.Objective()
    for j in range(data['num_vars']):
        objective.SetCoefficient(x[j], data['obj_coeffs'][j])
    objective.SetMinimization()
   
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        print("data ",data['num_vars'])
        for j in range(data['num_vars']):
            print(x[j].name(), ' = ', x[j].solution_value())
         
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        # getNodesandCustomer(nodeCount,data['num_vars'],x,edges,discreteTimeWindows,int(solver.Objective().Value()),timeWindows)

        print()
       
       
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    print(df)
    main()
