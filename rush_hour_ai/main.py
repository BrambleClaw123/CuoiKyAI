import os
import pygame
from core.level_loader import load_level
from core.constants import *
from ui.game_window import draw_board
from ui.menu_window import run_menu

# Import AI
from algorithms.uninformed.bfs import BFS

# Hàm Mapping Thuật toán động
def get_solver(algo_name):
    if algo_name == "BFS":
        return BFS()
    # Sau này thêm DFS: if algo_name == "DFS": return DFS()
    return BFS() # Mặc định trả về BFS nếu chưa làm

def get_move_description(state1, state2):
    """So sánh 2 state để rút ra câu mô tả bước đi"""
    for v1, v2 in zip(state1.vehicles, state2.vehicles):
        if v1.x != v2.x or v1.y != v2.y:
            if v1.orientation == 'H':
                direction = "sang phải" if v2.x > v1.x else "sang trái"
            else:
                direction = "xuống dưới" if v2.y > v1.y else "lên trên"
            return f"Xe {v1.id} -> {direction}"
    return "Không rõ"

def run_game(screen, clock, level_config):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"level_{level_config['level']:02d}.json"
    file_path = os.path.join(base_dir, "levels", filename)
    
    if not os.path.exists(file_path):
        file_path = os.path.join(base_dir, "levels", "level_01.json")

    initial_state = load_level(file_path)
    solver = get_solver(level_config['algo'])

    font_sm = pygame.font.SysFont("segoe ui", 18)
    font_md = pygame.font.SysFont("segoe ui", 22)
    font_lg = pygame.font.SysFont("segoe ui", 26, bold=True)

    game_status = "WAITING" 
    solution_path = []
    move_history_texts = []
    
    current_step = 0
    step_delay = 500
    last_update_time = 0

    # --- BIẾN QUẢN LÝ CUỘN LOG ---
    log_scroll_offset = 0
    max_visible_lines = 14

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # 1. Xử lý cuộn bằng con lăn chuột
            if event.type == pygame.MOUSEWHEEL:
                if game_status in ["ANIMATING", "FINISHED"]:
                    max_offset = max(0, current_step - max_visible_lines)
                    # event.y dương khi cuộn lên, âm khi cuộn xuống
                    log_scroll_offset -= event.y 
                    log_scroll_offset = max(0, min(log_scroll_offset, max_offset))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
                if event.key == pygame.K_SPACE and game_status == "WAITING":
                    game_status = "SOLVING"
                
                # 2. Xử lý cuộn bằng phím mũi tên Lên/Xuống
                if game_status in ["ANIMATING", "FINISHED"]:
                    if event.key == pygame.K_UP:
                        log_scroll_offset = max(0, log_scroll_offset - 1)
                    elif event.key == pygame.K_DOWN:
                        max_offset = max(0, current_step - max_visible_lines)
                        log_scroll_offset = min(max_offset, log_scroll_offset + 1)

        screen.fill(APP_BG)

        # --- PANEL TRÁI ---
        panel_left = pygame.Rect(20, 20, 540, 620)
        pygame.draw.rect(screen, PANEL_BG, panel_left, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, panel_left, width=2, border_radius=12)
        
        board_offset_x = panel_left.x + (panel_left.width - BOARD_SIZE) // 2
        board_offset_y = panel_left.y + (panel_left.height - BOARD_SIZE) // 2

        state_to_draw = initial_state if game_status in ["WAITING", "SOLVING", "NO_SOLUTION"] else solution_path[current_step]
        draw_board(screen, state_to_draw, board_offset_x, board_offset_y)

        # --- PANEL PHẢI ---
        panel_right = pygame.Rect(580, 20, 350, 620)
        pygame.draw.rect(screen, PANEL_BG, panel_right, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, panel_right, width=2, border_radius=12)

        px, py = panel_right.x + 20, panel_right.y + 20
        title_surf = font_lg.render(f"Level {level_config['level']}", True, LIGHT_TEXT)
        algo_surf = font_md.render(f"Thuật toán: {level_config['algo']}", True, (100, 200, 255))
        screen.blit(title_surf, (px, py))
        screen.blit(algo_surf, (px, py + 35))
        pygame.draw.line(screen, BORDER_COLOR, (px, py + 70), (panel_right.right - 20, py + 70), 2)

        if game_status in ["ANIMATING", "FINISHED"]:
            # Hiển thị thêm hướng dẫn cuộn
            step_title = font_md.render(f"Các bước di chuyển: ", True, LIGHT_TEXT)
            screen.blit(step_title, (px, py + 85))
            
            # Render LOG dựa trên thanh cuộn
            start_idx = log_scroll_offset
            end_idx = min(current_step, start_idx + max_visible_lines)
            
            for i in range(start_idx, end_idx):
                color = (255, 215, 0) if i == current_step - 1 else (150, 150, 150)
                txt_surf = font_sm.render(f"Bước {i+1}: {move_history_texts[i]}", True, color)
                # Tính toán lại vị trí Y dựa vào start_idx thay vì index cũ
                screen.blit(txt_surf, (px, py + 120 + (i - start_idx) * 25))

            if game_status == "FINISHED":
                pygame.draw.rect(screen, (30, 80, 30), (px, panel_right.bottom - 70, panel_right.width - 40, 50), border_radius=8)
                summary_txt = font_md.render(f"Đã giải quyết trong {len(solution_path)-1} bước!", True, WHITE)
                screen.blit(summary_txt, (px + 10, panel_right.bottom - 58))

        # --- STATUS BAR BÊN DƯỚI ---
        status_y = WINDOW_HEIGHT - 50
        if game_status == "WAITING":
            status_text = font_lg.render("Nhấn [SPACE] để AI bắt đầu tính toán", True, (0, 200, 100))
        elif game_status == "SOLVING":
            status_text = font_lg.render("AI đang duyệt qua các trạng thái... Vui lòng chờ!", True, (255, 150, 0))
            screen.blit(status_text, (40, status_y))
            pygame.display.flip()
            
            solution_path = solver.solve(initial_state)
            if not solution_path:
                game_status = "NO_SOLUTION"
            else:
                game_status = "ANIMATING"
                last_update_time = pygame.time.get_ticks()
                move_history_texts = [get_move_description(solution_path[i], solution_path[i+1]) for i in range(len(solution_path)-1)]
                status_text = font_lg.render("Đang mô phỏng kết quả...", True, (100, 150, 255))
                
        elif game_status == "ANIMATING":
            status_text = font_lg.render("Đang mô phỏng kết quả...", True, (100, 150, 255))
        elif game_status == "FINISHED":
            status_text = font_lg.render("Hoàn tất! Nhấn [ESC] để quay lại Menu.", True, (0, 200, 100))
        elif game_status == "NO_SOLUTION":
            status_text = font_lg.render("Lỗi: Bản đồ bị khóa chết (Deadlock)!", True, (255, 50, 50))

        if game_status != "SOLVING":
            screen.blit(status_text, (40, status_y))

        # --- LOGIC ANIMATION ---
        if game_status == "ANIMATING":
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > step_delay:
                if current_step < len(solution_path) - 1:
                    current_step += 1
                    # Tự động cuộn xuống dưới cùng khi xe đang chạy
                    log_scroll_offset = max(0, current_step - max_visible_lines)
                else:
                    game_status = "FINISHED"
                last_update_time = current_time

        pygame.display.flip()
        clock.tick(FPS)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"level_{level_config['level']:02d}.json"
    file_path = os.path.join(base_dir, "levels", filename)
    
    if not os.path.exists(file_path):
        file_path = os.path.join(base_dir, "levels", "level_01.json")

    initial_state = load_level(file_path)
    solver = get_solver(level_config['algo'])

    font_sm = pygame.font.SysFont("segoe ui", 18)
    font_md = pygame.font.SysFont("segoe ui", 22)
    font_lg = pygame.font.SysFont("segoe ui", 26, bold=True)

    game_status = "WAITING" 
    solution_path = []
    move_history_texts = []
    
    current_step = 0
    step_delay = 500
    last_update_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
                if event.key == pygame.K_SPACE and game_status == "WAITING":
                    game_status = "SOLVING"

        # --- NỀN TOÀN MÀN HÌNH ---
        screen.fill(APP_BG)

        # --- KHỞI TẠO 2 PANEL ---
        # Panel Trái: Kích thước 540x620, chứa bàn cờ
        panel_left = pygame.Rect(20, 20, 540, 620)
        # Panel Phải: Kích thước 350x620, chứa thông tin và Log
        panel_right = pygame.Rect(580, 20, 350, 620)

        # Vẽ nền và viền cho 2 Panel
        pygame.draw.rect(screen, PANEL_BG, panel_left, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, panel_left, width=2, border_radius=12)
        
        pygame.draw.rect(screen, PANEL_BG, panel_right, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, panel_right, width=2, border_radius=12)

        # --- PANEL TRÁI: SA BÀN GAME ---
        # Tính toán để đẩy bàn cờ vào chính giữa Panel trái
        board_offset_x = panel_left.x + (panel_left.width - BOARD_SIZE) // 2
        board_offset_y = panel_left.y + (panel_left.height - BOARD_SIZE) // 2

        state_to_draw = initial_state if game_status in ["WAITING", "SOLVING", "NO_SOLUTION"] else solution_path[current_step]
        draw_board(screen, state_to_draw, board_offset_x, board_offset_y)

        # --- PANEL PHẢI: THÔNG TIN & LOG ---
        px, py = panel_right.x + 20, panel_right.y + 20
        
        title_surf = font_lg.render(f"Level {level_config['level']}", True, LIGHT_TEXT)
        algo_surf = font_md.render(f"Thuật toán: {level_config['algo']}", True, (100, 200, 255))
        screen.blit(title_surf, (px, py))
        screen.blit(algo_surf, (px, py + 35))
        
        pygame.draw.line(screen, BORDER_COLOR, (px, py + 70), (panel_right.right - 20, py + 70), 2)

        if game_status in ["ANIMATING", "FINISHED"]:
            step_title = font_md.render(f"Lịch sử di chuyển ({current_step}/{len(solution_path)-1})", True, LIGHT_TEXT)
            screen.blit(step_title, (px, py + 85))
            
            # Giới hạn in 14 bước gần nhất
            start_idx = max(0, current_step - 14)
            for i in range(start_idx, current_step):
                color = (255, 215, 0) if i == current_step - 1 else (150, 150, 150)
                txt_surf = font_sm.render(f"Bước {i+1}: {move_history_texts[i]}", True, color)
                screen.blit(txt_surf, (px, py + 120 + (i - start_idx) * 25))

            # NẾU XONG: HIỆN TỔNG HỢP LOG Ở ĐÁY PANEL PHẢI
            if game_status == "FINISHED":
                pygame.draw.rect(screen, (30, 80, 30), (px, panel_right.bottom - 70, panel_right.width - 40, 50), border_radius=8)
                summary_txt = font_md.render(f"Đã giải quyết trong {len(solution_path)-1} bước!", True, WHITE)
                screen.blit(summary_txt, (px + 10, panel_right.bottom - 58))

        # --- THANH TRẠNG THÁI (STATUS BAR) BÊN DƯỚI ---
        status_y = WINDOW_HEIGHT - 50
        
        if game_status == "WAITING":
            status_text = font_lg.render("Nhấn [SPACE] để AI bắt đầu tính toán", True, (0, 200, 100))
        elif game_status == "SOLVING":
            status_text = font_lg.render("AI đang duyệt qua các trạng thái... Vui lòng chờ!", True, (255, 150, 0))
            screen.blit(status_text, (40, status_y))
            pygame.display.flip()
            
            solution_path = solver.solve(initial_state)
            if not solution_path:
                game_status = "NO_SOLUTION"
            else:
                game_status = "ANIMATING"
                last_update_time = pygame.time.get_ticks()
                move_history_texts = [get_move_description(solution_path[i], solution_path[i+1]) for i in range(len(solution_path)-1)]
                status_text = font_lg.render("Đang mô phỏng kết quả...", True, (100, 150, 255))
                
        elif game_status == "ANIMATING":
            status_text = font_lg.render("Đang mô phỏng kết quả...", True, (100, 150, 255))
        elif game_status == "FINISHED":
            status_text = font_lg.render("Hoàn tất! Nhấn [ESC] để quay lại Menu.", True, (0, 200, 100))
        elif game_status == "NO_SOLUTION":
            status_text = font_lg.render("Lỗi: Bản đồ bị khóa chết (Deadlock)!", True, (255, 50, 50))

        if game_status != "SOLVING":
            screen.blit(status_text, (40, status_y))

        # --- LOGIC CHUYỂN CẢNH ---
        if game_status == "ANIMATING":
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > step_delay:
                if current_step < len(solution_path) - 1:
                    current_step += 1
                else:
                    game_status = "FINISHED"
                last_update_time = current_time

        pygame.display.flip()
        clock.tick(FPS)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"level_{level_config['level']:02d}.json"
    file_path = os.path.join(base_dir, "levels", filename)
    
    if not os.path.exists(file_path):
        file_path = os.path.join(base_dir, "levels", "level_01.json")

    initial_state = load_level(file_path)
    solver = get_solver(level_config['algo'])

    # Setup Fonts
    font_sm = pygame.font.SysFont("segoe ui", 18)
    font_md = pygame.font.SysFont("segoe ui", 22)
    font_lg = pygame.font.SysFont("segoe ui", 26, bold=True)

    game_status = "WAITING" 
    solution_path = []
    move_history_texts = [] # Lưu trữ chuỗi text các bước đi
    
    current_step = 0
    step_delay = 500
    last_update_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
                if event.key == pygame.K_SPACE and game_status == "WAITING":
                    game_status = "SOLVING"

        # TÔ MÀU NỀN TOÀN MÀN HÌNH
        screen.fill(WHITE)

        # --- KHU VỰC 1: SA BÀN GAME (Bên trái) ---
        state_to_draw = initial_state if game_status in ["WAITING", "SOLVING", "NO_SOLUTION"] else solution_path[current_step]
        draw_board(screen, state_to_draw)

        # --- KHU VỰC 2: SIDEBAR (Bên phải) ---
        sidebar_rect = pygame.Rect(BOARD_SIZE + 40, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT - 60)
        pygame.draw.rect(screen, DARK_BG, sidebar_rect)
        
        # Tiêu đề Sidebar
        title_surf = font_lg.render(f"Level {level_config['level']}", True, LIGHT_TEXT)
        algo_surf = font_md.render(f"Algo: {level_config['algo']}", True, (100, 200, 255))
        screen.blit(title_surf, (BOARD_SIZE + 60, 20))
        screen.blit(algo_surf, (BOARD_SIZE + 60, 55))
        
        # Đường kẻ ngang
        pygame.draw.line(screen, LIGHT_TEXT, (BOARD_SIZE + 60, 90), (WINDOW_WIDTH - 20, 90), 1)

        # In danh sách các bước đi (Giới hạn hiển thị 15 bước gần nhất để không bị tràn màn hình)
        if game_status in ["ANIMATING", "FINISHED"]:
            step_title = font_md.render(f"Steps: {current_step} / {len(solution_path)-1}", True, LIGHT_TEXT)
            screen.blit(step_title, (BOARD_SIZE + 60, 100))
            
            start_idx = max(0, current_step - 15)
            for i in range(start_idx, current_step):
                # Màu vàng cho bước hiện tại, màu xám cho bước cũ
                color = (255, 215, 0) if i == current_step - 1 else (150, 150, 150)
                txt_surf = font_sm.render(f"{i+1}. {move_history_texts[i]}", True, color)
                screen.blit(txt_surf, (BOARD_SIZE + 60, 140 + (i - start_idx) * 25))

        # --- KHU VỰC 3: THANH TRẠNG THÁI (Bên dưới) ---
        status_rect = pygame.Rect(0, WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60)
        pygame.draw.rect(screen, STATUS_BG, status_rect)

        # Căn chỉnh text ở thanh trạng thái
        if game_status == "WAITING":
            status_text = font_lg.render("Nhấn SPACE để AI bắt đầu giải", True, (0, 120, 0))
        elif game_status == "SOLVING":
            status_text = font_lg.render("Đang suy nghĩ... (Chờ chút nhé)", True, (200, 100, 0))
            
            # Ép render ngay lập tức trước khi AI khóa luồng
            screen.blit(status_text, (20, WINDOW_HEIGHT - 45))
            pygame.display.flip()
            
            solution_path = solver.solve(initial_state)
            if not solution_path:
                game_status = "NO_SOLUTION"
            else:
                game_status = "ANIMATING"
                last_update_time = pygame.time.get_ticks()
                # Dịch toàn bộ các bước ra text một lần
                move_history_texts = [get_move_description(solution_path[i], solution_path[i+1]) for i in range(len(solution_path)-1)]
                status_text = font_lg.render("Đang chạy Animation...", True, (0, 0, 200))
                
        elif game_status == "ANIMATING":
            status_text = font_lg.render("AI đang giải...", True, (0, 0, 200))
        elif game_status == "FINISHED":
            status_text = font_lg.render("Đã giải xong! Nhấn ESC để thoát.", True, (0, 120, 0))
        elif game_status == "NO_SOLUTION":
            status_text = font_lg.render("Bản đồ khóa chết (Deadlock)!", True, (200, 0, 0))

        # In chữ trạng thái bên trái góc dưới
        if game_status != "SOLVING": # Né trường hợp đã in ở trên
            screen.blit(status_text, (20, WINDOW_HEIGHT - 45))

        # In chữ ESC bên phải góc dưới
        esc_surf = font_md.render("ESC: Menu", True, (100, 100, 100))
        screen.blit(esc_surf, (WINDOW_WIDTH - 120, WINDOW_HEIGHT - 40))

        # --- LOGIC CHUYỂN CẢNH ---
        if game_status == "ANIMATING":
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > step_delay:
                if current_step < len(solution_path) - 1:
                    current_step += 1
                else:
                    game_status = "FINISHED"
                last_update_time = current_time

        pygame.display.flip()
        clock.tick(FPS)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"level_{level_config['level']:02d}.json"
    file_path = os.path.join(base_dir, "levels", filename)
    
    # Đề phòng trường hợp chưa tạo file json cho level mới
    if not os.path.exists(file_path):
        print(f"Chưa tạo file {filename}! Tạm thời load level_01.json")
        file_path = os.path.join(base_dir, "levels", "level_01.json")

    initial_state = load_level(file_path)
    solver = get_solver(level_config['algo'])

    font_info = pygame.font.SysFont("segoe ui", 24)
    font_large = pygame.font.SysFont("segoe ui", 18, bold=True)

    # Các biến quản lý trạng thái
    game_status = "WAITING" 
    solution_path = []
    current_step = 0
    step_delay = 500
    last_update_time = 0

    running = True
    while running:
        # --- 1. BẮT SỰ KIỆN ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # Quay lại menu
                
                # Nhấn SPACE để kích hoạt AI nếu đang ở trạng thái chờ
                if event.key == pygame.K_SPACE and game_status == "WAITING":
                    game_status = "SOLVING"

        # --- 2. XỬ LÝ & VẼ GIAO DIỆN THEO TRẠNG THÁI ---
        screen.fill(GRAY)

        if game_status == "WAITING":
            draw_board(screen, initial_state)
            # Vẽ thông báo nhấp nháy hoặc chữ đậm để người dùng biết cần làm gì
            start_text = font_large.render("Nhấn SPACE (Khoảng trắng) để AI bắt đầu giải!", True, (0, 100, 0))
            screen.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, WINDOW_HEIGHT - 65))

        elif game_status == "SOLVING":
            draw_board(screen, initial_state)
            solving_text = font_large.render("AI đang dốc sức suy nghĩ...", True, (200, 100, 0))
            screen.blit(solving_text, (WINDOW_WIDTH//2 - solving_text.get_width()//2, WINDOW_HEIGHT - 65))
            
            # Ép pygame phải vẽ dòng chữ "Đang suy nghĩ" ra màn hình TRƯỚC KHI bị thuật toán làm đứng máy
            pygame.display.flip() 
            
            # Gọi thuật toán AI (Bước này tốn thời gian)
            solution_path = solver.solve(initial_state)
            
            if not solution_path:
                game_status = "NO_SOLUTION"
            else:
                game_status = "ANIMATING"
                last_update_time = pygame.time.get_ticks()

        elif game_status == "ANIMATING" or game_status == "FINISHED":
            # Logic chuyển cảnh animation
            current_time = pygame.time.get_ticks()
            if game_status == "ANIMATING" and current_time - last_update_time > step_delay:
                if current_step < len(solution_path) - 1:
                    current_step += 1
                else:
                    game_status = "FINISHED" # Giải xong rồi thì đứng im
                last_update_time = current_time

            # Vẽ trạng thái từng bước
            draw_board(screen, solution_path[current_step])
            
            # Vẽ thanh thông tin bên dưới
            info_text = f"Level {level_config['level']} - {level_config['algo']} | Step {current_step}/{len(solution_path)-1}"
            info_surf = font_info.render(info_text, True, (0,0,0))
            screen.blit(info_surf, (20, WINDOW_HEIGHT - 35))

        elif game_status == "NO_SOLUTION":
            draw_board(screen, initial_state)
            err_text = font_large.render("Bản đồ khóa chết! Không tìm thấy đường đi.", True, RED)
            screen.blit(err_text, (WINDOW_WIDTH//2 - err_text.get_width()//2, WINDOW_HEIGHT - 65))

        # Nút ESC luôn hiện ở góc dưới bên phải trong mọi trạng thái
        esc_surf = font_info.render("Nhấn ESC để về Menu", True, RED)
        screen.blit(esc_surf, (WINDOW_WIDTH - 240, WINDOW_HEIGHT - 35))

        pygame.display.flip()
        clock.tick(FPS)
    """Vòng lặp chạy màn hình Game AI"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tạm thời bắt mọi level chạy file level_01.json vì ta chưa tạo các file kia
    # Sau này đổi thành: f"level_{level_config['level']:02d}.json"
    file_path = os.path.join(base_dir, "levels", "level_01.json")
    
    initial_state = load_level(file_path)
    solver = get_solver(level_config['algo'])
    
    print(f"Đang chạy Level {level_config['level']} bằng {level_config['algo']}...")
    solution_path = solver.solve(initial_state)

    if not solution_path:
        print("Không tìm thấy đường đi!")
        return # Quay lại menu

    current_step = 0
    step_delay = 500
    last_update_time = pygame.time.get_ticks()
    
    # Font thông báo
    font_info = pygame.font.SysFont("segoe ui", 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Nhấn ESC để quay lại Menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 

        # Logic Animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > step_delay:
            if current_step < len(solution_path) - 1:
                current_step += 1
            last_update_time = current_time

        screen.fill(GRAY)
        
        # Vẽ bàn cờ
        draw_board(screen, solution_path[current_step])
        
        # Vẽ thông tin hướng dẫn
        info_text = f"Level {level_config['level']} - {level_config['algo']} | Step {current_step}/{len(solution_path)-1}"
        info_surf = font_info.render(info_text, True, (0,0,0))
        screen.blit(info_surf, (20, WINDOW_HEIGHT - 35))
        
        esc_surf = font_info.render("Nhấn ESC để về Menu", True, (200, 0, 0))
        screen.blit(esc_surf, (WINDOW_WIDTH - 240, WINDOW_HEIGHT - 35))

        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Rush Hour AI Architecture")
    clock = pygame.time.Clock()

    # Vòng lặp Tổng của toàn bộ ứng dụng
    while True:
        # 1. Chạy màn hình Menu
        selected_level = run_menu(screen, clock)
        
        # Nếu run_menu trả về None (người dùng bấm nút X tắt cửa sổ)
        if selected_level is None:
            break
            
        # 2. Chuyển sang màn hình Game với config vừa lấy được
        run_game(screen, clock, selected_level)

    pygame.quit()

if __name__ == "__main__":
    main()