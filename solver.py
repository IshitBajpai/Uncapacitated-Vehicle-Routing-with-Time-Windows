from unicodedata import name
from ortools.linear_solver import pywraplp

from ortools.linear_solver import pywraplp



def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    s_x1a= solver.NumVar(0, 1, 's_x1a')
    s_x1b = solver.NumVar(0, 1, 's_x1b')
    s_x2a = solver.NumVar(0, 1, 's_x2a')
    x1a_t = solver.NumVar(0, 1, 'x1a_t')
    x1b_t = solver.NumVar(0, 1, 'x1b_t')
    x2a_t = solver.NumVar(0, 1, 'x2a_t')
    x1a_x2a = solver.NumVar(0, 1, 'x1a_x2a')
    

    print('Number of variables =', solver.NumVariables())

    # constraints on incoming edges for customers
    solver.Add( s_x1a + s_x1b == 1 ) 
    solver.Add( s_x2a + x1a_x2a == 1)

    # constraints on outgoing edges for customers
    solver.Add(x1a_t+x1b_t+x1a_x2a == 1)
    solver.Add(x2a_t == 1)

    #constraints in capacities of edges
    #Done above ig

    print('Number of constraints =', solver.NumConstraints())

    solver.Minimize(s_x1a+s_x1b+s_x2a)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('s_x1a =', s_x1a.solution_value())
        print('s_x1b =', s_x1b.solution_value())
        print('x1a_x2a =',  x1a_x2a.solution_value())
    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())

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
def compareTime(t1,t2): #O(1)
    # considering pm > am if t1 >= t2 return 1
    if(t1[5:]==t2[5:]):
        if(int(t1[:2]) == int(t2[:2])):
            if(int(t1[3:5]) >= int(t2[3:5])):
                return 1
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
    while(compareTime(timeWindow[1],currtime) == 1): 
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
    tw2 = ['09:20am','09:25a,']
    tw3 = ['9:40','10:40']

    starting_time = '6:00am'

    timeMatrix = [ [9999,10,5], 
             [9999],[] ]
    # print(addTime("08:30am",20))
    print(discreteTime(tw1,2))


    

if __name__ == '__main__':
    main()