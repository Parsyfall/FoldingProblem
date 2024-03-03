from random import choices, randint, randrange, random
import numpy as np
from typing import List


class Chromosome:
    sequence: List[str] = []
    fitness: float = 0.0

    @staticmethod
    def get_lattice(lines: int, columns: int) -> np.ndarray:
        return np.full((lines, columns), -1, dtype=np.int8)

    @staticmethod
    def generate_chromosome(length: int) -> List[str]:
        return choices(["R", "U", "L", "D"], k=length)

    def calc_fitness(self) -> float:
        # TODO: Try orthogonal axes and a vector of points instead of matrix
        length = len(self.sequence)
        lattice = self.get_lattice(length, length)

        collision = score = 0
        X = Y = length - 1

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        flag = False

        for letter in self.sequence:
            if lattice[X][Y] in [0, 1]:
                collision += 1

            lattice[X][Y] = 0 if letter == "H" else 1

            if flag and letter == "H":
                score -= 1

            for dir in directions:
                if 0 <= X + dir[0] < length and 0 <= Y + dir[1] < length:
                    if lattice[X + dir[0]][Y + dir[1]] == 0:
                        score += 1

            match letter:
                case "U":
                    X -= 1
                case "D":
                    X += 1
                case "R":
                    Y += 1
                case "L":
                    Y -= 1

            flag = letter == "H"

        if collision == 0:
            self.fitness = score * 100 + 1
        elif collision == 2:
            self.fitness = (score * 100 + 1) / 2
        else:
            self.fitness = (score * 100 + 1) / collision * collision

        return self.fitness

    def __init__(self, length: int = 1, sequence: List[str] = []) -> None:
        if not sequence:
            sequence = self.generate_chromosome(length)
        self.sequence = sequence
        self.fitness = self.calc_fitness()


Population = list[Chromosome]


# Initialization: generate initial generation
def generatePopulation(size: int, chromosome_length: int) -> Population:
    return [Chromosome.generateChromosome(chromosome_length) for _ in range(size)]


# Performe crossover on two parents and return two new children
def singlePointCrossover(a: Chromosome, b: Chromosome) -> tuple[Chromosome, Chromosome]:
    if len(a.sequence) != len(b.sequence):
        raise ValueError("Genome a and b must be of the same lenght")

    lenght = len(a.sequence)

    if lenght < 2:
        return a, b

    p = randint(1, lenght - 1)
    return a.sequence[0:p] + b.sequence[:p], b.sequence[0:p] + a.sequence[:p]


# Performe a mutation on a specific Chromosome
def mutation(population: Population, probability: float):
    for chromosome in population:
        if random() <= probability:
            index = randrange(len(chromosome.sequence))
            weights = (
                [0, 1, 0, 1]
                if chromosome.sequence[index] in ["R", "L"]
                else [1, 0, 1, 0]
            )  # Set zero weight for antipod moves [R, L] and [U, D]

            chromosome.sequence[index] = choices(
                ["R", "U", "L", "D"], weights=weights
            ).pop()  # Why pop(), to return a string instead of a list[str]


# Selection: prepare the next generation
def selection(population: Population) -> Population:  # Which method to use?
    # TODO: Sort with a dict (index, fitness) ensure elitism
    return NotImplementedError  # FIXME: Add an implementation


def runEvolution(population_size: int, generations: int):  # TODO: Assemble this part
    # Initialize population
    pop = generatePopulation(10, 10)

    # Performe selection on initial population
    pop = selection()

    t = 0
