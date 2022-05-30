from operator import le
from unicodedata import name
from numpy import conjugate
from ortools.linear_solver import pywraplp
from ortools.linear_solver import pywraplp
from datetime import datetime

def addTime(s, n): #O(1)
      h, m = map(int, s[:-2].split(':'))
      h %= 12
      if s[-2:] == 'pm':
         h += 12
      t = h * 60 + m + n
      h, m = divmod(t, 60)
      h %= 24
      suffix = 'a' if h < 12 else 'p'
      h %= 12
      if h == 0:
         h = 12
      return "{:02d}:{:02d}{}m".format(h, m, suffix)


def lenghtOfTimeWindow(startTime,endingTime):
    if(startTime[5:]=='pm' and startTime[:2]!='12'):
        hrs = int (startTime[:2]) + 12
        s = str(hrs) + startTime[2:5]+':00'
    else:
        s = startTime[:5]+':00'
    
    if(endingTime[5:]=='pm' and endingTime[:2]!='12'):
        hrs = int (endingTime[:2]) + 12
        e = str(hrs) + endingTime[2:5]+':00'
    else:
        e = endingTime[:5]+':00'
    print(s,e)
    FMT = '%H:%M:%S'
    lenghtOfTw = str(datetime.strptime(e, FMT) - datetime.strptime(s, FMT))
    print(lenghtOfTw)
    c=-1
    for i in lenghtOfTw:
        c+=1
        if (i==':'):
            break
    print(c)
    return 60*int(lenghtOfTw[:c]) + int (lenghtOfTw[c+1:c+3])



def compareTime(t1,t2): #O(1)
    # considering pm > am if t1 > t2 return 1 , = then 0
    if(t1[5:]==t2[5:]):
        if(int(t1[:2]) == int(t2[:2])):
            if(int(t1[3:5]) > int(t2[3:5])):
                return 1
            if(int(t1[3:5]) == int(t2[3:5])):
                return 0
            else:
                return -1
        elif ((int(t1[:2]) > int(t2[:2]))):
            return 1
        else :
            return -1
    if(t1[5:]=='am'):
        return -1
    else:
        return 1



#improve all timewindows are taken as input
def discreteTime(timeWindow,intervalSize):   # O(lenghtOftimeWindow/size)
    tw = [] 
    currtime = timeWindow[0]
    while(compareTime(timeWindow[1],currtime) == 1 or compareTime(timeWindow[1],currtime) == 0): 
        tw.append(currtime)
        currtime=addTime(currtime,intervalSize)
    return tw

def reachableCustomers(timeMatrix,discreteTimeWindowMatrix): # O( (n^2)(m^2)/25 )
    # creates variable => existence of edge bw (i,t)->(j,t') and stores it 
    # x1_6_30_am__x2_7_40_am = solver.NumVar(0, 1, 'x1_6_30_am__x2_7_40_am')
   
    
    
            

               



    # no need 
    pass

