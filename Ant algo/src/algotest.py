import random

import AntColonyTSPAlgo as ant
import GraphGenerator as gen
import networkx as nx
import unittest


class Algotest(unittest.TestCase):

    def test_random_graph(self):
        graph = gen.GraphGenerator().create_complete_graph(20)

        manuel_graph = nx.Graph()
        number_of_nodes = 20
        manuel_graph.add_nodes_from(range(number_of_nodes))

        nodes = list(manuel_graph.nodes)
        for i in range(manuel_graph.number_of_nodes() - 1):
            current_node = nodes[i]
            for j in range(i + 1, manuel_graph.number_of_nodes()):
                target_node = nodes[j]

                if j - i != 1:
                    manuel_graph.add_edge(current_node, target_node, weight=random.randint(1, 10))
                if j - i == 1 or j - i == (number_of_nodes - 1):
                    manuel_graph.add_edge(current_node, target_node, weight=1)

        algo = ant.AntColonyTSPAlgo()
        tour = algo.get_optimal_tour(graph, 10, 10)
        tour_two = algo.get_optimal_tour(manuel_graph, 10, 10)

        self.assertEqual(20, len(tour))
        self.tour_check(tour)
        self.test_check_edges_complete_graph(graph)
        self.test_check_neighbor_nodes_complete_graph(graph)

        # New Tests
        self.tour_check(tour_two)
        self.test_check_edges_complete_graph(manuel_graph)
        self.test_find_min_weight(tour_two, number_of_nodes)

    def tour_check(self, tour):
        # test if the edges in the path are connected to the following edge
        for i in range(0, len(tour) - 1):
            nodes = set()
            nodes.add(tour[i][0])
            nodes.add(tour[i][1])

            self.assertTrue(tour[i + 1][0] in nodes or tour[i + 1][1] in nodes)
        # finally, test if the last edge of the path is connected to the first node
        firstNodes = set()
        firstNodes.add(tour[0][0])
        firstNodes.add(tour[0][1])

        self.assertTrue(tour[len(tour) - 1][0]
                        in firstNodes or tour[len(tour) - 1][1] in firstNodes)

    def test_check_edges_complete_graph(self, graph):
        # tests, whether the number of edges corresponds to a complete graph
        number_of_nodes = graph.number_of_nodes()
        number_of_edges_in_complete_graph = number_of_nodes * (number_of_nodes - 1) / 2  # n(n-1)/2
        self.assertEqual(graph.number_of_edges(), number_of_edges_in_complete_graph)

    def test_check_neighbor_nodes_complete_graph(self, graph):
        # node degree of each node of the complete graph should be n-1
        for node in list(graph.nodes):
            adj_nodes = list(graph.adj[node])
            self.assertEqual(graph.number_of_nodes() - 1, len(adj_nodes))

    def test_find_min_weight(self, tour, min_length_tour):
        self.assertEqual(min_length_tour, len(tour))


if __name__ == '__main__':
    unittest.main()
