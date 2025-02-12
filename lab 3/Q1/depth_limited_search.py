class GoalBasedAgentDLS:
    def __init__(self, graph, start, goal, depth_limit):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.depth_limit = depth_limit

    def depth_limited_search(self, node, depth):
        if depth > self.depth_limit:
            return None
        if node == self.goal:
            return [node]
        for neighbor in self.graph.get(node, []):
            path = self.depth_limited_search(neighbor, depth + 1)
            if path:
                return [node] + path
        return None

    def search(self):
        return self.depth_limited_search(self.start, 0)

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

agent = GoalBasedAgentDLS(graph, 'A', 'G', 3)
path = agent.search()
print("Path:", path)