def main():
    customers = 3

    tw1 = ['09:00am','09:10am']
    tw2 = ['09:20am','09:25am']
    #tw3 = ['09:40am','10:00am']

    timeWindows = [tw1,tw2] 
    discreteTimeWindows = []
    for i in timeWindows:
        discreteTimeWindows.append(discreteTime(i,5))
    
    print(discreteTimeWindows)
    starting_time = '6:00am'

    # time required to reach from customer i to customer j
    timeMatrix = [ [0,100], # time required to reach i from 1
                   [2,0] ]
    # print(addTime("08:30am",20))
    # print(discreteTime(tw1,2))

    count = 0
    nodeCount =[]
    nodeValues = {}
   
    # for i in discreteTimeWindows:
    #     for j in i:
    #         nodeValues[discreteTimeWindows[discreteTimeWindows.index(i)][i.index(j)]] = count+1
    #         nodeCount[] = count+1
    #         count+=1
    for i in range(0,len(discreteTimeWindows)):
        c = []
        for j in range(0,len(discreteTimeWindows[i])):
            c.append(count+1)
            count+=1
        nodeCount.append(c)
    print(nodeCount)

    edgeNumber = 0
    x = {}
    edges = {}
    edgesList = [] # stores edge number going out of ith node
    edgesList.append([])
    solver = pywraplp.Solver.CreateSolver('GLOP')
    infinity = solver.infinity()
    curr_time = '6:00am'
    for i in range(0,len(discreteTimeWindows)):
        for j in range(0,len(discreteTimeWindows[i])):    # j th node
            u = nodeCount[i][j]
            utime = discreteTimeWindows[i][j]
            e = []  # stores edges reachable from u
            for k in range(0,len(discreteTimeWindows)):
                for l in range(len(discreteTimeWindows[k])-1,-1,-1): # l th node
                    v = nodeCount[k][l]
                    vtime = discreteTimeWindows[k][l]
                    print(utime,vtime)
                    print('time from',u,'to',v,'is',timeMatrix[i][k])
                    print()
                    if(i!=k and  compareTime( addTime(utime,timeMatrix[i][k]),vtime) != 1 ):
                       
                        x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
                        edges['x[%i]' % edgeNumber] = (u,v)
                        e.append(edgeNumber)
                        edgeNumber += 1
                    elif (compareTime( addTime(utime,timeMatrix[i][k] ) , vtime) == 1):
                        break
            edgesList.append(e)

    print(edgeNumber)
    print('x',x)
    print("edges",edges)
    print("edgesList",edgesList)
    

    # out of s
    e =[]
    for i in range(0,len(nodeCount)):
        for j in range(0,len(nodeCount[i])):
            e.append(edgeNumber)
            x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
            edges['x[%i]' % edgeNumber] = (0,nodeCount[i][j])
            edgeNumber+=1
    edgesList[0]=e

    # into t (except s)
    e=[]
    for i in range(0,len(nodeCount)):
        for j in range(0,len(nodeCount[i])):
            x[edgeNumber] =  solver.NumVar(0, 1, 'x[%i]' % edgeNumber)
            edges['x[%i]' % edgeNumber] = (nodeCount[i][j],-1)
            #add edge number in edge list 
            edgesList[nodeCount[i][j]].append(edgeNumber)
            edgeNumber+=1
    edgesList.append([])
    


    print('edge list',edgesList)
    print("edges",edges)
    print('edge number',edgeNumber)

    data = {}

    # for i in range(1,len(edgesList)):
    #     for j in range(0,len(edgesList[i])):
    #         print(edgesList[i][j])

    data['constraint_coeffs'] = [
        
    ]
    data['bounds'] = [] # inclusive

    # contraint for outgoing flow foe a customer
   
    for i in range(0,len(nodeCount)):
        contraint = [0] * (edgeNumber)
        for j in range(0,len(nodeCount[i])):
            node = nodeCount[i][j]
            for k in range(0,len(edgesList[node])):
                e = edgesList[node][k]
                contraint[e] = 1
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1u')
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1l')

    print(data['constraint_coeffs'])
    print(data['bounds'])   

    # constraint for incoming for a customer
    incomingEdgeList =[]
    for i in range(0,len(edgesList)):
        incomingEdgeList.append([])
    for i in edges:
        v = edges[i][1]
        for j in range(0,len(i)):
            if(i[j]==']'):
                break
        edge_no = int(i[2:j])
        incomingEdgeList[v].append(edge_no)

    print(incomingEdgeList)

    for i in range(0,len(nodeCount)):
        contraint = [0] * (edgeNumber)
        for j in range(0,len(nodeCount[i])):
            node = nodeCount[i][j]
            for k in range(0,len(incomingEdgeList[node])):
                e = incomingEdgeList[node][k]
                contraint[e] = 1
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1u')
        data['constraint_coeffs'].append(contraint)
        data['bounds'].append('1l')

    print(data['constraint_coeffs'])
    print(data['bounds'])   

    # constraint for a node incoming = outgoing
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
            

    print(data['constraint_coeffs'])
    print(data['bounds']) 
    

    # objective function minimize outgoing flow from 0 node
    objectiveCoefficients = [0] * (edgeNumber)
    for i in range(0,len(edgesList[0])):
        objectiveCoefficients[edgesList[0][i]]=1
    data['obj_coeffs'] = objectiveCoefficients
    print(objectiveCoefficients)

   
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
    # In Python, you can also set the objective as follows.
    # obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
    # solver.Maximize(solver.Sum(obj_expr))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for j in range(data['num_vars']):
            print(x[j].name(), ' = ', x[j].solution_value())
        print()
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()
