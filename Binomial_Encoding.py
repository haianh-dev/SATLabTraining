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