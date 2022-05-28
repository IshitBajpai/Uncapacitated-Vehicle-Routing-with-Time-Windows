from ortools.linear_solver import pywraplp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['constraint_coeffs'] = [
        [1,2],
        [3,-1],
        [1,-1],
    ]
    data['bounds'] = ['14u','0l','2u'] # inclusive
    data['obj_coeffs'] = [3,4]
    data['num_vars'] = 2
    data['num_constraints'] = 3
    return data



def main():
    data = create_data_model()
    solver = pywraplp.Solver.CreateSolver('GLOP')
    infinity = solver.infinity()
    x = {}
    for j in range(data['num_vars']):
        x[j] = solver.NumVar(0, infinity, 'x[%i]' % j)
    print('Number of variables =', solver.NumVariables())


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
    objective.SetMaximization()
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
 