"""
Sokoban Solver using SAT (Boilerplate)
--------------------------------------
Instructions:
- Implement encoding of Sokoban into CNF.
- Use PySAT to solve the CNF and extract moves.
- Ensure constraints for player movement, box pushes, and goal conditions.

Grid Encoding:
- 'P' = Player
- 'B' = Box
- 'G' = Goal
- '#' = Wall
- '.' = Empty space
"""

from pysat.formula import CNF
from pysat.solvers import Solver

# Directions for movement
DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


class SokobanEncoder:
    def __init__(self, grid, T):
        """
        Initialize encoder with grid and time limit.

        Args:
            grid (list[list[str]]): Sokoban grid.
            T (int): Max number of steps allowed.
        """
        self.grid = grid
        self.T = T
        self.N = len(grid)
        self.M = len(grid[0])

        self.goals = []
        self.boxes = []
        self.walls = []
        self.player_start = None

        # TODO: Parse grid to fill self.goals, self.boxes, self.player_start
        self._parse_grid()

        self.num_boxes = len(self.boxes)
        self.cnf = CNF()

    def _parse_grid(self):
        """Parse grid to find player, boxes, and goals."""
        # TODO: Implement parsing logic
        for y,row in enumerate(self.grid):
            for x,value in enumerate(row):
                if value=='P':
                    self.player_start = (x+1,y+1)
                if value=='B':
                    self.boxes.append((x+1,y+1))
                if value=='#':
                    self.walls.append((x+1,y+1))
                if value=='G':
                    self.goals.append((x+1,y+1))
        pass

    # ---------------- Variable Encoding ----------------
    def var_player(self, x, y, t):
        """
        Variable ID for player at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        return t*1000 + y*21 + x

    def var_box(self, b, x, y, t):
        """
        Variable ID for box b at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        return (b+1)*100000+ t*1000 + y*21 + x
        pass

    # ---------------- Encoding Logic ----------------
    def encode(self):
        """
        Build CNF constraints for Sokoban:
        - Initial state
        - Valid moves (player + box pushes)
        - Non-overlapping boxes
        - Goal condition at final timestep
        """
        # TODO: Add constraints for:
        # 1. Initial conditions
        # 2. Player movement
        # 3. Box movement (push rules)
        # 4. Non-overlap constraints
        # 5. Goal conditions
        # 6. Other conditions

        

        M = self.M # number of columns so x coord so the 2nd coord
        N = self.N # number of rows so y coord so the 1st coord
        T = self.T
        num_boxes = self.num_boxes
        cnf = CNF()

        #initial condition
        i = 0
        for pos in self.boxes:
            y = pos[1]
            x = pos[0]
            cnf.append([self.var_box(i,x,y,0)])
            i = i+1

        py = self.player_start[1]
        px = self.player_start[0]

        cnf.append([self.var_player(px,py,0)])

        
        #SINGLE POSITION RULES
        #Player
        for t in range(T+1):
            cnf.append([self.var_player(x,y,t) for x in range(1,M+1) for y in range(1,N+1)]) # player at atleast one position
        
        for t in range(T+1):
            for x1 in range(1,M+1):
                for y1  in range(1,N+1):
                    for x2 in range(1,M+1):
                        for y2 in range(1,N+1):
                            if(x2>x1 or (x1==x2 and y2>y1)):
                                cnf.append([-self.var_player(x1,y1,t),-self.var_player(x2,y2,t)]) # player at not more than one position
        
        #Boxes
        for b in range(num_boxes):
            for t in range(T+1):
                cnf.append([self.var_box(b,x,y,t) for x in range(1,M+1) for y in range(1,N+1)])
        
        for b in range(num_boxes):
            for t in range(T+1):
                for x1 in range(1,M+1):
                    for y1  in range(1,N+1):
                        for x2 in range(1,M+1):
                            for y2 in range(1,N+1):
                                if(x2>x1 or (x1==x2 and y2>y1)):
                                    cnf.append([-self.var_box(b,x1,y1,t),-self.var_box(b,x2,y2,t)])
        
        #NO COINCIDENCE RULES
        #Player and boxes shouldnt be in a wall
        for pos in self.walls:
            y = pos[1]
            x = pos[0]
            for t in range(T+1):
                cnf.append([-self.var_player(x,y,t)])
                for b in range(num_boxes):
                    cnf.append([-self.var_box(b,x,y,t)])
        
        #Player shouldnt be in boxes
        for b in range(self.num_boxes):
            for t in range(T+1):
                for x in range(1,M+1):
                    for y  in range(1,N+1):
                        cnf.append([-self.var_player(x,y,t),-self.var_box(b,x,y,t)])
        
        #Boxes shouldnt be in boxes
        for b1 in range(self.num_boxes):
            for b2 in range(self.num_boxes):
                if(b2>b1):
                    for t in range(T+1):
                        for x in range(1,M+1):
                            for y  in range(1,N+1):
                                cnf.append([-self.var_box(b1,x,y,t),-self.var_box(b2,x,y,t)])
        
        #MOVEMENT LOGIC
        #player move
        for t in range(T):
            for x in range(1,M+1):
                for y  in range(1,N+1):
                    lis = []
                    lis.append(-self.var_player(x,y,t))
                    if(x+1<=M):
                        lis.append(self.var_player(x+1,y,t+1))
                    if(y+1<=N):
                        lis.append(self.var_player(x,y+1,t+1))
                    if(x-1>0):
                        lis.append(self.var_player(x-1,y,t+1))
                    if(y-1>0):
                        lis.append(self.var_player(x,y-1,t+1))
                    cnf.append(lis)
        #box move
        for b in range(self.num_boxes):
            for t in range(T):
                for x in range(1,M+1):
                    for y  in range(1,N+1):
                        if(x+1<=M and x-1>0):
                            cnf.append([-self.var_box(b,x,y,t),-self.var_player(x,y,t+1),-self.var_player(x-1,y,t),self.var_box(b,x+1,y,t+1)])
                            cnf.append([-self.var_box(b,x,y,t),-self.var_player(x,y,t+1),-self.var_player(x+1,y,t),self.var_box(b,x-1,y,t+1)])
                        if(y+1<=N and y-1>0):
                            cnf.append([-self.var_box(b,x,y,t),-self.var_player(x,y,t+1),-self.var_player(x,y-1,t),self.var_box(b,x,y+1,t+1)])
                            cnf.append([-self.var_box(b,x,y,t),-self.var_player(x,y,t+1),-self.var_player(x,y+1,t),self.var_box(b,x,y-1,t+1)])
        
        #preventing illegal box moves like if box is at edge and player moves into it
        for b in range(self.num_boxes):
            for t in range(T):
                x = M
                for y in range(1,N+1):
                    cnf.append([-self.var_box(b,x,y,t),-self.var_player(x-1,y,t),-self.var_player(x,y,t+1)])
                x=1
                for y in range(1,N+1):
                    cnf.append([-self.var_box(b,x,y,t),-self.var_player(x+1,y,t),-self.var_player(x,y,t+1)])
                y=N
                for x in range(1,M+1):
                    cnf.append([-self.var_box(b,x,y,t),-self.var_player(x,y-1,t),-self.var_player(x,y,t+1)])
                y=1
                for x in range(1,M+1):
                    cnf.append([-self.var_box(b,x,y,t),-self.var_player(x,y+1,t),-self.var_player(x,y,t+1)])

        #box dont move
        for b in range(self.num_boxes):
            for t in range(T):
                for x in range(1,M+1):
                    for y  in range(1,N+1):
                        cnf.append([-self.var_box(b,x,y,t),self.var_player(x,y,t+1),self.var_box(b,x,y,t+1)])
        
        #FINAL CHECKS
        for b in range(self.num_boxes):
            cnf.append([self.var_box(b,x,y,T) for (x,y) in self.goals])
        self.cnf  = cnf
        return cnf

