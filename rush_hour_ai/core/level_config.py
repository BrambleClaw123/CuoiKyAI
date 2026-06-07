from core.vehicle import Vehicle
from algorithms.bfs_solver import BFSSolver
from algorithms.dfs_solver import DFSSolver
from algorithms.ids_solver import IDSSolver
# from algorithms.dfs_solver import DFSSolver
# from algorithms.ids_solver import IDSSolver

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
    'X': {"bg": "#7F1D1D", "border": "#EF4444", "text": "#FCA5A5"}, 
    'A': {"bg": "#1E293B", "border": "#3B82F6", "text": "#93C5FD"},
    'B': {"bg": "#3B0764", "border": "#A855F7", "text": "#D8B4FE"},
    'C': {"bg": "#042F2E", "border": "#14B8A6", "text": "#5EEAD4"},
    'D': {"bg": "#451A03", "border": "#F59E0B", "text": "#FCD34D"},
    'E': {"bg": "#500732", "border": "#EC4899", "text": "#F9A8D4"},
    'F': {"bg": "#022C22", "border": "#10B981", "text": "#6EE7B7"},
    'G': {"bg": "#431407", "border": "#F97316", "text": "#FDBA74"},
    'H': {"bg": "#1A1B4B", "border": "#6366F1", "text": "#A5B4FC"},
    'I': {"bg": "#422006", "border": "#EAB308", "text": "#FDE047"}
}

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
            "GSA": {"label": "Greedy Search Algorithm", "desc": "Duyệt theo hàm heuristic đánh giá.\nTập trung hướng đích, nhanh kịch bản.", "solver": BFSSolver()}, 
            "A*":  {"label": "A* Algorithm", "desc": "Kết hợp chi phí thực tế và heuristic.\nTìm đường ngắn nhất tối ưu tuyệt đối.", "solver": BFSSolver()}, 
            "IDA*": {"label": "Iterative Deepening A*", "desc": "Phiên bản IDA* tiết kiệm bộ nhớ.\nDùng giới hạn chi phí tăng dần.", "solver": BFSSolver()}  
        }
    }
}