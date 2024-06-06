from pulp import *

# Create a linear programming problem
prob = LpProblem("CuttingStockProblem", LpMinimize)

# Order specifications
order_widths = [1000, 680, 500]
order_heights = [2000, 2000, 1000]
order_quantities = [3, 3, 2]

# Define the width of the stock roll
stock_width = 2000

# Define decision variables
x_vars = LpVariable.dicts("x", (range(len(order_widths)), range(stock_width + 1)), 0, None, LpInteger)

# Objective function: minimize the number of rolls used
prob += lpSum([x_vars[i][j] for i in range(len(order_widths)) for j in range(stock_width + 1)])

# Constraints
# Ensure the orders are met
for i in range(len(order_widths)):
    prob += lpSum([x_vars[i][j] for j in range(stock_width + 1)]) >= order_quantities[i]

# Ensure the width constraints are met
for j in range(stock_width + 1):
    prob += lpSum([order_widths[i] * x_vars[i][j] for i in range(len(order_widths))]) <= stock_width

# Solve the problem
prob.solve()

# Print the results
print(f"Status: {LpStatus[prob.status]}")

for i in range(len(order_widths)):
    for j in range(stock_width + 1):
        if value(x_vars[i][j]) > 0:
            print(f"Order {i+1}: Width {order_widths[i]}, Height {order_heights[i]}, Quantity: {value(x_vars[i][j])}")

print(f"Total rolls used: {value(prob.objective)}")