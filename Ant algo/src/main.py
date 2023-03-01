if __name__ == "__main__":
    import GraphGenerator as gGen
    import networkx as nx
    import matplotlib.pyplot as plt
    import AntSystem
    # gen = gGen.GraphGenerator()
    # graph = gen.create_complete_graph(50)
    # nx.write_edgelist(graph, 'graph_50.edgelist')
    g = nx.read_edgelist('graph_50.edgelist')
    # tsp = nx.approximation.traveling_salesman_problem
    tsp = nx.approximation.greedy_tsp
    cycle = tsp(g)
    cost = sum(g[n][nbr]["weight"] for n, nbr in nx.utils.pairwise(cycle))
    print(cycle)
    print(cost)
    # pos = nx.spring_layout(g)
    # nx.draw(g, pos, with_labels=True)
    # labels = nx.get_edge_attributes(g, 'weight')
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    # plt.show()
