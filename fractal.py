#!/usr/bin/env python3
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import sys

RESOLUTION = 1001
SCALE = 1
THRESHOLD = 2

class Fractal:
    def __init__(self, top, left, right, iterations):
        self.iterations = iterations
        self._coordinates = Fractal.createCoordinateMatrix(top, left, right)
        self._results = None

    @staticmethod
    def createCoordinateMatrix(top, left, right):
        temp_matrix = np.zeros((RESOLUTION, RESOLUTION)).astype(complex)
        interval = np.abs(right - left) / (RESOLUTION - 1)

        def generateMatrix():
            for row in range(RESOLUTION):
                if row % 100 == 0:
                    print(row)
                yield [((top - interval * row) * 1j +
                    (left + interval * col)) for col in range(RESOLUTION)]

        return generateMatrix()

    # creates magnitude graph from coordinate matrix
    def create(self, verbose=False):
        temp_matrix = np.zeros((RESOLUTION, RESOLUTION)).astype(float)

        for row in range(RESOLUTION):
            for column in range(RESOLUTION):
                temp_matrix[row][column] = np.abs(self._coordinates[row][column]).real

        if verbose == True:
            print(temp_matrix)

        self._results = temp_matrix

    def show(self, continuous=False, colormap="twilight"):
        if self._results is None:
            raise ValueError("No fractal defined.")
        results = self._results
        results *= SCALE
        if continuous:
            results = np.mod(results, 1)
        im = Image.fromarray(np.uint8(getattr(cm, colormap)(results)*255))
        im.show()
        return

class Julia(Fractal):
    def __init__(self, top, left, right, iterations, c):
        self.c = c
        super().__init__(top, left, right, iterations)

    def create(self, verbose=False):
        temp_matrix = np.zeros((RESOLUTION, RESOLUTION)).astype(float)
        
        print("------------------------")
        print("Creating fractal...")
        print("------------------------")

        for row in range(RESOLUTION):
            if row % 100 == 0:
                print(row)
            for column in range(RESOLUTION):
                temp_number = self._coordinates[row][column]
                for i in range(self.iterations):
                    temp_number = temp_number ** 2 + c
                    if np.abs(temp_number).real > THRESHOLD:
                        break
                temp_matrix[row][column] = np.abs(temp_number).real

        if verbose == True:
            print(temp_matrix)

        self._results = temp_matrix

class Mandelbrot(Fractal):
    def __init__(self, top, left, right, iterations):
        super().__init__(top, left, right, iterations)

    def create(self, verbose=False):
        temp_matrix = np.zeros((RESOLUTION, RESOLUTION)).astype(float)

        print("------------------------")
        print("Creating fractal...")
        print("------------------------")

        row_index = 0
        col_index = 0
        for row in self._coordinates:
            for c in row:
                temp_number = 0
                for i in range(self.iterations):
                    temp_number = temp_number ** 2 + c
                    if np.abs(temp_number).real > THRESHOLD:
                        break
                temp_matrix[row_index][col_index] = np.abs(temp_number).real
                col_index += 1
            col_index = 0
            row_index += 1

        if verbose == True:
            print(temp_matrix)

        self._results = temp_matrix


def takeFirstInput():
    if len(sys.argv) == 1:
        top = float(input("Top? "))
        left = float(input("Left? "))
        right = float(input("Right? "))
        if right <= left:
            raise ValueError("That's greater than your left value.")
        iterations = int(input("Iterations? "))
        return (top, left, right, iterations)
    else:
        arguments = sys.argv.copy()
        arguments.pop(0)
        return tuple(arguments)

if __name__ == "__main__":
    selection = int(input("1: Julia, 2: Mandelbrot: "))
    if not (selection == 1 or selection == 2):
        raise ValueError("Incorrect value")
    elif selection == 1:
        c = complex(input("c? "))
    while 1:
        if selection == 1:
            first_fractal = Julia(*takeFirstInput(), c)
        else:
            first_fractal = Mandelbrot(*takeFirstInput())
        first_fractal.create(verbose=False)
        first_fractal.show(continuous=True)
        input("Zoom in?")
