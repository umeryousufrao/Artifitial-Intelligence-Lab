
def dls(node,goal,depth,path,visited):

    if node not in visited:
        visited.append(node)
    else:
        return False
    
    if node==goal:
        path.append(node)
        return True
    
    if depth==0:
        return node==goal
    
    if node not in tree:
        return False
    
    for child in tree[node]:
        if dls(child,goal,depth-1,path,visited):
            path.append(node)
            return True    
        
    return False

def iterative_deepening(start, goal,max_depth):

    for depth in range(max_depth+1):
        print(f"Depth: {depth}")
        path=[]
        visited=[]

        if dls(start,goal,depth,path,visited):
            print("\nPath to goal:", " → ".join(reversed(path)))
            return
    print("Goal not found within depth limit.")

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

start_node="A"
goal_node="I"
max_depth=5
iterative_deepening(start_node,goal_node,max_depth)
