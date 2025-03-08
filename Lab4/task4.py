import heapq
import random
import time

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = []
    
    def add_edge(self, from_node, to_node, base_time):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[(from_node, to_node)] = {
            "base_time": base_time,
            "traffic_multiplier": 1.0
        }
        self.nodes[from_node].append(to_node)
        self.nodes[to_node].append(from_node)
    
    def update_traffic(self, from_node, to_node, traffic_condition):
        if (from_node, to_node) in self.edges:
            base_time = self.edges[(from_node, to_node)]["base_time"]
            traffic_multiplier = 1 + traffic_condition
            self.edges[(from_node, to_node)]["traffic_multiplier"] = traffic_multiplier

    def get_edge_weight(self, from_node, to_node):
        if (from_node, to_node) in self.edges:
            base_time = self.edges[(from_node, to_node)]["base_time"]
            traffic_multiplier = self.edges[(from_node, to_node)]["traffic_multiplier"]
            return base_time * traffic_multiplier
        return float('inf')


class AStarSearch:
    def __init__(self, graph):
        self.graph = graph
    
    def heuristic(self, current, goal):
        return abs(ord(current) - ord(goal))

    def astar(self, start, goal):
        open_list = []
        closed_list = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        heapq.heappush(open_list, (f_score[start], start))

        while open_list:
            _, current = heapq.heappop(open_list)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            closed_list.add(current)
            
            for neighbor in self.graph.nodes[current]:
                if neighbor in closed_list:
                    continue

                tentative_g_score = g_score[current] + self.graph.get_edge_weight(current, neighbor)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
        
        return None


graph = Graph()
graph.add_edge('A', 'B', 5)
graph.add_edge('B', 'C', 3)
graph.add_edge('A', 'C', 10)
graph.add_edge('C', 'D', 1)

graph.update_traffic('A', 'B', 0.2)
graph.update_traffic('B', 'C', -0.1)

astar_search = AStarSearch(graph)
path = astar_search.astar('A', 'D')
print(f"Path from A to D: {path}")

for _ in range(5):
    time.sleep(1)
    from_node = random.choice(['A', 'B', 'C'])
    to_node = random.choice(graph.nodes[from_node])
    traffic_condition = random.uniform(-0.2, 0.5)
    graph.update_traffic(from_node, to_node, traffic_condition)
    print(f"Traffic updated: {from_node} to {to_node} -> {traffic_condition*100:.2f}%")
    
    path = astar_search.astar('A', 'D')
    print(f"Updated path from A to D: {path}")
import heapq
import random
import time

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = []
    
    def add_edge(self, from_node, to_node, base_time):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[(from_node, to_node)] = {
            "base_time": base_time,
            "traffic_multiplier": 1.0
        }
        self.nodes[from_node].append(to_node)
        self.nodes[to_node].append(from_node)
    
    def update_traffic(self, from_node, to_node, traffic_condition):
        if (from_node, to_node) in self.edges:
            base_time = self.edges[(from_node, to_node)]["base_time"]
            traffic_multiplier = 1 + traffic_condition
            self.edges[(from_node, to_node)]["traffic_multiplier"] = traffic_multiplier

    def get_edge_weight(self, from_node, to_node):
        if (from_node, to_node) in self.edges:
            base_time = self.edges[(from_node, to_node)]["base_time"]
            traffic_multiplier = self.edges[(from_node, to_node)]["traffic_multiplier"]
            return base_time * traffic_multiplier
        return float('inf')


class AStarSearch:
    def __init__(self, graph):
        self.graph = graph
    
    def heuristic(self, current, goal):
        return abs(ord(current) - ord(goal))

    def astar(self, start, goal):
        open_list = []
        closed_list = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        heapq.heappush(open_list, (f_score[start], start))

        while open_list:
            _, current = heapq.heappop(open_list)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            closed_list.add(current)
            
            for neighbor in self.graph.nodes[current]:
                if neighbor in closed_list:
                    continue

                tentative_g_score = g_score[current] + self.graph.get_edge_weight(current, neighbor)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
        
        return None


graph = Graph()
graph.add_edge('A', 'B', 5)
graph.add_edge('B', 'C', 3)
graph.add_edge('A', 'C', 10)
graph.add_edge('C', 'D', 1)

graph.update_traffic('A', 'B', 0.2)
graph.update_traffic('B', 'C', -0.1)

astar_search = AStarSearch(graph)
path = astar_search.astar('A', 'D')
print(f"Path from A to D: {path}")

for _ in range(5):
    time.sleep(1)
    from_node = random.choice(['A', 'B', 'C'])
    to_node = random.choice(graph.nodes[from_node])
    traffic_condition = random.uniform(-0.2, 0.5)
    graph.update_traffic(from_node, to_node, traffic_condition)
    print(f"Traffic updated: {from_node} to {to_node} -> {traffic_condition*100:.2f}%")
    
    path = astar_search.astar('A', 'D')
    print(f"Updated path from A to D: {path}")
