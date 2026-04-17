from pysat.solvers import Glucose3

class SudokuSATSolver:
    def __init__(self):
        self.solver = Glucose3()
        self.aux_id = 730

    def get_x_id(self,i,j,k):
        return (i-1)*81 + (j-1)*9 + k    

    def add_amo_sc(self, vars_list):
        n = len(vars_list)

        if n <= 1:
            return
        
        s = [self.aux_id + i for i in range(n-1)]
        self.aux_id += (n-1)

        self.solver.add_clause([-vars_list[0], s[0]])

        for i in range(1, n-1):
            self.solver.add_clause([-vars_list[i], s[i]])
            self.solver.add_clause([-s[i-1], s[i]])
            self.solver.add_clause([-vars_list[i], -s[i-1]])

        self.solver.add_clause([-vars_list[n-1], -s[n-2]])

    def solve(self, board):
        for i in range(1, 10):
            for j in range(1, 10):
                self.solver.add_clause([self.get_x_id(i,j,k) for k in range(1, 10)])

        for i in range(1, 10):
            for j in range(1,10):
                self.add_amo_sc([self.get_x_id(i,j,k) for k in range(1, 10)])
        
        for i in range(1, 10):
            for k in range(1, 10):
                self.add_amo_sc([self.get_x_id(i,j,k) for j in range(1,10)])

        for j in range(1, 10):
            for k in range(1,10):
                self.add_amo_sc([self.get_x_id(i,j,k) for i in range(1, 10)])

        for r_st in [1, 4, 7]:
            for c_st in [1, 4, 7]:
                for k in range(1, 10):
                    block3x3 = []
                    for i in range(r_st, r_st+3):
                        for j in range(c_st, c_st+3):
                            block3x3.append(self.get_x_id(i,j,k))
                    self.add_amo_sc(block3x3)

        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    self.solver.add_clause([self.get_x_id(r+1, c+1, board[r][c])])    
        
        if self.solver.solve():
            lst = self.solver.get_model()
            solved_board = [[0 for x in range(9)] for y in range(9)]
            for var in lst:
                if 0 < var <= 729:
                    v_id = var -1
                    row = v_id // 81
                    col = (v_id//9)%9
                    value = (v_id%9)+1
                    solved_board[row][col] = value
            return solved_board
        return None 
puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SudokuSATSolver()
result = solver.solve(puzzle)

if result:
    for row in result: 
        print(row)
else:
    print("Vô nghiệm")                                     

