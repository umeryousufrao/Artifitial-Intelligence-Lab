import heapq

class UtilityBasedAgentUCS:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal

    def uniform_cost_search(self):
        pq = [(0, self.start, [])]  # (cost, current_node, path)
        visited = set()
        
        while pq:
            cost, node, path = heapq.heappop(pq)
            if node in visited:
                continue
            path = path + [node]
            visited.add(node)
            
            if node == self.goal:
                return (cost, path)
                
            for neighbor, weight in self.graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor, path))
        return None

# Example usage:
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 5), ('E', 2)],
    'C': [('F', 1)],
    'D': [],
    'E': [('G', 3)],
    'F': [],
    'G': []
}

agent = UtilityBasedAgentUCS(graph, 'A', 'G')
result = agent.uniform_cost_search()
print("Cost and Path:", result)
