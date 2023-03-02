import MinMaxAntSystem as ant
import GraphGenerator as gen
import csv
import os
import networkx as nx


class Experiment:

    def __init__(self, ant_number, run_number):
        self.node_numbers = [10, 30, 50]
        self.ant_number = ant_number
        self.run_number = run_number
        self.opt10 = 250
        self.opt30 = 397
        self.opt50 = 582

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

            # rho test

            # writer.writerow([number, self.run_algo_evaporation_rate(graph, 0, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.1, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.2, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.3, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.4, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.5, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.5, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.7, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.8, opt),
            #                  self.run_algo_evaporation_rate(graph, 0.9, opt),
            #                  self.run_algo_evaporation_rate(graph, 1, opt)])
            # alpha beta test

            writer.writerow([number,
                             self.run_algo_alpha_beta(graph, 1, 1, opt),
                             self.run_algo_alpha_beta(graph, 2, 2, opt),
                             self.run_algo_alpha_beta(graph, 3, 3, opt),
                             self.run_algo_alpha_beta(graph, 1, 2, opt),
                             self.run_algo_alpha_beta(graph, 1, 3, opt),
                             self.run_algo_alpha_beta(graph, 2, 1, opt),
                             self.run_algo_alpha_beta(graph, 2, 3, opt),
                             self.run_algo_alpha_beta(graph, 3, 1, opt),
                             self.run_algo_alpha_beta(graph, 3, 2, opt)])

    def run_algo_evaporation_rate(self, graph, rho, opt):
        algo = ant.MinMaxAntSytem(1, 1, rho)
        tour = algo.get_optimal_tour(
            graph, self.ant_number, self.ant_number, opt)
        return self.__get_tour_weight(tour)

    def run_algo_alpha_beta(self, graph, alpha, beta, opt):
        algo = ant.MinMaxAntSytem(alpha, beta, 0.1)
        tour = algo.get_optimal_tour(
            graph, self.ant_number, self.ant_number, opt)
        return self.__get_tour_weight(tour)

    def __get_tour_weight(self, tour):
        return sum(c['weight'] for a, b, c in tour)


def run_multiple_experiments():
    ant_numbers = [10, 30, 50]
    run_numbers = [10, 30, 50]
    dirpath = os.path.dirname(__file__)
    with open(os.path.join(dirpath, f'results\MMAS_alpha_beta_test.csv'), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # writer.writerow(['nodes', '0', '0.1', '0.2', '0.3',
        #                  '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'])
        writer.writerow(['nodes', '1/1', '2/2', '3/3', '1/2',
                         '1/3', '2/1', '2/3', '3/1', '3/2'])
        for run_number in run_numbers:
            writer.writerow([f'runs: {run_number}'])
            for ant_number in ant_numbers:
                writer.writerow([f'ants: {ant_number}'])
                experiment = Experiment(ant_number, run_number)
                experiment.run(writer)


run_multiple_experiments()
