import networkx as nx
import UnionFindNodes as u
import random


class AntColonySystem:

    # initialize algorithm with default alpha,beta, rho and probability q
    # alpha = parameter for importance of acttractiveness
    # beta = parameter for importance of pheromones
    # rho = pheromone evaporation rate
    # q(q0) = parameter to favour exploration(higher q0) or exploitation(smaller q)
    def __init__(self, alpha=1, beta=1, rho=0.6, q=0.5):
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.t = 0.0002
        # t(t0) = (number of nodes *rough approximation of optimal tour length)^-1 -> use small constant should suffice
        self.globalBestLength = float("inf")
        self.globalBestTour = []

    # Expects a  weighted complete graph, a number of Ants and a number of runs
    # creates the optimal tour thorough a weighted complete graph
    # where each node has been visited once
    def get_optimal_tour(self, graph: nx.Graph, antNumber, runs):
        currentRun = 0
        self.add_initial_pheromones_and_attractiveness(graph)

        while currentRun < runs:
            self.ants_run(graph, antNumber)
            self.update_pheromones(graph)
            currentRun += 1

        return self.get_tour_with_highest_pheromones(graph)

    def get_tour_with_highest_pheromones(self, graph: nx.Graph):
        finalTour = []
        nodeCount = graph.number_of_nodes()
        ufn = u.UnionFindNodes(list(graph.nodes()))

        start = list(graph.nodes)[random.randint(0, nodeCount-1)]
        currentNode = start
        while ufn.count() > 1:
            finalCurrentNode = currentNode
            edgesToUnvisitedAdjacentNodes = self.get_edges_to_unvisited_adjacent_nodes(
                graph, ufn, finalCurrentNode)
            chosenEdge = max(edgesToUnvisitedAdjacentNodes,
                             key=lambda item: item[2]['pheromones'])
            finalTour.append(chosenEdge)
            nextNode = chosenEdge[1] if not ufn.connected(
                currentNode, chosenEdge[1]) else chosenEdge[2]
            ufn.union(currentNode, nextNode)
            currentNode = nextNode

        finalTour.append([edge for edge in list(graph.edges(
            currentNode, data=True)) if edge[0] == start or edge[1] == start][0])
        return finalTour

    # update pheromones for every edge
    # pk,new = (1-rho) * pk,old + rho * pk best global tour
    def update_pheromones(self, graph: nx.Graph):
        for edge in list(graph.edges(data=True)):
            if (edge) in self.globalBestTour:
                if self.rho == 0:
                    edge[2]['pheromones'] = edge[2]["pheromones"] + \
                        (1 / self.globalBestLength)
                else:
                    edge[2]['pheromones'] = (1 - self.rho) * edge[2]["pheromones"] + self.rho * (
                        1 / self.globalBestLength)

    def ants_run(self, graph: nx.Graph, antNumber):
        antTours = self.get_ant_tours(graph, antNumber)

        for i in range(antNumber):
            antTour = antTours[i]
            antTourLength = sum(c['weight'] for a, b, c in antTour)
            if(antTourLength < self.globalBestLength):
                self.globalBestLength = antTourLength
                self.globalBestTour.clear()
                self.globalBestTour = antTour

    # return the tour of one ant over all nodes
    def get_ant_tours(self, graph: nx.Graph, antNumber):
        antTours = {}
        antUFNs = {}
        edgesToUpdate = []
        nodeCount = graph.number_of_nodes()
        for i in range(0, nodeCount):
            edgesToUpdate.clear()
            for m in range(0, antNumber):
                if(i == 0):
                    antTour = []
                    antTours[m] = antTour
                    ufn = u.UnionFindNodes(list(graph.nodes()))
                    start = list(graph.nodes)[random.randint(0, nodeCount-1)]
                    currentNode = start
                    antUFNs[m] = [ufn, currentNode, start]

                if(i < nodeCount - 1):
                    finalCurrentNode = antUFNs[m][1]
                    edgesToUnvisitedAdjacentNodes = self.get_edges_to_unvisited_adjacent_nodes(
                        graph, antUFNs[m][0], finalCurrentNode)
                    chosenEdge = self.get_edge_with_best_visiting_probability(
                        edgesToUnvisitedAdjacentNodes)
                    antTours[m].append(chosenEdge)
                    edgesToUpdate.append(chosenEdge)
                    nextNode = chosenEdge[1] if not antUFNs[m][0].connected(
                        antUFNs[m][1], chosenEdge[1]) else chosenEdge[2]
                    antUFNs[m][0].union(antUFNs[m][1], nextNode)
                    currentNode = nextNode
                    antUFNs[m][1] = currentNode
                else:
                    antTours[m].append([edge for edge in list(graph.edges(
                        currentNode, data=True)) if edge[0] == antUFNs[m][2] or edge[1] == antUFNs[m][2]][0])
                for edge in edgesToUpdate:
                    edge[2]['pheromones'] = (
                        1 - self.rho) * edge[2]['pheromones'] + self.rho * self.t

        return antTours

    # adds initial pheromone value as well as
    # attractiveness value to each edge in a weighted complete graph.
    # Attractiveness = 1.0/ Weight of the edge
    # Initial pheromones = 1.0/ Total Weight of a random tour
    def add_initial_pheromones_and_attractiveness(self, graph: nx.Graph):
        weightOfRandomTour = self.get_weight_of_random_tour(graph)

        for edge in list(graph.edges(data=True)):
            edge[2]['attractiveness'] = 1 / edge[2]['weight']
            edge[2]['pheromones'] = self.t  # t0?

    # Returns the weight of a randomly created Tour,
    # where each Node is visited once for a weighted complete graph.
    def get_weight_of_random_tour(self, graph: nx.Graph):
        weight = 0
        nodeCount = graph.number_of_nodes()
        ufn = u.UnionFindNodes(list(graph.nodes()))

        start = list(graph.nodes)[random.randint(0, nodeCount-1)]
        currNode = start
        nextNode = list(graph.nodes)[random.randint(0, nodeCount-1)]

        while ufn.count() > 1:
            while not ufn.union(currNode, nextNode):
                nextNode = list(graph.nodes)[random.randint(0, nodeCount-1)]
            finalNextNode = nextNode
            weight += [edge for edge in list(graph.edges(
                currNode, data=True)) if edge[0] == finalNextNode or edge[1] == finalNextNode][0][2]["weight"]

            currNode = nextNode

        return weight

    def get_edge_with_best_visiting_probability(self, edgesToUnvisitedAdjacentNodes):
        # action choice rule, if q <= q0
        if(random.random() <= self.q):
            return max(edgesToUnvisitedAdjacentNodes, key=lambda node: self.calculate_acs_probability(node))
        else:
            return max(edgesToUnvisitedAdjacentNodes, key=lambda node: (
                self.calculate_probability_dividend(node) / self.calculate_probability_divisor(
                    edgesToUnvisitedAdjacentNodes)))

    def calculate_acs_probability(self, node):
        return(node[2]['pheromones'] * node[2]['attractiveness'] ** self.alpha)

    def calculate_probability_divisor(self, edgesToUnvisitedAdjacentNodes):
        return sum(
            c['attractiveness'] ** self.alpha + c['pheromones'] ** self.beta for a, b, c in
            edgesToUnvisitedAdjacentNodes)

    def calculate_probability_dividend(self, node):
        return (node[2]['attractiveness'] ** self.alpha + node[2][
            'pheromones'] ** self.beta)

    def get_edges_to_unvisited_adjacent_nodes(self, graph, ufn, current_node):
        edgesToUnvisitedAdjacentNodes = []
        for edge in list(graph.edges(current_node, data=True)):
            if self.is_adjacent_node_not_visited(ufn, current_node, edge):
                edgesToUnvisitedAdjacentNodes.append(edge)
        return edgesToUnvisitedAdjacentNodes

    def is_adjacent_node_not_visited(self, ufn, current_node, edge):
        return not ufn.connected(current_node, edge[0]) or not ufn.connected(current_node, edge[1])
