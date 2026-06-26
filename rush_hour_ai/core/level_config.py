from core.vehicle import Vehicle
from algorithms.uninformed_search_algorithm.bfs_solver import BFSSolver
from algorithms.uninformed_search_algorithm.dfs_solver import DFSSolver
from algorithms.uninformed_search_algorithm.ids_solver import IDSSolver
from algorithms.informed_search_algorithm.a_star_solver import AStarSolver
from algorithms.local_search_algorithm.stimulated_annealing_solver import AnnealingSolver
from algorithms.search_in_complex_environment.belief_goal_solver import BeliefGoalSolver
from algorithms.constraint_satisfaction_problem.backtracking_solver import BacktrackingSolver
from algorithms.adversarial_search_problem.minimax_solver import MinimaxSolver
from algorithms.informed_search_algorithm.gsa_solver import GSASolver
from algorithms.informed_search_algorithm.ida_star import IDAStarSolver
from algorithms.local_search_algorithm.lbs_solver import LBSSolver
from algorithms.local_search_algorithm.shc_solver import SHCSolver
from algorithms.search_in_complex_environment.and_or_graph import AndOrGraphSolver
from algorithms.constraint_satisfaction_problem.forward_checking import ForwardCheckingSolver
from algorithms.constraint_satisfaction_problem.min_conflict_solver import MinConflictsSolver
from algorithms.search_in_complex_environment.partial_start_solver import PartialStartSolver
from algorithms.adversarial_search_problem.expectimax_solver import ExpectimaxSolver
from algorithms.adversarial_search_problem.alphabeta_solver import AlphaBetaSolver

BG_COLOR = "#0A0C10"
PANEL_COLOR = "#111318"
PANEL2_COLOR = "#161A22"
BORDER_COLOR = "#2A2F3D"
ACCENT_CYAN = "#00E5FF"
ACCENT_ORANGE = "#FF6B35"
GREEN_NEON = "#22C55E"
RED_NEON = "#EF4444"
TEXT_MAIN = "#E2E8F0"
TEXT_MUTED = "#94A3B8"
CELL_SIZE = 76  

CAR_COLORS = {
    # Phe MAX (Đỏ + Xanh Lục)
    'X': {"bg": "#7F1D1D", "border": "#EF4444", "text": "#FCA5A5"}, 
    'A': {"bg": "#064E3B", "border": "#10B981", "text": "#6EE7B7"},
    'B': {"bg": "#064E3B", "border": "#10B981", "text": "#6EE7B7"},
    
    # Phe MIN Cảnh Sát (Đen + Xanh Dương Đậm)
    'C': {"bg": "#0F172A", "border": "#3B82F6", "text": "#93C5FD"},
    'D': {"bg": "#0F172A", "border": "#3B82F6", "text": "#93C5FD"},
    'E': {"bg": "#0F172A", "border": "#3B82F6", "text": "#93C5FD"},
    
    # Xe Trung Lập (Xám / Cam)
    'F': {"bg": "#334155", "border": "#94A3B8", "text": "#CBD5E1"},
    'G': {"bg": "#431407", "border": "#F97316", "text": "#FDBA74"},
    'H': {"bg": "#1A1B4B", "border": "#6366F1", "text": "#A5B4FC"},
    'I': {"bg": "#422006", "border": "#EAB308", "text": "#FDE047"}
}

def get_dummy_vehicles():
    from core.vehicle import Vehicle
    return [
        Vehicle('X', 2, 1, 2, 'H', is_target=True),
        Vehicle('A', 0, 0, 2, 'V'), 
        Vehicle('B', 0, 1, 2, 'H')
    ]

