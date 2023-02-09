## libs used:

    pip isntall networkx
    pip install matplotlib

## ideas for tests:

    generator:
    - check amount of vertices and edges
        edges of complete graph = n(n-1)/2
    - check for adjacency (graph.adj[node]), every node should 
        be neighbour of every node

    algo:
    - check tour lentgh(nodecount = edgecount)
    - go through the tour and check if all nodes are connected
        and then check last for connection to first node

