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