def decode(model, encoder):
    """
    Decode SAT model into list of moves ('U', 'D', 'L', 'R').

    Args:
        model (list[int]): Satisfying assignment from SAT solver.
        encoder (SokobanEncoder): Encoder object with grid info.

    Returns:
        list[str]: Sequence of moves.
    """
    N, M, T = encoder.N, encoder.M, encoder.T

    moves = []
    lastpos = (0,0)

    
    for x in range(1,M+1):
        for y in range(1,N+1):
            index = y*100 + x
            if index in model:
                lastpos = (x,y)

    for t in range(1,T+1):
        for x in range(1,M+1):
            for y in range(1,N+1):
                index = t*1000 + y*21 + x
                if index in model:
                    px = lastpos[0]
                    py = lastpos[1]
                    if(px==x and py-y==1):
                        moves.append('U')
                    if(px==x and py-y==-1):
                        moves.append('D')
                    if(px-x==-1 and py==y):
                        moves.append('R')
                    if(px-x==1 and py==y):
                        moves.append('L')
                    lastpos = (x,y)

    for t in range(T+1):
        print("at time ",t)
        for y in range(1,N+1):
            for x in range(1,M+1):
                printe = False
                pindex = t*1000 + y*100 + x
                if(pindex in model):
                    print("P",end=" ")
                    printe = True
                for b in range(encoder.num_boxes):
                    bindex = (b+1)*100000+ t*1000 + y*21 + x
                    if bindex in model:
                        print("B",end=" ")
                        printe = True
                if((x,y) in encoder.walls):
                    print('#',end=" ")
                    printe = True
                elif((x,y) in encoder.goals):
                    print('G',end=" ")
                    printe = True
                if(not printe):
                   print(".",end=" ")
            print("") #this was to visualise the grid


    return moves
    # TODO: Map player positions at each timestep to movement directions
    pass


def solve_sokoban(grid, T):
    """
    DO NOT MODIFY THIS FUNCTION.

    Solve Sokoban using SAT encoding.

    Args:
        grid (list[list[str]]): Sokoban grid.
        T (int): Max number of steps allowed.

    Returns:
        list[str] or "unsat": Move sequence or unsatisfiable.
    """

    encoder = SokobanEncoder(grid, T)
    cnf = encoder.encode()

    with Solver(name='g3') as solver:
        solver.append_formula(cnf)
        if not solver.solve():
            return -1

        model = solver.get_model()
        if not model:
            return -1

        return decode(model, encoder)


