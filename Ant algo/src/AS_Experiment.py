import AntSystem as ant
import GraphGenerator as gen
import csv
import os
import networkx as nx


class Experiment:

    def __init__(self, ant_number, run_number):
        self.node_numbers = [10, 30, 50]
        self.ant_number = ant_number
        self.run_number = run_number

    def run(self, writer):
        number = 10
        for number in self.node_numbers:
            graph = nx.read_edgelist(f'graph_{number}.edgelist')

            # rho test

            # writer.writerow([number, self.run_algo_evaporation_rate(graph, 0),
            #                  self.run_algo_evaporation_rate(graph, 0.1),
            #                  self.run_algo_evaporation_rate(graph, 0.2),
            #                  self.run_algo_evaporation_rate(graph, 0.3),
            #                  self.run_algo_evaporation_rate(graph, 0.4),
            #                  self.run_algo_evaporation_rate(graph, 0.5),
            #                  self.run_algo_evaporation_rate(graph, 0.5),
            #                  self.run_algo_evaporation_rate(graph, 0.7),
            #                  self.run_algo_evaporation_rate(graph, 0.8),
            #                  self.run_algo_evaporation_rate(graph, 0.9),
            #                  self.run_algo_evaporation_rate(graph, 1)])
            # alpha beta test

            writer.writerow([number,
                             self.run_algo_alpha_beta(graph, 1, 1),
                             self.run_algo_alpha_beta(graph, 2, 2),
                             self.run_algo_alpha_beta(graph, 3, 3),
                             self.run_algo_alpha_beta(graph, 1, 2),
                             self.run_algo_alpha_beta(graph, 1, 3),
                             self.run_algo_alpha_beta(graph, 2, 1),
                             self.run_algo_alpha_beta(graph, 2, 3),
                             self.run_algo_alpha_beta(graph, 3, 1),
                             self.run_algo_alpha_beta(graph, 3, 2)])

    def run_algo_evaporation_rate(self, graph, rho):
        algo = ant.AntSystem(1, 1, rho)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_alpha_beta(self, graph, alpha, beta):
        algo = ant.AntSystem(alpha, beta, 0.9)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def __get_tour_weight(self, tour):
        return sum(c['weight'] for a, b, c in tour)


def run_multiple_experiments():
    ant_numbers = [10, 30, 50]
    run_numbers = [10, 30, 50]
    dirpath = os.path.dirname(__file__)
    with open(os.path.join(dirpath, f'results\AS_alpha_beta_test.csv'), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['nodes', '1/1', '2/2', '3/3', '1/2',
                         '1/3', '2/1', '2/3', '3/1', '3/2'])
        for run_number in run_numbers:
            writer.writerow([f'runs: {run_number}'])
            for ant_number in ant_numbers:
                writer.writerow([f'ants: {ant_number}'])
                experiment = Experiment(ant_number, run_number)
                experiment.run(writer)


run_multiple_experiments()
