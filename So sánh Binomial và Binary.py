def AMO_Binomial(g, vars):
    """
    Binomial Encoding (Pairwise) cho ràng buộc At Most One (AMO)
    :param g: Đối tượng SAT solver (ví dụ: Glucose3())
    :param vars: Danh sách ID của các biến chính
    """
    n = len(vars)
    # Duyệt qua tất cả các cặp biến (i, j) với i < j
    for i in range(n):
        for j in range(i + 1, n):
            # Thêm mệnh đề (¬Xi V ¬Xj)
            g.add_clause([-vars[i], -vars[j]])
            
    # Binomial không dùng biến phụ nên không cần trả về next_id

import math

def AMO_Binary(g, vars, start_id_var):
    """
    Binary Encoding cho ràng buộc At Most One (AMO)
    :param g: Đối tượng SAT solver
    :param vars: Danh sách ID của các biến chính
    :param start_id_var: ID bắt đầu cấp phát cho các biến phụ
    :return: ID biến phụ tiếp theo (next_id_var)
    """
    n = len(vars)
    if n <= 1:
        return start_id_var
        
    # Tính số bit cần thiết để biểu diễn n trạng thái: m = ceil(log2(n))
    m = math.ceil(math.log2(n))
    
    # Tạo danh sách m biến phụ đại diện cho m bit (từ bit 0 đến bit m-1)
    aux_vars = list(range(start_id_var, start_id_var + m))
    
    # Ràng buộc: X_i -> (Bộ bit biến phụ mang giá trị index của i)
    for i in range(n):
        for bit_pos in range(m):
            # Kiểm tra xem bit thứ 'bit_pos' của số 'i' là 1 hay 0
            is_bit_one = (i & (1 << bit_pos)) > 0
            
            if is_bit_one:
                # Nếu bit là 1: X_i -> aux_vars[bit_pos] <=> ¬X_i ∨ aux_vars[bit_pos]
                g.add_clause([-vars[i], aux_vars[bit_pos]])
            else:
                # Nếu bit là 0: X_i -> ¬aux_vars[bit_pos] <=> ¬X_i ∨ ¬aux_vars[bit_pos]
                g.add_clause([-vars[i], -aux_vars[bit_pos]])
                
    return start_id_var + m

from pysat.solvers import Glucose3

def test_AMO():
    # Giả sử ta có 4 biến chính: X1, X2, X3, X4
    variables = [1, 2, 3, 4]
    
    # ---------------- TEST BINOMIAL ----------------
    print("--- Test Binomial Encoding ---")
    g_binom = Glucose3()
    AMO_Binomial(g_binom, variables)
    
    # Giả sử ép X1 và X2 đều là True (Cố tình vi phạm AMO)
    g_binom.add_clause([1])
    g_binom.add_clause([2])
    
    if g_binom.solve():
        print("Trạng thái: SAT (Có lỗi)")
    else:
        print("Trạng thái: UNSAT (Đúng chuẩn AMO, vì có 2 biến True)")
        
    # ---------------- TEST BINARY ----------------
    print("\n--- Test Binary Encoding ---")
    g_bin = Glucose3()
    next_id = max(variables) + 1 # Bắt đầu cấp biến phụ từ số 5
    next_id = AMO_Binary(g_bin, variables, next_id)
    
    # Giả sử ép X2 (index 1) là True -> AMO vẫn thoả mãn
    g_bin.add_clause([2])
    
    if g_bin.solve():
        print("Trạng thái: SAT (Đúng chuẩn AMO, vì chỉ có 1 biến True)")
        print("Model:", g_bin.get_model())
        print(f"ID biến mới tiếp theo cho các ràng buộc sau là: {next_id}")
    else:
        print("Trạng thái: UNSAT (Có lỗi)")

if __name__ == "__main__":
    test_AMO()