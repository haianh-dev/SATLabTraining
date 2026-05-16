import math
from pysat.solvers import Glucose3

# --- 1. Quản lý ID biến phụ ---
dictionary_id = {}
next_id = 1  # LỖI 1: Chưa gán giá trị khởi tạo cho next_id

def KeySCVar(i, j, s):
    return f"{i}_{j}_{s}"

def SCVar(i, j, s):
    """Lấy hoặc tạo ID cho biến đăng ký R_{i,j,s}"""
    global next_id  # LỖI 2: Cần khai báo global để thay đổi giá trị biến toàn cục
    key = KeySCVar(i, j, s)
    if key in dictionary_id:
        return dictionary_id[key]
    dictionary_id[key] = next_id
    next_id += 1
    return dictionary_id[key]

# --- 2. Mã hóa AMK cho từng Block (Công thức 1-7) ---
def encode_AMK_block(g, block, number_block, k):
    w = len(block)
    # (1) Xi,j -> Ri,j,1
    for j in range(0, w - 1):
        g.add_clause([-block[j], SCVar(number_block, j, 0)])
        
    for j in range(1, w - 1):
        for s in range(0, min(j, k)):
            # (2) Ri,j-1,s -> Ri,j,s
            g.add_clause([-SCVar(number_block, j-1, s), SCVar(number_block, j, s)])
            # (3) Xi,j ^ Ri,j-1,s-1 -> Ri,j,s
            if s > 0:
                g.add_clause([-block[j], -SCVar(number_block, j-1, s-1), SCVar(number_block, j, s)])
    
    # (7) Ràng buộc chặn trên: Xi,j -> -Ri,j-1,k
    for j in range(k, w):
        g.add_clause([-block[j], -SCVar(number_block, j-1, k-1)])

# --- 3. Logic chia Subset (Area) và Block ---
def get_area(vars, weight, number):
    start = weight * number
    end = min(start + weight, len(vars))
    return vars[start:end]

def number_block(number_of_area, is_forward):
    """Xác định ID khối: Mỗi Area có 1 khối xuôi và 1 khối ngược"""
    num = 2 * number_of_area
    return num if is_forward else num + 1

def encode_areas(g, vars, k, weight):
    n_areas = math.ceil(len(vars) / weight)
    for i in range(n_areas):
        area = get_area(vars, weight, i)
        # Area đầu chỉ cần khối ngược, Area cuối chỉ cần khối xuôi, 
        # các Area giữa cần cả hai để kết nối
        if i != 0:
            encode_AMK_block(g, area, number_block(i, True), k) # Khối xuôi
        if i != n_areas - 1:
            encode_AMK_block(g, area[::-1], number_block(i, False), k) # Khối ngược (đảo)

# --- 4. Kết nối các khối (Connecting Clauses) ---
def connect_areas(g, area_idx1, area_idx2, k, weight):
    # Nối khối ngược của Area trước với khối xuôi của Area sau
    id_block_back = number_block(area_idx1, False)
    id_block_fwd = number_block(area_idx2, True)
    
    for j in range(2, weight + 1):
        for p in range(1, k + 1):
            j1 = (weight - j + 1) - 1
            s1 = (k - p + 1) - 1
            j2 = (j - 1) - 1
            s2 = (p) - 1
            if s1 >= 0 and s2 >= 0:
                g.add_clause([-SCVar(id_block_back, j1, s1), -SCVar(id_block_fwd, j2, s2)])

# --- 5. Hàm chạy chính (Main Driver) ---
def solve_ladder_amk(vars, k, weight):
    global next_id  # Cần khai báo global để reset giá trị next_id theo vars
    g = Glucose3()
    next_id = max(vars) + 1
    
    n_areas = math.ceil(len(vars) / weight)
    # Mã hóa từng vùng
    encode_areas(g, vars, k, weight)
    # Kết nối các vùng liền kề
    for i in range(n_areas - 1):
        connect_areas(g, i, i + 1, k, weight)
        
    return g

if __name__ == "__main__":
    variables = list(range(1, 11))
    solver = solve_ladder_amk(variables, k=2, weight=4)
    
    # LỖI 3: Biến của bạn truyền vào là từ 1 đến 10, nên ép biến 2 và 3 chứ không phải 14 và 15
    # Giả sử ép biến 2 và 3 là True (đã đạt ngưỡng k=2 cho cửa sổ x1..x4)
    solver.add_clause([2])
    solver.add_clause([3])
    
    if solver.solve():
        print("SAT - Tìm thấy lời giải!")
        model = solver.get_model()
        print("Các biến True:", [x for x in model if x > 0 and x <= 10])
    else:
        print("UNSAT - Không có lời giải.")