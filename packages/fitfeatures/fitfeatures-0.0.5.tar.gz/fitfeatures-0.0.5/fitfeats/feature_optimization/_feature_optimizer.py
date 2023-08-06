import hashlib
import logging
from typing import Sequence

import numpy as np
import matplotlib.pyplot as plt
from geneal.genetic_algorithms import BinaryGenAlgSolver
from sklearn.model_selection import cross_val_score

from fitfeats.base import Base


class FeatureOptimizer(BinaryGenAlgSolver, Base):

    def __init__(
            self,
            estimator,
            cv=10,
            scoring=None,
            max_gen: int = 100,
            pop_size: int = 20,
            selection_rate: float = 0.5,
            mutation_rate: float = 0.1,
            selection_strategy: str = "roulette_wheel",
            n_jobs: int = -1,
    ):
        """
        :param estimator: estimator object implementing 'fit'
            The object to use to fit the data.

        :param cv: int, cross-validation generator or an iterable, optional
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:

            - None, to use the default 5-fold cross validation,
            - integer, to specify the number of folds in a `(Stratified)KFold`,
            - :term:`CV splitter`,
            - An iterable yielding (train, test) splits as arrays of indices.

        :param scoring: string, callable or None, optional,
            `default`: r2 for regression, `accuracy` for classification

            A string (see model evaluation documentation) or
            a scorer callable object / function with signature
            ``scorer(estimator, X, y)`` which should return only
            a single value.

            Similar to :func:`cross_validate`
            but only a single metric is permitted.

            If None, the default estimator scorer will be used.

        :param max_gen: int, optional. Default: 100
            Genetic algorithm parameter which controls for how many
            iterations the algorithm is run.

        :param pop_size: int, optional. Default: 20
            Genetic algorithm parameter which controls how many
            individuals exist in the population.

            Must be larger than 2.

        :param selection_rate: float, optional. Default: 0.5
            Genetic algorithm parameter which controls how many
            individuals can be selected for the next generation.

            Must be a number between 0 and 1.

        :param mutation_rate: float, optional. Default: 0.1
            Genetic algorithm parameter which controls how many
            mutations happen on each iteration.

            Must be a number between 0 and 1.

        :param selection_strategy: string, optional. Default: "roulette_wheel"
            Genetic algorithm parameter which controls how individuals
            are selected for crossover.

            Options are:

            - roulette_wheel: This selection strategy orders the individuals
                in the selection pool by probability, with the fittest
                individuals having higher odds of being selected.
            - random: This selection procedure selects randomly individuals
                from the selection pool, following in essence a similar
                procedure as the roulette wheel, but with the same
                probabilities for each individual.
            - two_by_two: This strategy groups the individuals in
                the mating pool 2 by 2, from top to bottom.
            - tournament: This strategy will select 3 individuals
                candidates for each parent position, which are then
                sorted by their fitness and from which the fittest
                one is selected.

        :param n_jobs: int or None, optional. Default: -1
            The number of CPUs to use to do the computation.
            ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
            ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
            for more details.
        """

        Base.__init__(self)

        BinaryGenAlgSolver.__init__(
            self,
            n_genes=1,
            max_gen=max_gen,
            pop_size=pop_size,
            selection_rate=selection_rate,
            mutation_rate=mutation_rate,
            selection_strategy=selection_strategy,
            verbose=False,
            show_stats=True,
        )

        self.scoring = scoring

        self.check_input(estimator, scoring)

        self.estimator = estimator
        self.cv = cv
        self.n_jobs = n_jobs

        self.individuals = {}

        self.selected_features_ = None

    def fitness_function(self, individual):
        """
        Method that the genetic algorithm will call for assessing the fitness
        of each individual.

        :param individual: Chromosome encoding a feature subset selection.

        :return: The fitness of the individual.
        """
        try:
            features = self.features[:, individual == 1]
        except TypeError:
            features = self.features.iloc[:, individual == 1]

        if features.shape[1] == 0:
            return -np.inf

        individual_hash = hashlib.sha1(individual).hexdigest()

        if individual_hash in self.individuals:
            return self.individuals[individual_hash]

        scores = cross_val_score(
            self.estimator,
            features,
            self.target,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=self.n_jobs
        )

        fitness = scores.mean()

        self.individuals[individual_hash] = fitness

        return fitness

    def initialize_population(self):
        """
        Initializes the population of individuals.

        :return: a numpy array with a randomized initialized population
        """

        population = super(FeatureOptimizer, self).initialize_population()

        population[0, :] = 1

        if self.feature_subset_exclude is not None:
            population[:, self.feature_subset_exclude] = 0
            population[-1, :] = 1
            population[-1, self.feature_subset_exclude] = 0

        if self.feature_subset_include is not None:
            population[:, self.feature_subset_include] = 1
            population[-2, :] = 0
            population[-2, self.feature_subset_include] = 1

        return population

    def fit(
            self,
            X,
            y,
            feature_subset_include: Sequence = None,
            feature_subset_exclude: Sequence = None
    ):
        """
        Fits the data and finds the optimal subset of features.

        :param X: {array-like, sparse matrix} of shape (n_samples, n_features)
            Training data

        :param y: array-like of shape (n_samples,) or (n_samples, n_targets)

        :param feature_subset_include: List[int, string], optional. Default: None
            Feature subset to always include in the optimal feature subset.
            Can be an array of ints or strings if X is a pandas dataframe. If
            feature is in both include and exclude subsets, the include subset
            has priority.

        :param feature_subset_exclude: List[int, string], optional. Default: None
            Feature subset to always exclude from the optimal feature subset.
            Can be an array of ints or strings if X is a pandas dataframe. If
            feature is in both include and exclude subsets, the include subset
            has priority.

        :return: None
        """

        try:
            n_genes = X.shape[1]
        except IndexError:
            raise Exception('X must be a 2-D array.')

        self.allowed_mutation_genes = np.arange(n_genes)
        self.n_genes = n_genes

        self.n_mutations = self.get_number_mutations()

        self.set_input_variables(X, y, feature_subset_include, feature_subset_exclude)

        self.solve()

        self.selected_features_ = np.arange(self.features.shape[1])[self.best_individual_ == 1]

    def print_stats(self, time_str):
        """
        Prints the statistics of the optimization run

        :param time_str: time string given by the method get_elapsed_time
        :return: None
        """

        logging.info(f"Total running time: {time_str}")
        logging.info(f"Population size: {self.pop_size}")
        logging.info(f"Number variables: {self.n_genes}")
        logging.info(f"Selection rate: {self.selection_rate}")
        logging.info(f"Mutation rate: {self.mutation_rate}")
        logging.info(f"Number Generations: {self.generations_}\n")
        logging.info(f"Best score: {self.metrics[self.scoring]['factor'] * self.best_fitness_}")

        if self.columns is not None:
            logging.info(f"Best features: {self.columns[self.best_individual_ == 1]}")
        else:
            logging.info(f"Best features: {self.best_individual_ == 1}")

    def plot_fitness_results(self, mean_fitness, max_fitness, iterations):
        """
        Plots the evolution of the mean and max fitness of the population

        :param mean_fitness: mean fitness array for each generation

        :param max_fitness: max fitness array for each generation

        :param iterations: total number of generations

        :return: None
        """

        plt.figure(figsize=(7, 7))

        x = np.arange(1, iterations + 1)

        plt.plot(x, self.metrics[self.scoring]["factor"] * mean_fitness, label="mean score")
        plt.plot(x, self.metrics[self.scoring]["factor"] * max_fitness, label="max score")

        plt.xlabel("Iterations")
        plt.ylabel(self.metrics[self.scoring]["name"])

        plt.legend()
        plt.show()
