import AntSystem as ant
import GraphGenerator as gen
import csv
import os


class Experiment:

    def __init__(self, ant_number, run_number):
        self.node_numbers = [10, 20, 30, 40, 50]
        self.ant_number = ant_number
        self.run_number = run_number

    def run(self):
        dirpath = os.path.dirname(__file__)
        with open(os.path.join(dirpath, f'results\AS_rho_test_{self.ant_number}ants_{self.run_number}runs.csv'), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            writer.writerow(['nodes', 0.00, 0.25, 0.50, 0.75, 1.00])
            number = 10
            for number in self.node_numbers:
                graph = gen.GraphGenerator().create_complete_graph(number)

                writer.writerow([number, self.run_algo_no_evaporation_rate(graph),
                                self.run_algo_with_evaporation_rate_25_percent(
                                    graph),
                                self.run_algo_with_evaporation_rate_50_percent(
                                    graph),
                                self.run_algo_with_evaporation_rate_75_percent(
                                    graph),
                                self.run_algo_with_evaporation_rate_100_percent(graph)])

    def run_algo_no_evaporation_rate(self, graph):
        algo = ant.AntSystem(1, 1, 0)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_with_evaporation_rate_25_percent(self, graph):
        algo = ant.AntSystem(1, 1, 0.25)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_with_evaporation_rate_50_percent(self, graph):
        algo = ant.AntSystem(1, 1, 0.5)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_with_evaporation_rate_75_percent(self, graph):
        algo = ant.AntSystem(1, 1, 0.75)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def run_algo_with_evaporation_rate_100_percent(self, graph):
        algo = ant.AntSystem(1, 1, 1)
        tour = algo.get_optimal_tour(graph, self.ant_number, self.ant_number)
        return self.__get_tour_weight(tour)

    def __get_tour_weight(self, tour):
        return sum(c['weight'] for a, b, c in tour)


def run_multiple_experiments():
    ant_numbers = [10, 20, 30, 40, 50]
    run_numbers = [10, 20, 30, 40, 50]
    for run_number in run_numbers:
        print(f'runs: {run_number}')
        for ant_number in ant_numbers:
            experiment = Experiment(ant_number, run_number)
            experiment.run()
            print(
                f'ants: {ant_number}')


run_multiple_experiments()
