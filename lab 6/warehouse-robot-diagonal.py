import numpy as np
from ortools.sat.python import cp_model
import math

def solve_warehouse_robot_path(grid_size, start, target, obstacles):
    """
    Solve the warehouse robot path finding problem with diagonal movements.
    
    Args:
        grid_size: Size of the grid (n x n)
        start: Tuple (x, y) representing the starting position
        target: Tuple (x, y) representing the target position
        obstacles: List of tuples (x, y) representing obstacle positions
    
    Returns:
        The path as a list of positions
    """
    # Create the model
    model = cp_model.CpModel()
    
    # Estimate max path length (Manhattan distance is a lower bound)
    max_path_length = abs(target[0] - start[0]) + abs(target[1] - start[1])
    # Double it to ensure we have enough steps for diagonal movement
    max_path_length = min(max_path_length * 2, grid_size * grid_size)
    
    # Variables: positions at each step
    x_pos = {}
    y_pos = {}
    
    for step in range(max_path_length + 1):
        x_pos[step] = model.new_int_var(0, grid_size - 1, f'x_{step}')
        y_pos[step] = model.new_int_var(0, grid_size - 1, f'y_{step}')
    
    # Constraints
    
    # Starting position
    model.add(x_pos[0] == start[0])
    model.add(y_pos[0] == start[1])
    
    # Target position (for the last step)
    model.add(x_pos[max_path_length] == target[0])
    model.add(y_pos[max_path_length] == target[1])
    
    # Diagonal movement constraints
    for step in range(max_path_length):
        # Create variables to track diagonal movement
        dx = model.new_int_var(-1, 1, f'dx_{step}')
        dy = model.new_int_var(-1, 1, f'dy_{step}')
        
        # Enforce diagonal movement (dx and dy cannot both be 0)
        zero_dx = model.new_bool_var(f'zero_dx_{step}')
        zero_dy = model.new_bool_var(f'zero_dy_{step}')
        
        model.add(dx == 0).only_enforce_if(zero_dx)
        model.add(dx != 0).only_enforce_if(zero_dx.not_())
        model.add(dy == 0).only_enforce_if(zero_dy)
        model.add(dy != 0).only_enforce_if(zero_dy.not_())
        
        # Both dx and dy cannot be zero (no staying in place)
        model.add(zero_dx + zero_dy <= 1)
        
        # Diagonal movement: Link dx, dy to position changes
        model.add(x_pos[step + 1] == x_pos[step] + dx)
        model.add(y_pos[step + 1] == y_pos[step] + dy)
    
    # Obstacle avoidance
    for step in range(max_path_length + 1):
        for ox, oy in obstacles:
            model.add(x_pos[step] != ox).OnlyEnforceIf(y_pos[step] == oy)
    
    # Path length minimization
    # We add a boolean variable for each step to indicate if we've reached the target
    reached_target = []
    for step in range(max_path_length + 1):
        rt = model.new_bool_var(f'reached_{step}')
        model.add(x_pos[step] == target[0]).only_enforce_if(rt)
        model.add(y_pos[step] == target[1]).only_enforce_if(rt)
        reached_target.append(rt)
    
    # Objective: minimize the first step at which we reach the target
    model.minimize(sum((step + 1) * reached_target[step] for step in range(max_path_length + 1)))
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    # Extract solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        path = []
        for step in range(max_path_length + 1):
            # Check if we've reached the target
            if solver.value(x_pos[step]) == target[0] and solver.value(y_pos[step]) == target[1]:
                path.append((solver.value(x_pos[step]), solver.value(y_pos[step])))
                break
            path.append((solver.value(x_pos[step]), solver.value(y_pos[step])))
        
        # Calculate the total path cost (using Pythagorean theorem for diagonal movement)
        total_cost = 0
        for i in range(len(path) - 1):
            dx = path[i+1][0] - path[i][0]
            dy = path[i+1][1] - path[i][1]
            step_cost = math.sqrt(dx*dx + dy*dy)
            total_cost += step_cost
            
        return path, total_cost
    else:
        return None, 0

# Example usage with a 5x5 grid
grid_size = 5
start = (1, 1)
target = (4, 4)
obstacles = [(2, 2), (3, 2), (2, 3)]  # Example obstacles

def print_grid(grid_size, path, obstacles):
    """Print the grid with the path and obstacles."""
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Mark obstacles
    for ox, oy in obstacles:
        grid[oy][ox] = 'X'
    
    # Mark path
    for step, (x, y) in enumerate(path):
        if (x, y) == start:
            grid[y][x] = 'S'
        elif (x, y) == target:
            grid[y][x] = 'T'
        else:
            grid[y][x] = str(step)
    
    # Print grid
    print(' ' + '-' * (2 * grid_size + 1))
    for row in grid:
        print('|', end=' ')
        for cell in row:
            print(cell, end=' ')
        print('|')
    print(' ' + '-' * (2 * grid_size + 1))

# Solve and print results
path, cost = solve_warehouse_robot_path(grid_size, start, target, obstacles)
if path:
    print(f"Path found: {path}")
    print(f"Total cost: {cost:.2f}")
    print_grid(grid_size, path, obstacles)
else:
    print("No path found.")
