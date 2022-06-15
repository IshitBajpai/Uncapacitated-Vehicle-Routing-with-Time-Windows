from operator import le
from unicodedata import name
from numpy import conjugate
from ortools.linear_solver import pywraplp
from ortools.linear_solver import pywraplp
from datetime import datetime
import random

# 20 customer -> 1.1 minute
# 30 customers -> 5 minute    1.69 minutes
# 40                          2.45 min
# 50 customer -> 160 minute


def discreteTime(timeWindow, intervalSize):   # O(lenghtOftimeWindow/size)
    tw = []
    currtime = timeWindow[0]
    while (currtime <= timeWindow[1]):
        tw.append(currtime)
        currtime = currtime+intervalSize
    return tw

def main():
    customers = 2

    timeWindows = [[20, 30], [10, 30]]
    # for i in range(0,customers):
    #     st = random.randint(1,2)*10
    #     et = random.randint(1,3)*10 + st
    #     tw = [st,et]
    #     timeWindows.append(tw)

    print("time Windows ", timeWindows)
    print()

    discreteTimeWindows = []
    for i in timeWindows:
        discreteTimeWindows.append(discreteTime(i, 10))

    print("discreteTimeWindows", discreteTimeWindows)
    print()
    # starting_time = '6:00am'

    timeMatrix = [[0, 100], [100, 0]]
    # timeMatrix = []
    # for i in range(0,customers):
    #     timeMatrix.append([0]*customers)
    # for i in range(0,customers):
    #     for j in range(0,customers):
    #         if(i==j):
    #             timeMatrix[i][j] = 0
    #         elif (i<j):
    #             timeMatrix[i][j] = random.randint(1,10)*10
    #             timeMatrix[j][i] = timeMatrix[i][j]

    print("timeMatrix", timeMatrix)
    print()

    count = 0
    nodeCount = []  # assigns a number to node using count and stores its value

    for i in range(0, len(discreteTimeWindows)):
        c = []
        for j in range(0, len(discreteTimeWindows[i])):
            c.append(count+1)
            count += 1
        nodeCount.append(c)

    print("Node Count ", nodeCount)
    print()

    edgeFlows = {}
    edgeNumber = 0
    x = {}
    edges = {}
    edgesList = []  # stores edge number going out of ith node
    edgesList.append([])  # for s
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # GRAPH CONSTRUCTION

    # out of s to starting of each customer
    e = []
    for i in range(0, len(nodeCount)):
        x[edgeNumber] = solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
        edges['x[%i]' % edgeNumber] = (0, nodeCount[i][0])
        edgeFlows[edgeNumber] = (0, nodeCount[i][0])
        e.append(edgeNumber)
        edgeNumber += 1
    edgesList[0] = e

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

    i = 0
    while(i < len(discreteTimeWindows)):
        tu = nodeCount[i][-1]
        start_utime = discreteTimeWindows[i][0]
        end_utime = discreteTimeWindows[i][-1]
        # stores edges reachable from u
        for k in range(0, len(discreteTimeWindows)):
            sv = nodeCount[k][0]

            start_vtime = discreteTimeWindows[k][0]
            end_vtime = discreteTimeWindows[k][-1]

            if(i != k and start_utime + timeMatrix[i][k] > end_vtime):
                break  # not reachable

            elif(i != k and start_vtime > end_utime + timeMatrix[i][k]):
                # edge bw (u,tu) -> (v,sv)
                e = []
                x[edgeNumber] = solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
                edges['x[%i]' % edgeNumber] = (tu, sv)  # u -> v reachable
                edgeFlows[edgeNumber] = (tu, sv)
                print(tu, "->", sv)
                e.append(edgeNumber)
                edgesList[tu].extend(e)
                edgeNumber += 1
                break

            elif(i != k and start_vtime == end_utime + timeMatrix[i][k]):
                e = []
                x[edgeNumber] = solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
                edges['x[%i]' % edgeNumber] = (tu, sv)  # u -> v reachable
                print(tu, "->", sv)
                edgeFlows[edgeNumber] = (tu, sv)
                e.append(edgeNumber)
                edgesList[tu].extend(e)
                edgeNumber += 1
                break

            elif (i != k and start_vtime < end_utime + timeMatrix[i][k]):

                firstReachableNode_index = 0  # first such that node >= sv
                for j in range(0, len(discreteTimeWindows[i])):
                    if(timeMatrix[i][k] + discreteTimeWindows[i][j] >= start_vtime):
                        firstReachableNode_index = j
                        break
                # now starting from firstReachableNode make edges until feasible
                for l in range(firstReachableNode_index, len(discreteTimeWindows[i])):
                    e = []
                    reachingTime = discreteTimeWindows[i][l]+timeMatrix[i][k]
                    for r in range(0, len(discreteTimeWindows[k])):
                        if(discreteTimeWindows[k][r] >= reachingTime):
                            print(edgesList[nodeCount[i][l]])
                            print(nodeCount[i][l], "->", nodeCount[k][r])
                            # edge bw these two
                            x[edgeNumber] = solver.NumVar(
                                0, 1, 'x[%i]' % edgeNumber)
                            edges['x[%i]' % edgeNumber] = (
                                nodeCount[i][l], nodeCount[k][r])  # u -> v reachable
                            edgeFlows[edgeNumber] = (
                                nodeCount[i][l], nodeCount[k][r])

                            e.append(edgeNumber)
                            edgesList[nodeCount[i][l]].extend(e)
                            print("hdhdh", edgesList[nodeCount[i][l]])
                            edgeNumber += 1
                            break
                break

        i += 1

    print('edge list b4 s t', edgesList)
    print()

    # into t (except s)
    e = []
    for i in range(0, len(nodeCount)):
        x[edgeNumber] = solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
        edges['x[%i]' % edgeNumber] = (nodeCount[i][-1], -1)
        edgeFlows[edgeNumber] = (nodeCount[i][-1], -1)
        # add edge number in edge list
        edgesList[nodeCount[i][-1]].append(edgeNumber)
        edgeNumber += 1
    edgesList.append([])

    print("Node Count after s and t:", nodeCount)
    print()

    # GRAPH Construction OVER

    # if I add it to  0 edge i'll get flow for 1 at the same edge  , add to 1 customer 2 customer
    offset = edgeNumber
    print("edge flows:", edgeFlows)

    flows = [0]*customers
    for i in range(customers):
        flows[i] = edgeFlows.copy()
        keys = edgeFlows.keys()
        for j in keys:  # stores key values of edgeflows i.e 0 1 2
            # all x[] > offset are for flow variables
            x[edgeNumber] = solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
            # remove key and replace it by edge
            t = flows[i].pop(j)
            flows[i][edgeNumber] = t
            edgeNumber += 1

    print("flows", flows)

    print()

    with open('edgeList.txt', 'w') as f:
        f.write("Edge List \n")
        f.write(str(edgesList))
    with open('edges.txt', 'w') as f:
        f.write("Edges \n")
        f.write(str(edges))

    print('edge list', edgesList)
    print()
    print("edges", edges)
    print()
    print('edge number', edgeNumber)
    print()

    data = {}

    data['constraint_coeffs'] = []
    data['bounds'] = []  # inclusive

    # contraint for outgoing flow for a customer

    for i in range(0, len(nodeCount)):  # choose one list from nodeCount
        contraint = [0] * (edgeNumber)
        for j in range(0, len(nodeCount[i])):  # se
            node = nodeCount[i][j]
            for k in range(0, len(edgesList[node])):
                e = edgesList[node][k]
                u = edges['x[%i]' % e][0]
                v = edges['x[%i]' % e][1]
                    # print("u", u, "v", v)
                if(v not in nodeCount[i]):
                        # print('hello')
                        # print("u", u, "v", v)
                        contraint[e] = 1
                
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1u')
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1l')

    # print(data['constraint_coeffs'])
    # print(data['bounds'])

    # constraint for incoming for a customer
    incomingEdgeList = []
    for i in range(0, len(edgesList)):
        incomingEdgeList.append([])  # adding lists in a list
    for i in edges:
        v = edges[i][1]  # u -> v

        edge_no = int(i[2:-1])
        incomingEdgeList[v].append(edge_no)

    print("incoming edge list: ", incomingEdgeList)
    print()

    for i in range(0, len(nodeCount)):
        contraint = [0] * (edgeNumber)  # indicates number of edges
        for j in range(0, len(nodeCount[i])):
            node = nodeCount[i][j]
            for k in range(0, len(incomingEdgeList[node])):
                e = incomingEdgeList[node][k]
                u = edges['x[%i]' % e][0]
                v = edges['x[%i]' % e][1]
                    # print("u", u, "v", v)
                if(u not in nodeCount[i]):
                        # print('hello')
                        # print("u", u, "v", v)
                        contraint[e] = 1
                
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1u')
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1l')

    # print(data['constraint_coeffs'])
    # print(data['bounds'])

    # constraint for a node incoming = outgoing
    for i in range(0, len(nodeCount)):
        for j in range(0, len(nodeCount[i])):
            contraint = [0] * (edgeNumber)
            node = nodeCount[i][j]
            for k in range(0, len(incomingEdgeList[node])):
                e = incomingEdgeList[node][k]
                contraint[e] = 1
            for k in range(0, len(edgesList[node])):
                e = edgesList[node][k]
                contraint[e] = -1
            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('0u')

    # print(data['constraint_coeffs'])
    # print(data['bounds'])

    # constraints for incoming = 1
    print("offset", offset)
    # print("flows",flows)
    l = []
    for z in range(len(contraint)):
            l.append(z % 10)
    print(l)
    #  0<= xij - fij    f<x => 0<=x-f
    for j in range(len(flows)):
        diff = offset*j+offset
        for k in flows[j].keys():
            contraint = [0]*edgeNumber
            contraint[k] = -1
            contraint[k-diff] = 1
            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('0l')
    
            print(contraint," >= 0")

    # # constraint for incoming for a particular customer = 1
    print("CONSTRAINT for incoming = 1 ")
    for c in range(customers):
        addn = offset*(c+1)
        for i in range(0, len(nodeCount)):
            # indicates number of edges
            contraint = [0] * (edgeNumber)
            for j in range(0, len(nodeCount[i])):
                node = nodeCount[i][j]
                for k in range(0, len(incomingEdgeList[node])):
                    e = incomingEdgeList[node][k]
                    u = edges['x[%i]' % e][0]
                    v = edges['x[%i]' % e][1]
                    # print("u", u, "v", v)
                    if(u not in nodeCount[i]):
                        # print('hello')
                        # print("u", u, "v", v)
                        contraint[e+addn] = 1

            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('1u')
            data['constraint_coeffs'].append(contraint)
            data['bounds'].append('1l')
           
           
            print(contraint," =  1")

    # print("data[constraints] \n", data['constraint_coeffs'])
    # print("bounds\n",data['bounds'])
    # c=[]
    # for i in range(len(data['constraint_coeffs'][0])):
    #     c.append(i%10)
    # print(c)
    # for i in range(len(data['constraint_coeffs'])):
    #     print(data['constraint_coeffs'][i],"=",data['bounds'][i])

    # # flow conservation for node
    print("Constraint for node conservation")
    l = []
    for z in range(len(contraint)):
            l.append(z % 10)
    print(l)
    for c in range(customers):
        addn = offset*c+offset
        for i in range(0, len(nodeCount)):
            for j in range(0, len(nodeCount[i])):
                contraint = [0] * (edgeNumber)
                node = nodeCount[i][j]
                for k in range(0, len(incomingEdgeList[node])):
                    e = incomingEdgeList[node][k]
                    contraint[e+addn] = 1
                for k in range(0, len(edgesList[node])):
                    e = edgesList[node][k]
                    contraint[e+addn] = -1
                data['constraint_coeffs'].append(contraint)
                data['bounds'].append('0u')

                
                
                print(contraint, " = 0 ")

    # objective function minimize outgoing flow from 0 node
    objectiveCoefficients = [0] * (edgeNumber)
    for i in range(0, len(edgesList[0])):
        objectiveCoefficients[edgesList[0][i]] = 1
    data['obj_coeffs'] = objectiveCoefficients

    # print(objectiveCoefficients)

    data['num_vars'] = edgeNumber
    data['num_constraints'] = len(data['constraint_coeffs'])

    for i in range(data['num_constraints']):
        if(data['bounds'][i][-1] == 'u'):
            constraint = solver.RowConstraint(
                0, int(data['bounds'][i][:-1]), '')
        else:
            constraint = solver.RowConstraint(
                int(data['bounds'][i][:-1]), solver.infinity() , '')
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
        
        # for j in range(data['num_vars']):
        #     print(x[j].name(), ' = ', x[j].solution_value())

        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        # getNodesandCustomer(nodeCount,data['num_vars'],x,edges,discreteTimeWindows,int(solver.Objective().Value()),timeWindows)

        print()

    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
