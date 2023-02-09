import networkx as nx
import random


# GraphGenerator contains functions to create weighted graphs
# where all vertices are connected for tsp

class GraphGenerator:

    # createCompleteGraph generates a complete Graph with n vertices where
    # every edge is given a random weight between 1 and 100
    # At least 4 Nodes are expected to create a loop with
    # variable routes for tsp

    def create_complete_graph(self, v):
        if v < 4:
            raise Exception("At least four vertices are needed!")

        completeGraph = nx.Graph()
        completeGraph.add_nodes_from(range(v))

        # Iterate over all vertices and create an edge between the current
        # vertex and all following vertices
        vertices = list(completeGraph.nodes)
        for i in range(v - 1):
            currentVertex = vertices[i]
            for j in range(i + 1, v):
                targetVertex = vertices[j]
                completeGraph.add_edge(
                    currentVertex, targetVertex, weight=random.randint(1, 100))

        return completeGraph


