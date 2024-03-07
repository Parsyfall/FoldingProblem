import random as rd
from chromosome import Chromosome


Population = list[Chromosome]


# Initialization: generate initial generation
def generatePopulation(size: int, chromosome_length: int) -> Population:
    return [Chromosome.generate_chromosome(chromosome_length) for _ in range(size)]


# Performe crossover on two parents and return two new children
def singlePointCrossover(a: Chromosome, b: Chromosome) -> tuple[Chromosome, Chromosome]:
    if len(a.sequence) != len(b.sequence):
        raise ValueError("Genome a and b must be of the same length")

    lenght = len(a.sequence)

    if lenght < 2:
        return a, b

    p = rd.randint(1, lenght - 1)
    return (
        Chromosome(a.sequence[0:p] + b.sequence[:p]),
        Chromosome(b.sequence[0:p] + a.sequence[:p]),
    )


# Performe a mutation on a specific Chromosome
def mutation(population: Population, probability: float):
    if not (0 <= probability <= 1):
        raise ValueError("Probability must be within the interval [0, 1]")

    for chromosome in population:
        if rd.random() <= probability:
            index = rd.randrange(len(chromosome.sequence))
            if chromosome.sequence[index] in ["R", "L"]:
                options = ["R", "U", "D"]  # Removing "L" as it's antipod move
            else:
                options = ["L", "U", "D"]  # Removing "R" as it's antipod move

            chromosome.sequence[index] = rd.choice(options)


# Selection: prepare the next generation
def tournament_selection(
    population: Population, tournament_size: int, offsprings_number: int
) -> Population:
    Temp: Population = []
    Best: Population = []
    for _ in range(offsprings_number):
        # TODO: Find something faster/more efficient than a list for Temp
        Temp = rd.choices(population, k=tournament_size)
        Best.append(tournament(Temp))

    return Best


def tournament(participants: list[Chromosome]) -> Chromosome:
    Best: Chromosome = participants[0]
    for participant in participants[1:]:
        if participant.fitness > Best.fitness:
            Best = participant

    return Best


def runEvolution(population_size: int, generations: int):  # TODO: Assemble this part
    # Initialize population
    pop = generatePopulation(10, 10)

    # Performe selection on initial population
    pop = tournament_selection()

    t = 0
