"""Example of a simple nurse scheduling problem."""
import ortools
from ortools.sat.python import cp_model


def main():
    # Data.
    num_nurses = 6
    num_shifts = 3
    num_days = 14
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    #all_days = [[0,1,2,3,4,5,6],[7,8,9,10,11,12,13]]
    required_nurses = [[3,1,1],[3,1,1],[3,1,1],[3,1,1],[3,1,1],[2,2,1],[2,2,1],[3,1,1],[3,1,1],[3,1,1],[3,1,1],[3,1,1],[2,2,1],[2,2,1]]
    hourly_wage = [x*8 for x in [25,30,15,2000,35,20]]
    seniority_high = [0,1,0,0,1,1]

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d,
                        s)] = model.NewBoolVar(f'shift_n{n}d{d}s{s}') 
                
    # Each shift is assigned to exactly one nurse in the schedule period.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == required_nurses[d][s])

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # Each shift must have at least one seniority nurse per shift
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)]*seniority_high[n] for n in all_nurses) == 1)

    # max 3 nights per week
    #for week in all_days:
    #   for d in week:
    #       model.Add(sum(shifts[(n, d, s)] for ) <= 3)

    # Objective Function
    model.Minimize(
        sum(hourly_wage[n] * shifts[(n, d, s)] for n in all_nurses
            for d in all_days for s in all_shifts))

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print('Solution:')
        for d in all_days:
            print('Day', d)
            for n in all_nurses:
                for s in all_shifts:
                    if solver.Value(shifts[(n,d,s)]) == 1:
                     print('  Nurse %i (seniority: %i) works shift %i (%i$)' % (n, seniority_high[n], s, hourly_wage[n]))
        print(f'Total wages = {solver.ObjectiveValue()}')
    else:
        print('No optimal solution found !')


    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())



if __name__ == '__main__':
    main()




# import module
import calendar
   
yy = 2021
mm = 12
w = 1
   
# display the calendar
a = print(calendar.month(yy, mm))
print (calendar.calendar(2018))