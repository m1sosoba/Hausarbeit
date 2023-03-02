import AntColonySystem as ACS
import AntSystem as AS
import MinMaxAntSystem as MMAS
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

            writer.writerow([number,
                             self.run_algo_AS(graph),
                             self.run_algo_AS(graph),
                             self.run_algo_AS(graph),
                             self.run_algo_ACS(graph, t),
                             self.run_algo_ACS(graph, t),
                             self.run_algo_ACS(graph, t),
                             self.run_algo_MMAS(graph, opt),
                             self.run_algo_MMAS(graph, opt),
                             self.run_algo_MMAS(graph, opt)])

    def run_algo_AS(self, graph):
        algo = AS.AntSystem(2, 1, 0.9)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_ACS(self, graph, t):
        algo = ACS.AntColonySystem(2, 1, 0)
        tour = algo.get_optimal_tour(
            graph, t, self.ant_number, self.ant_number, 0.2)
        return self.__get_tour_weight(tour)

    def run_algo_MMAS(self, graph, opt):
        algo = MMAS.MinMaxAntSytem(3, 1, 0.2)
        tour = algo.get_optimal_tour(
            graph, self.ant_number, self.ant_number, opt)
        return self.__get_tour_weight(tour)

    def __get_tour_weight(self, tour):
        return sum(c['weight'] for a, b, c in tour)


def run_multiple_experiments():
    ant_numbers = [10, 30, 50]
    run_numbers = [10, 30, 50]
    dirpath = os.path.dirname(__file__)
    with open(os.path.join(dirpath, f'results\main_test.csv'), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['nodes', 'AS1', 'AS2', 'AS2', 'ACS1',
                         'ACS2', 'ACS3', 'MMAS1', 'MMAS2', 'MMAS3'])
        for run_number in run_numbers:
            writer.writerow([f'runs: {run_number}'])
            for ant_number in ant_numbers:
                writer.writerow([f'ants: {ant_number}'])
                experiment = Experiment(ant_number, run_number)
                experiment.run(writer)


run_multiple_experiments()
