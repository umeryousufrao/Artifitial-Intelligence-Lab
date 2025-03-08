import heapq
import math

def greedy_best_first_delivery_route(points, time_windows, start):
    open_list = []
    heapq.heappush(open_list, (0, start))
    visited = set()
    visited.add(start)
    path = [start]
    current_time = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in points:
            points.remove(current)
            visited.add(current)
            path.append(current)
            current_time += 1
            print(f"Visited: {current}, Current Path: {path}, Current Time: {current_time}")

        if not points:
            print("All points visited. Ending.")
            break

        best_heuristic = float('inf')
        best_neighbor = None

        for neighbor in get_neighbors(current, points, time_windows, current_time):
            if neighbor not in visited:
                heuristic = euclidean_distance(neighbor, points[-1]) if points else 0
                if heuristic < best_heuristic:
                    best_heuristic = heuristic
                    best_neighbor = neighbor
                    print(f"Best Neighbor: {best_neighbor}, Heuristic: {best_heuristic}")

        if best_neighbor:
            heapq.heappush(open_list, (best_heuristic, best_neighbor))

    return path

def get_neighbors(current, points, time_windows, current_time):
    valid_neighbors = []
    for point in points:
        if time_windows[point][0] <= current_time <= time_windows[point][1]:
            valid_neighbors.append(point)
    print(f"Valid Neighbors for {current}: {valid_neighbors}")
    return valid_neighbors

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

points = [(1, 1), (2, 2), (3, 3)]
time_windows = {
    (1, 1): (0, 5),
    (2, 2): (3, 6),
    (3, 3): (2, 7)
}
start = (0, 0)

path = greedy_best_first_delivery_route(points, time_windows, start)
print("Optimized Delivery Path:", path)
