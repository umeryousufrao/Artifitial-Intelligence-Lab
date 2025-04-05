import math
import random
from typing import List, Tuple

class DeliveryRouteOptimizer:
    def __init__(self, locations: List[Tuple[float, float]]):
        self.locations = locations
        self.num_locations = len(locations)
        
    def calculate_total_distance(self, route: List[int]) -> float:
        total_distance = 0.0
        for i in range(len(route)):
            from_idx = route[i]
            to_idx = route[(i + 1) % len(route)]
            
            from_x, from_y = self.locations[from_idx]
            to_x, to_y = self.locations[to_idx]
            
            distance = math.sqrt((to_x - from_x) ** 2 + (to_y - from_y) ** 2)
            total_distance += distance
            
        return total_distance
    
    def generate_neighbors(self, route: List[int]) -> List[List[int]]:
        neighbors = []
        
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                
                new_route = route.copy()
                new_route[i:j] = reversed(new_route[i:j])
                neighbors.append(new_route)
                
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = route.copy()
                new_route[i], new_route[j] = new_route[j], new_route[i]
                neighbors.append(new_route)
                
        return neighbors
    
    def hill_climbing(self, max_iterations: int = 1000) -> Tuple[List[int], float]:
        # Start with a random route
        current_route = [0] + list(range(1, self.num_locations))
        random.shuffle(current_route[1:])
        
        current_distance = self.calculate_total_distance(current_route)
        
        for _ in range(max_iterations):
            improved = False
            neighbors = self.generate_neighbors(current_route)
            
            for neighbor in neighbors:
                neighbor_distance = self.calculate_total_distance(neighbor)
                
                if neighbor_distance < current_distance:
                    current_route = neighbor
                    current_distance = neighbor_distance
                    improved = True
                    break
            
            if not improved:
                break
                
        return current_route, current_distance
    
    def hill_climbing_with_random_restarts(self, num_restarts: int = 5, max_iterations: int = 1000) -> Tuple[List[int], float]:
        best_route = None
        best_distance = float('inf')
        
        for _ in range(num_restarts):
            route, distance = self.hill_climbing(max_iterations)
            
            if distance < best_distance:
                best_route = route
                best_distance = distance
                
        return best_route, best_distance

def optimize_delivery_route(locations: List[Tuple[float, float]]) -> Tuple[List[int], float]:
    optimizer = DeliveryRouteOptimizer(locations)
    return optimizer.hill_climbing_with_random_restarts()

if __name__ == "__main__":
    # Example usage
    locations = [
        (0, 0),      # Starting point (depot)
        (10, 20),
        (15, 30),
        (20, 10),
        (30, 30),
        (40, 20)
    ]
    
    route, distance = optimize_delivery_route(locations)
    
    print("Optimized Route:")
    print(" -> ".join(str(loc) for loc in route))
    print(f"Total Distance: {distance:.2f}")
