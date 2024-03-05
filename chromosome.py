from typing import List
import numpy as np
from random import choices


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
