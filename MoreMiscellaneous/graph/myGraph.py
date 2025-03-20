class myGraph:
    def __init__(self):
        self.graph = {}
    
    def addEdge(self, u, v):
        if u not in self.graph:
            self.graph[u] = [v]
        else:
            self.graph[u].append(v)
    
    def printGraph(self):
        for node, edges in self.graph.items():
            print(f"{node} -> {' -> '.join(map(str, edges))}")
