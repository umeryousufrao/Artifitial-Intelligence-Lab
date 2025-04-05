from ortools.sat.python import cp_model
import numpy as np

def compute_island_boundary(island_map):
    """
    Compute the boundary of the largest contiguous landmass.
    
    Args:
        island_map: 2D numpy array where 1 represents land and 0 represents water
    
    Returns:
        A list of boundary points and the total perimeter length
    """
    height, width = island_map.shape
    
    # Create the model
    model = cp_model.CpModel()
    
    # Variables: binary variables for each cell indicating if it's a boundary cell
    is_boundary = {}
    for i in range(height):
        for j in range(width):
            # Only land cells can be boundary cells
            if island_map[i][j] == 1:
                is_boundary[(i, j)] = model.new_bool_var(f'boundary_{i}_{j}')
            else:
                # Water cells are never boundary cells
                is_boundary[(i, j)] = model.new_bool_var(f'boundary_{i}_{j}')
                model.add(is_boundary[(i, j)] == 0)
    
    # Constraints: A land cell is a boundary if at least one adjacent cell is water
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    
    for i in range(height):
        for j in range(width):
            if island_map[i][j] == 1:  # Only consider land cells
                # Create variables for each adjacent cell being water
                adjacent_water = []
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    # If neighbor is out of bounds or is water, it counts as water
                    if ni < 0 or ni >= height or nj < 0 or nj >= width or island_map[ni][nj] == 0:
                        adjacent_water.append(model.new_bool_var(f'water_{i}_{j}_{di}_{dj}'))
                        model.add(adjacent_water[-1] == 1)
                    else:
                        adjacent_water.append(model.new_bool_var(f'water_{i}_{j}_{di}_{dj}'))
                        model.add(adjacent_water[-1] == 0)
                
                # A land cell is boundary if at least one adjacent cell is water
                has_water_neighbor = model.new_bool_var(f'has_water_{i}_{j}')
                model.add(sum(adjacent_water) >= 1).OnlyEnforceIf(has_water_neighbor)
                model.add(sum(adjacent_water) == 0).OnlyEnforceIf(has_water_neighbor.Not())
                
                # Link boundary status to having a water neighbor
                model.add(is_boundary[(i, j)] == has_water_neighbor)
    
    # Objective: Count the boundary cells
    model.maximize(sum(is_boundary.values()))
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    # Extract solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        boundary_points = []
        for i in range(height):
            for j in range(width):
                if solver.value(is_boundary[(i, j)]) == 1:
                    boundary_points.append((i, j))
        
        perimeter = len(boundary_points)
        return boundary_points, perimeter
    else:
        return [], 0

def visualize_boundary(island_map, boundary_points):
    """
    Visualize the island map with its boundary.
    
    Args:
        island_map: 2D numpy array where 1 represents land and 0 represents water
        boundary_points: List of tuples (i, j) representing boundary points
    """
    height, width = island_map.shape
    result = np.zeros((height, width), dtype=str)
    
    # Fill with land and water symbols
    for i in range(height):
        for j in range(width):
            result[i, j] = '🟩' if island_map[i, j] == 1 else '🟦'
    
    # Mark boundary points
    for i, j in boundary_points:
        result[i, j] = '🔴'
    
    # Print the map
    for row in result:
        print(' '.join(row))

# Example usage
def main():
    # Example island map (1 = land, 0 = water)
    island_map = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    boundary_points, perimeter = compute_island_boundary(island_map)
    
    print(f"Island boundary points: {boundary_points}")
    print(f"Perimeter length: {perimeter}")
    
    visualize_boundary(island_map, boundary_points)

if __name__ == "__main__":
    main()
