import heapq
import random
import time


graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}


def heuristic(node, goal):
    heuristic_values = {'A': 3, 'B': 2, 'C': 1, 'D': 0}
    return heuristic_values[node]

def a_star_dynamic(graph, start, goal):
    open_queue = []
    heapq.heappush(open_queue, (0, start))
    g_values = {node: float('inf') for node in graph}
    g_values[start] = 0
    came_from = {}

    while open_queue:
        _, current = heapq.heappop(open_queue)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor, cost in graph[current].items():
            tentative_g = g_values[current] + cost
            if tentative_g < g_values[neighbor]:
                came_from[neighbor] = current
                g_values[neighbor] = tentative_g
                f_value = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_queue, (f_value, neighbor))

        
        time.sleep(1) 
        update_edge_costs(graph)

    return None

def update_edge_costs(graph):
    for node in graph:
        for neighbor in graph[node]:
            graph[node][neighbor] = random.randint(1, 10)
    print("Updated edge costs:", graph)


start = 'A'
goal = 'D'
print("Initial graph:", graph)
path = a_star_dynamic(graph, start, goal)
if path:
    print("Optimal path:", path)
else:
    print("No path found.")