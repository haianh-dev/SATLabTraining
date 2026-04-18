def add_alk_sc(self, vars_lst, k):
    n = len(vars_lst)
    if k<=0:
        return
    
    if k>n:
        self.solver.add_clause([])
        return 
    
    s = {}
    for i in range(n):
        for j in range(1,k+1):
            s[(i,j)] = self.aux_id
            self.aux_id += 1

    for i in range(n):
        self.solver.add_clause([-vars_lst[i],s[i,1]])     
        if i >0:
            for j in range(1, k+1):
                self.solver.add_clause([-s[(i-1,j)], s[(i,j)]]) 

            for j in range(2,k+1):
                self.solver.add_clause([-vars_lst[i], s[(i-1,j-1)], s[(i,j)]])

            self.solver.add_clause([s[(n-1,k)]])   