LEVEL_DATA = {
    1: {
        "name": "Gridlock Alpha",
        "bricks": [(0, 3)],
        "vehicles": [
            Vehicle('X', 2, 1, 2, 'H', is_target=True),
            Vehicle('A', 0, 0, 2, 'V'), 
            Vehicle('B', 0, 1, 2, 'H'), 
            Vehicle('C', 1, 3, 2, 'V'), 
            Vehicle('D', 1, 4, 2, 'H'),
            Vehicle('E', 2, 0, 2, 'V'), 
            Vehicle('F', 3, 2, 2, 'V'), 
            Vehicle('G', 3, 3, 2, 'H'),
            Vehicle('H', 3, 5, 3, 'V'), 
            Vehicle('I', 4, 0, 2, 'H'), 
            Vehicle('J', 5, 0, 2, 'H'),
            Vehicle('K', 5, 2, 3, 'H')
        ],
        "algorithms": {
            "BFS": {"label": "Breadth-First Search", "desc": "Tìm theo chiều rộng, duyệt từng lớp.\nĐảm bảo thời gian nhưng tốn RAM.", "solver": BFSSolver()},
            "DFS": {"label": "Depth-First Search", "desc": "Đi sâu vào một nhánh trước.\nÍt tốn bộ nhớ nhưng không đảm bảo thời gian.", "solver": DFSSolver()}, 
            "IDS": {"label": "Iterative Deepening", "desc": "Kết hợp ưu điểm của BFS và DFS.\nKết hợp ưu điểm về thời gian của BFS và bộ nhớ của DFS.", "solver": IDSSolver()}  
        }
    },
    2: {
        "name": "Beta Block",
        "bricks": [(0, 3), (5, 2)],
        "vehicles": [
            Vehicle('X', 2, 1, 2, 'H', is_target=True),
            Vehicle('A', 0, 0, 2, 'H'),
            Vehicle('B', 0, 4, 2, 'H'),
            Vehicle('C', 1, 0, 2, 'V'),
            Vehicle('D', 1, 3, 2, 'V'),
            Vehicle('E', 2, 5, 3, 'V'),
            Vehicle('F', 3, 0, 2, 'V'),
            Vehicle('G', 3, 2, 2, 'V'),
            Vehicle('H', 3, 3, 2, 'H'),
            Vehicle('I', 4, 3, 2, 'H')
        ],
        "algorithms": {
            "GSA": {"label": "Greedy Search", "desc": "Duyệt theo hàm heuristic đánh giá.\nTập trung hướng đích, nhanh kịch bản.", "solver": GSASolver()}, 
            "A*":  {"label": "A* Algorithm", "desc": "Kết hợp chi phí thực tế và heuristic.\nTìm đường ngắn nhất tối ưu tuyệt đối.", "solver": AStarSolver()}, 
            "IDA*": {"label": "Iterative Deepening A*", "desc": "Phiên bản IDA* tiết kiệm bộ nhớ.\nDùng giới hạn chi phí tăng dần.", "solver": IDAStarSolver()}  
        }
    },
    3: {
        "name": "Gamma Trap",
        "bricks": [(0, 1)],
        "vehicles": [
            Vehicle('X', 2, 2, 2, 'H', is_target=True),
            Vehicle('A', 0, 2, 3, 'H'),
            Vehicle('B', 0, 5, 2, 'V'),
            Vehicle('C', 1, 1, 2, 'V'),
            Vehicle('D', 1, 2, 2, 'H'),
            Vehicle('E', 2, 4, 2, 'V'),
            Vehicle('F', 2, 5, 2, 'V'),
            Vehicle('G', 3, 0, 2, 'H'),
            Vehicle('H', 3, 2, 2, 'V'),
            Vehicle('I', 4, 3, 3, 'H'),
            Vehicle('J', 5, 1, 2, 'H')
        ],
        "algorithms": {
            "SHC": {"label": "Stochastic Hill Climbing", "desc": "Leo đồi ngẫu nhiên.\nChọn ngẫu nhiên một trạng thái tốt hơn để tránh tối ưu cục bộ.", "solver": SHCSolver()}, 
            "LBS": {"label": "Local Beam Search", "desc": "Tìm kiếm chùm cục bộ.\nGiữ lại k trạng thái tốt nhất trong mỗi bước duyệt.", "solver": LBSSolver()},
            "SAA": {"label": "Simulated Annealing", "desc": "Mô phỏng luyện kim.\nChấp nhận bước lùi với xác suất giảm dần theo nhiệt độ.", "solver": AnnealingSolver()}
        }
    },
    4: {
        "name": "Delta Hard",
        "bricks": [(0, 0), (5, 0), (5, 5)],
        "vehicles": [
            Vehicle('X', 2, 1, 2, 'H', is_target=True),
            Vehicle('A', 0, 3, 3, 'V'), Vehicle('D', 1, 4, 2, 'V'),
            Vehicle('B', 3, 2, 2, 'H'), Vehicle('C', 4, 4, 2, 'H'),
            Vehicle('E', 1, 0, 2, 'V')
        ],
        "partial_view": [
            Vehicle('X', 2, 1, 2, 'H', is_target=True),
            Vehicle('A', 0, 3, 3, 'V')
        ],
        "belief_starts": [
            [
                Vehicle('X', 2, 1, 2, 'H', is_target=True),
                Vehicle('A', 0, 3, 3, 'V'), 
                Vehicle('D', 1, 4, 2, 'V'),
                Vehicle('B', 3, 2, 2, 'H'),
                Vehicle('C', 4, 4, 2, 'H'),
                Vehicle('E', 1, 0, 2, 'V')
            ],
            [
                Vehicle('X', 2, 1, 2, 'H', is_target=True),
                Vehicle('A', 0, 3, 3, 'V'), 
                Vehicle('D', 1, 4, 2, 'V'),
                Vehicle('B', 3, 3, 2, 'H'),
                Vehicle('C', 4, 4, 2, 'H'),
                Vehicle('E', 1, 0, 2, 'V')
            ]
        ],
        "algorithms": {
            "BGS": {"label": "Blind-Goal Search", "desc": "Tìm kiếm đích mù (Belief-Goal).\nGiải quyết bài toán khi không có thông tin hoàn hảo.", "solver": BeliefGoalSolver()}, 
            "PSS": {"label": "Partial-Start Search", "desc": "Tìm kiếm bắt đầu một phần.\nXử lý không gian trạng thái với khởi đầu không chắc chắn.", "solver": PartialStartSolver()}, 
            "AOG": {"label": "And-Or-Graph Search", "desc": "Duyệt đồ thị AND-OR.\nTìm lời giải dự phòng cho môi trường không tất định.", "solver": AndOrGraphSolver()} 
        }
    },
    5: {
        "name": "Arrange Time",
        "bricks": [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)
        ], 
        "vehicles": [
            Vehicle('X', 2, 0, 2, 'H', is_target=True),
            Vehicle('A', -1, -1, 3, 'H'), 
            Vehicle('B', -1, -1, 3, 'H'), 
            Vehicle('C', -1, -1, 3, 'H'), 
            Vehicle('D', -1, -1, 3, 'V'),
            Vehicle('E', -1, -1, 3, 'V'),
            Vehicle('F', -1, -1, 3, 'V')
        ],
        "algorithms": {
            "BT": {"label": "Backtracking", "desc": "Quay lui (CSP).\nThử gán giá trị, nếu vi phạm ràng buộc thì quay lại.", "solver": BacktrackingSolver()},
            "FC": {"label": "Forward Checking", "desc": "Kiểm tra tiến.\nLoại bỏ các giá trị vi phạm ràng buộc ngay khi gán.", "solver": ForwardCheckingSolver()}, 
            "MC": {"label": "Min Conflict", "desc": "Tối thiểu xung đột.\nSửa đổi trạng thái để giảm số lượng ràng buộc bị vi phạm.", "solver": MinConflictsSolver()} 
        }
    },
    6: {
        "name": "The Great Escape",
        "bricks": [(0, 0)], # Một cục gạch trang trí ở góc
        "vehicles": [
            # --- PHE MAX (Mục tiêu tẩu thoát) ---
            Vehicle('X', 2, 1, 2, 'H', is_target=True), 
            Vehicle('B', 5, 0, 2, 'H'), # Xe đồng minh (chạy loăng quăng cho vui)
            
            # --- PHE MIN (Cảnh sát rượt đuổi) ---
            Vehicle('C', 4, 5, 2, 'V'), # Xe cảnh sát đang nằm chờ ở dưới
            Vehicle('D', 0, 2, 2, 'H'), # Xe cảnh sát tuần tra ở trên
            
            # --- XE TRUNG LẬP (Bia đỡ đạn) ---
            Vehicle('F', 3, 4, 2, 'H')  # Xe dân sự đang vô tình chắn đường xe cảnh sát C
        ],
        "algorithms": {
            "MM": {"label": "Minimax", "desc": "Minimax không cắt tỉa.", "solver": MinimaxSolver()},
            "AB": {"label": "Alpha-Beta", "desc": "Minimax có cắt tỉa Alpha-Beta.", "solver": AlphaBetaSolver()},
            "EX": {"label": "Expectimax", "desc": "Đối thủ hành động ngẫu nhiên theo xác suất.", "solver": ExpectimaxSolver()}
        }
    }
}