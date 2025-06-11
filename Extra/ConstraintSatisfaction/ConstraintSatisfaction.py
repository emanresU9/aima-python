from constraint import *

# Two machines, X1, and X2. X1 costs $50/hour to run, X2 costs
#  $80/hour to run. Goal is to minimize cost.

# X1 requires 5 units of labor per hour. X2 requires 2 units of
#  labor per hour. Total of 20 units of labor to spend.

# X1 produces 10 units of output per hour. X2 produces 12 units
#  of output per hour. Company needs 90 units of output.



dollar_cost_X1 = 50
dollar_cost_X2 = 80
labor_cost_X1 = 5
labor_cost_X2 = 2
LABOR_LIMIT = 20
production_rate_X1 = 10
production_rate_X2 = 12
production_requirement = 90

# Formulas:  90 <= T1 * production_rate_X1 + T2 * production_rate_X2
#            20 >= T1 * labor_cost_X1 + T2 * labor_cost_X2
#           cost = T1 * dollar_cost_X1 + T2 * dollar_cost_X2