from random import choices, randint

# Initial sequence of amino acids, "HPPHPPH" or "01001010"
Sequence = list[int]  # or list[str]

# A set o rules (RULD) representing a self-avoiding path in a lattice
Chromosome = list[str]

Population = list[Chromosome]


def generateChromosome(length: int) -> Chromosome:
    return choices(["R", "U", "L", "D"], k=length)


# Initialization: generate initial generation
def generatePopulation(size: int, chromosome_length: int) -> Population:
    return [generateChromosome(chromosome_length) for _ in range(size)]


# Evaluate a chromosome fittnes
def fitness(chromosome: Chromosome):
    return NotImplementedError


# Performe crossover on two parents and return two new childs
def singelPointCrossover(a: Chromosome, b: Chromosome) -> tuple[Chromosome, Chromosome]:
    if len(a) != len(b):
        raise ValueError("Genome a and b must be of the same lenght")
    
    lenght = len(a)
    
    if lenght < 2:
        return a, b

    p = randint(1, lenght -1)
    return a[0:p] + b[:p], b[0:p] + a[:p]



# Performe a mutation on a specific Chromosome
def mutation():
    return NotImplementedError


# Selection: prepare the next generation
def selection():
    return NotImplementedError