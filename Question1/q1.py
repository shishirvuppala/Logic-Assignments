"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List

def var_generator(i,j,num): #will return the index of the propositional variable encoding the presense of number num at cell in ith row and jth column
    return (i*90+j*10+num)

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""
    # TODO: implement encoding and solving using PySAT
    #Read in the number in the sudoku
    cnf = CNF()
    for i in range(9):
        for j in range(9):
            if(grid[i][j]!=0):
                cnf.append([var_generator(i,j,grid[i][j])]) #encodes the constraints of the testcase
    #Row constraint
    for i in range(9):
        for num in range(1,10):
            cnf.append([var_generator(i,j,num) for j in range(9)]) #encodes presense of number num atleast once in a row
    #Column constraint
    for j in range(9):
        for num in range(1,10):
            cnf.append([var_generator(i,j,num) for i in range(9)]) #encodes presense of number num atleast once in a column
    #Subbox constraint
    for i in range(3):
        for j in range(3):
            for num in range(1,10):
                cnf.append([var_generator(3*i+k,3*j+l,num) for k in range(3) for l in range(3)]) #encodes presense of number num atleast once in a column
    #Cell constraint
    for i in range(9):
        for j in range(9):
            cnf.append([var_generator(i,j,num) for num in range(1,10)]) # atleast one number per cell
    
    for i in range(9):
        for j in range(9):
            for num1 in range(1,10):
                for num2 in range(num1+1,10):
                    cnf.append([-var_generator(i,j,num1),-var_generator(i,j,num2)]) # no more than one number per cell
    # decoding
    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        if solver.solve():
            model = solver.get_model()
            for element in model:
                if(element>0):
                    num = element%10
                    j = (element//10)%9
                    i = (element//90)
                    grid[i][j] = num
            return grid
        else:
            return []
    