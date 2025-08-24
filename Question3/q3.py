from pysat.formula import CNF
from pysat.solvers import Solver
import sys
import glob
import os

input_lines = sys.stdin.read().strip().splitlines()

C = int(input_lines[0])
clauses = [ list(map(int,line.strip().split())) for line in input_lines[1:]]


# take two clause in clauses
# is they are the same except for at one position and at that position they are negs of each other then remove both of them and replace them with the common part
# if one of them is a subset of the other then remove the larger one
# repeat step 2 until the condition is not true
def simplify_clauses(clauses):
    clausesset = [set(c) for c in clauses]
    changed = True

    while(changed):
        pass


# final generator
negset = []

for clause in clauses:
    for lit in clause:
        if(lit>0):
            if(lit not in negset):
                negset.append(lit)

numberofnandgates = 0

for lit in negset:
    a = lit
    print("G{0} = NAND(x{0}, x{0})".format(a))
    numberofnandgates = numberofnandgates + 1

if(C == 1):
    for clause in clauses:
        print("F1 = NAND(",end="")
        numberofnandgates = numberofnandgates + 1
        for i,lit in enumerate(clause):
            if(lit<0):
                print("x{0}".format(abs(lit)),end="")
            else:
                print("G{0}".format(abs(lit)),end="")
            if(i!=len(clause)-1):
                print(", ",end="")
        print(")")
    print("OUTPUT = F1")
    print("Total NAND Gates used: {0}".format(numberofnandgates))

else:
    for ind,clause in enumerate(clauses):
        print("C{0} = NAND(".format(ind+1),end="")
        numberofnandgates = numberofnandgates + 1
        for i,lit in enumerate(clause):
            if(lit<0):
                print("x{0}".format(abs(lit)),end="")
            else:
                print("G{0}".format(abs(lit)),end="")
            if(i!=len(clause)-1):
                print(", ",end="")
        print(")")
    print("F1 = NAND(",end="")
    numberofnandgates = numberofnandgates + 1
    for ind in range(1,C+1):
        print("C{0}".format(ind),end="")
        if(ind!=C):
            print(", ",end="")
    print(")")
    print("F2 = NAND(F1, F1)")
    print("OUTPUT = F2")
    numberofnandgates = numberofnandgates + 1
    print("Total NAND Gates used: {0}".format(numberofnandgates))

