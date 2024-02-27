from random import choices, randint, randrange, random
import numpy as np
import numpy.typing

# Initial sequence of amino acids, "HPPHPPH" or "01001010" (1-for P and 0-for H)
Sequence = list[int]  # or list[str]

# Chromosome = a set o rules (RULD) representing a self-avoiding path in a lattice
Chromosome = list[str]

# Lattice = matrix
# Lattice = numpy.typing.NDArray(
#     (int, int), -1, dtype=np.int8
# )  # Something like this, a matrix filled with -1 to easily represent P and H in it (1 and 0), can be obtained with np.full()

# Population = a list of chromosomes
Population = list[Chromosome]


def generateChromosome(length: int) -> Chromosome:
    return choices(["R", "U", "L", "D"], k=length)


# Initialization: generate initial generation
def generatePopulation(size: int, chromosome_length: int) -> Population:
    return [generateChromosome(chromosome_length) for _ in range(size)]


# Descritpion
def getLattice(lines: int, columns: int):
    return np.full((lines, columns), -1, dtype=np.int8)


# Evaluate a chromosome fitness
def fitness(chromosome: Chromosome) -> float:
    length = len(chromosome)
    lattice = getLattice(  # TODO: find a better solution
        length, length
    )  # easiest/worst solution, regarding memory at least, get a matrix of size 4n^2

    collision = score = 0
    X = Y = (
        length - 1
    )  # Does it make any difference if it's either length or length-1 ?

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Flag used to check sequential neighbours
    flag = False

    for letter in chromosome:
        # Collision in folding
        if lattice[X][Y] in [0, 1]:
            collision += 1

        # Populate lattice
        lattice[X][Y] = 0 if letter == "H" else 1

        # Raised flag -> previous letter was H
        if flag and letter == "H":
            score -= 1

        # Check for neighbour H
        # TODO: Handle auto of bounds check
        for dir in directions:
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

        # Raise the flag whether the current letter is H
        flag = True if letter == "H" else False

    if collision == 0:
        return score * 100 + 1
    elif collision == 2:
        return (score * 100 + 1) / 2
    else:
        return (score * 100 + 1) / collision * collision


# Performe crossover on two parents and return two new children
def singlePointCrossover(a: Chromosome, b: Chromosome) -> tuple[Chromosome, Chromosome]:
    if len(a) != len(b):
        raise ValueError("Genome a and b must be of the same lenght")

    lenght = len(a)

    if lenght < 2:
        return a, b

    p = randint(1, lenght - 1)
    return a[0:p] + b[:p], b[0:p] + a[:p]


# Performe a mutation on a specific Chromosome
def mutation(population: Population, probability: float) -> Chromosome:
    for chromosome in population:
        if random() <= probability:
            index = randrange(len(chromosome))
            weights = (
                [0, 1, 0, 1] if chromosome[index] in ["R", "L"] else [1, 0, 1, 0]
            )  # Set zero weight for antipod moves [R, L] and [U, D]

            chromosome[index] = choices(
                ["R", "U", "L", "D"], weights=weights
            ).pop()  # Why pop(), to return a string instead of a list[str]

    return chromosome


# Selection: prepare the next generation
def selection():
    # TODO: Sort with a dict (index, fitness) ensure elitism
    return NotImplementedError  # FIXME: Add an implementation


def runEvolution():  # TODO: Assemble this part
    pop = generatePopulation(10, 10)
