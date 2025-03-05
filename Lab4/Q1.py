from collections import deque
import itertools
import math

maze = [
    [0, 1, 0, 0, 2],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [2, 0, 0, 0, 2]
]

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(x, y, maze):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != 1

def best_first_search(maze, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, maze):
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None

def find_goals(maze):
    goals = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                goals.append((i, j))
    return goals

def compute_distance_matrix(maze, goals):
    n = len(goals)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                distance_matrix[i][j] = 0
            else:
                path = best_first_search(maze, goals[i], goals[j])
                if path:
                    distance_matrix[i][j] = len(path) - 1
                else:
                    distance_matrix[i][j] = math.inf
    return distance_matrix

def solve_tsp(distance_matrix):
    n = len(distance_matrix)
    min_cost = math.inf
    best_order = None
    for order in itertools.permutations(range(n)):
        cost = 0
        for i in range(n - 1):
            cost += distance_matrix[order[i]][order[i + 1]]
        if cost < min_cost:
            min_cost = cost
            best_order = order
    return best_order

def find_shortest_path(maze):
    goals = find_goals(maze)
    if not goals:
        return None
    distance_matrix = compute_distance_matrix(maze, goals)
    best_order = solve_tsp(distance_matrix)
    final_path = []
    for i in range(len(best_order) - 1):
        start = goals[best_order[i]]
        end = goals[best_order[i + 1]]
        path = best_first_search(maze, start, end)
        if not path:
            return None
        final_path.extend(path[:-1])
    final_path.append(goals[best_order[-1]])
    return final_path

shortest_path = find_shortest_path(maze)
if shortest_path:
    print("Shortest path covering all goals:", shortest_path)
else:
    print("No valid path found.")