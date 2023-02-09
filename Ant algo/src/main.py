if __name__ == "__main__":
    import GraphGenerator as gGen
    import networkx as nx
    import matplotlib.pyplot as plt
    import AntColonyTSPAlgo
    gen = gGen.GraphGenerator()
    graph = gen.create_complete_graph(10)
    #edges = list(graph.edges(data=True))
    ant = AntColonyTSPAlgo.AntColonyTSPAlgo()
    print(ant.get_optimal_tour(graph, 5, 10))
    g = nx.Graph()
    g.add_edges_from(ant.get_optimal_tour(graph, 5, 10))

    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.show()
