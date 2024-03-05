from random import choice, randint, randrange, random
from . import chromosome as ch


Population = list[ch.Chromosome]


# Initialization: generate initial generation
def generatePopulation(size: int, chromosome_length: int) -> Population:
    return [ch.Chromosome.generate_chromosome(chromosome_length) for _ in range(size)]


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
    return (
        ch.Chromosome(a.sequence[0:p] + b.sequence[:p]),
        ch.Chromosome(b.sequence[0:p] + a.sequence[:p]),
    )


# Performe a mutation on a specific ch.Chromosome
def mutation(population: Population, probability: float):
    if not (0 <= probability <= 1):
        raise ValueError("Probability must be within the interval [0, 1]")

    for chromosome in population:
        if random() <= probability:
            index = randrange(len(chromosome.sequence))
            if chromosome.sequence[index] in ["R", "L"]:
                options = ["R", "U", "D"]  # Removing "L" as it's antipod move
            else:
                options = ["L", "U", "D"]  # Removing "R" as it's antipod move

            chromosome.sequence[index] = choice(options)


# Selection: prepare the next generation
def selection(population: Population) -> Population:  # Which method to use?
    return NotImplementedError  # FIXME: Add an implementation


def runEvolution(population_size: int, generations: int):  # TODO: Assemble this part
    # Initialize population
    pop = generatePopulation(10, 10)

    # Performe selection on initial population
    pop = selection()

    t = 0
