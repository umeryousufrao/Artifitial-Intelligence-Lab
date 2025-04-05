import random
import math
from typing import List, Tuple, Dict

class GeneticAlgorithmTSP:
    def __init__(self, cities: List[Tuple[float, float]], population_size: int = 100, 
                 mutation_rate: float = 0.01, elite_size: int = 20, generations: int = 500):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.generations = generations
        self.num_cities = len(cities)
        self.distance_matrix = self._create_distance_matrix()
        
    def _create_distance_matrix(self) -> List[List[float]]:
        matrix = [[0.0 for _ in range(self.num_cities)] for _ in range(self.num_cities)]
        
        for i in range(self.num_cities):
            for j in range(i+1, self.num_cities):
                x1, y1 = self.cities[i]
                x2, y2 = self.cities[j]
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                matrix[i][j] = distance
                matrix[j][i] = distance
                
        return matrix
    
    def _calculate_route_distance(self, route: List[int]) -> float:
        distance = 0.0
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]
            distance += self.distance_matrix[from_city][to_city]
        return distance
    
    def _create_initial_population(self) -> List[List[int]]:
        population = []
        for _ in range(self.population_size):
            route = list(range(self.num_cities))
            random.shuffle(route)
            population.append(route)
        return population
    
    def _rank_routes(self, population: List[List[int]]) -> List[Tuple[int, float]]:
        fitness_results = {}
        for i, route in enumerate(population):
            fitness_results[i] = 1.0 / self._calculate_route_distance(route)
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)
    
    def _selection(self, ranked_population: List[Tuple[int, float]], population: List[List[int]]) -> List[List[int]]:
        selection_results = []
        
        # Elitism - keep the best routes
        for i in range(self.elite_size):
            selection_results.append(population[ranked_population[i][0]])
        
        # Roulette wheel selection for the rest
        fitness_sum = sum(ranked[1] for ranked in ranked_population)
        for _ in range(self.population_size - self.elite_size):
            pick = random.uniform(0, fitness_sum)
            current = 0
            for i, (idx, fitness) in enumerate(ranked_population):
                current += fitness
                if current >= pick:
                    selection_results.append(population[idx])
                    break
        
        return selection_results
    
    def _breed(self, parent1: List[int], parent2: List[int]) -> List[int]:
        # Ordered crossover (OX)
        child = [-1] * self.num_cities
        
        # Select substring from parent1
        start, end = sorted(random.sample(range(self.num_cities), 2))
        
        # Copy substring from parent1 to child
        for i in range(start, end + 1):
            child[i] = parent1[i]
        
        # Fill the remaining positions with cities from parent2
        parent2_idx = 0
        child_idx = 0
        
        while child_idx < self.num_cities:
            if child_idx >= start and child_idx <= end:
                child_idx = end + 1
                continue
                
            if parent2[parent2_idx] not in child:
                child[child_idx] = parent2[parent2_idx]
                child_idx += 1
                
            parent2_idx = (parent2_idx + 1) % self.num_cities
        
        return child
    
    def _breed_population(self, mating_pool: List[List[int]]) -> List[List[int]]:
        children = []
        
        # Keep elite routes
        for i in range(self.elite_size):
            children.append(mating_pool[i])
        
        # Breed the rest
        pool = random.sample(mating_pool, len(mating_pool))
        
        for i in range(self.population_size - self.elite_size):
            child = self._breed(pool[i], pool[len(mating_pool) - i - 1])
            children.append(child)
            
        return children
    
    def _mutate(self, route: List[int]) -> List[int]:
        for i in range(self.num_cities):
            if random.random() < self.mutation_rate:
                j = random.randint(0, self.num_cities - 1)
                route[i], route[j] = route[j], route[i]
        return route
    
    def _mutate_population(self, population: List[List[int]]) -> List[List[int]]:
        mutated_population = []
        
        # Keep elite routes without mutation
        for i in range(self.elite_size):
            mutated_population.append(population[i])
        
        # Mutate the rest
        for i in range(self.elite_size, self.population_size):
            mutated = self._mutate(population[i])
            mutated_population.append(mutated)
            
        return mutated_population
    
    def solve(self) -> Tuple[List[int], float]:
        population = self._create_initial_population()
        
        for _ in range(self.generations):
            ranked_population = self._rank_routes(population)
            mating_pool = self._selection(ranked_population, population)
            children = self._breed_population(mating_pool)
            population = self._mutate_population(children)
        
        # Get the best route after all generations
        best_route_index = self._rank_routes(population)[0][0]
        best_route = population[best_route_index]
        best_distance = self._calculate_route_distance(best_route)
        
        return best_route, best_distance

def solve_tsp(cities: List[Tuple[float, float]]) -> Tuple[List[int], float]:
    ga = GeneticAlgorithmTSP(cities)
    return ga.solve()

if __name__ == "__main__":
    # Example usage with 10 random cities
    random.seed(42)  # For reproducibility
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(10)]
    
    best_route, best_distance = solve_tsp(cities)
    
    print("Best Route:")
    print(" -> ".join(str(city) for city in best_route))
    print(f"Total Distance: {best_distance:.2f}")
