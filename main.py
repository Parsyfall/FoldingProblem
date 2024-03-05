from random import choices, randint, randrange, random
from . import chromosome as ch


Population = list[ch.Chromosome]


# Initialization: generate initial generation
def generatePopulation(size: int, chromosome_length: int) -> Population:
    return [ch.Chromosome.generateChromosome(chromosome_length) for _ in range(size)]


# Performe crossover on two parents and return two new children
def singlePointCrossover(
    a: ch.Chromosome, b: ch.Chromosome
) -> tuple[ch.Chromosome, ch.Chromosome]:
    if len(a.sequence) != len(b.sequence):
        raise ValueError("Genome a and b must be of the same lenght")

    lenght = len(a.sequence)

    if lenght < 2:
        return a, b

    p = randint(1, lenght - 1)
    return a.sequence[0:p] + b.sequence[:p], b.sequence[0:p] + a.sequence[:p]


# Performe a mutation on a specific ch.Chromosome
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
