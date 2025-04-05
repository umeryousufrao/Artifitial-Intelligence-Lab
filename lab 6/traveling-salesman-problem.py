from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import matplotlib.pyplot as plt

def create_distance_matrix(points):
    """
    Creates a distance matrix from a list of points.
    
    Args:
        points: List of (x, y) coordinates
    
    Returns:
        Distance matrix where matrix[i][j] is the distance from point i to point j
    """
    num_points = len(points)
    matrix = np.zeros((num_points, num_points))
    
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                # Euclidean distance
                x1, y1 = points[i]
                x2, y2 = points[j]
                matrix[i][j] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return matrix.astype(int)  # Convert to integers for OR-Tools

def solve_tsp(distance_matrix):
    """
    Solves the TSP problem using OR-Tools.
    
    Args:
        distance_matrix: Matrix of distances between cities
    
    Returns:
        A list of city indices representing the optimal tour
    """
    # Create the routing model
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    
    # Define the distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 30
    
    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    
    if solution:
        # Extract the tour
        index = routing.Start(0)
        tour = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            tour.append(manager.IndexToNode(index))
        
        # Calculate total distance
        total_distance = 0
        for i in range(len(tour) - 1):
            total_distance += distance_matrix[tour[i]][tour[i+1]]
        
        return tour, total_distance
    else:
        return None, 0

def visualize_tsp_solution(points, tour):
    """
    Visualizes the TSP solution.
    
    Args:
        points: List of (x, y) coordinates
        tour: List of city indices representing the tour
    """
    # Extract x and y coordinates
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    
    plt.figure(figsize=(10, 8))
    
    # Plot the cities
    plt.scatter(xs, ys, s=100, c='blue')
    
    # Plot the tour
    for i in range(len(tour) - 1):
        plt.plot([points[tour[i]][0], points[tour[i+1]][0]],
                 [points[tour[i]][1], points[tour[i+1]][1]], 'k-')
    
    # Plot the return to the starting city
    plt.plot([points[tour[-1]][0], points[tour[0]][0]],
             [points[tour[-1]][1], points[tour[0]][1]], 'k-')
    
    # Add city labels
    for i, (x, y) in enumerate(points):
        plt.text(x + 1, y + 1, f"City {i}", fontsize=12)
    
    plt.title("TSP Solution")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()

def main():
    # Generate 10 random cities in a 100x100 grid
    np.random.seed(42)  # For reproducibility
    points = [(np.random.randint(0, 100), np.random.randint(0, 100)) for _ in range(10)]
    
    # Create distance matrix
    distance_matrix = create_distance_matrix(points)
    
    # Solve TSP
    tour, total_distance = solve_tsp(distance_matrix)
    
    if tour:
        print(f"Optimal tour: {tour}")
        print(f"Total distance: {total_distance}")
        
        # Visualize the solution
        visualize_tsp_solution(points, tour)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
