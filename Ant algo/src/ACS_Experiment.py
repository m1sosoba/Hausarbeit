import AntColonySystem as ACS
import GraphGenerator as gen
import csv
import os
import networkx as nx


class Experiment:

    def __init__(self, ant_number, run_number):
        self.node_numbers = [10, 30, 50]
        self.opt10 = 250
        self.opt30 = 397
        self.opt50 = 582
        self.ant_number = ant_number
        self.run_number = run_number

    def run(self, writer):
        number = 10
        for number in self.node_numbers:
            graph = nx.read_edgelist(f'graph_{number}.edgelist')
            if number == 10:
                opt = self.opt10
            elif number == 30:
                opt = self.opt30
            else:
                opt = self.opt50

            t = (number * opt)**(-1)

            # rho test

            # writer.writerow([number, self.run_algo_evaporation_rate(graph, t, 0),
            #                  self.run_algo_evaporation_rate(graph, t, 0.1),
            #                  self.run_algo_evaporation_rate(graph, t, 0.2),
            #                  self.run_algo_evaporation_rate(graph, t, 0.3),
            #                  self.run_algo_evaporation_rate(graph, t, 0.4),
            #                  self.run_algo_evaporation_rate(graph, t, 0.5),
            #                  self.run_algo_evaporation_rate(graph, t, 0.5),
            #                  self.run_algo_evaporation_rate(graph, t, 0.7),
            #                  self.run_algo_evaporation_rate(graph, t, 0.8),
            #                  self.run_algo_evaporation_rate(graph, t, 0.9),
            #                  self.run_algo_evaporation_rate(graph, t, 1)])
            # alpha beta test

            writer.writerow([number,
                             self.run_algo_q(graph, t, 0),
                             self.run_algo_q(graph, t, 0.1),
                             self.run_algo_q(graph, t, 0.2),
                             self.run_algo_q(graph, t, 0.3),
                             self.run_algo_q(graph, t, 0.4),
                             self.run_algo_q(graph, t, 0.5),
                             self.run_algo_q(graph, t, 0.6),
                             self.run_algo_q(graph, t, 0.7),
                             self.run_algo_q(graph, t, 0.8),
                             self.run_algo_q(graph, t, 0.9),
                             self.run_algo_q(graph, t, 1)])

    def run_algo_evaporation_rate(self, graph, t, rho):
        algo = ACS.AntColonySystem(2, 1, rho)
        tour = algo.get_optimal_tour(
            graph, t, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_q(self, graph, t, q):
        algo = ACS.AntColonySystem(2, 1, 0)
        tour = algo.get_optimal_tour(
            graph, t, self.ant_number, self.ant_number, q)
        return self.__get_tour_weight(tour)

    def __get_tour_weight(self, tour):
        return sum(c['weight'] for a, b, c in tour)


def run_multiple_experiments():
    ant_numbers = [10, 30, 50]
    run_numbers = [10, 30, 50]
    dirpath = os.path.dirname(__file__)
    with open(os.path.join(dirpath, f'results\ACS_q_test.csv'), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['nodes', '0', '0.1', '0.2', '0.3',
                         '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'])
        for run_number in run_numbers:
            writer.writerow([f'runs: {run_number}'])
            for ant_number in ant_numbers:
                writer.writerow([f'ants: {ant_number}'])
                experiment = Experiment(ant_number, run_number)
                experiment.run(writer)


run_multiple_experiments()
