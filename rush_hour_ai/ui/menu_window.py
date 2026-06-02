import os
import pygame
from core.constants import *
from ui.components import Button

def run_menu(screen, clock):
    buttons = []
    cols = 3
    
    # 1. THU GỌN CHIỀU CAO VÀ KHOẢNG CÁCH NÚT
    btn_w, btn_h = 220, 50         # Giảm chiều cao từ 55 xuống 50
    padding_x, padding_y = 30, 15  # Giảm khoảng cách dọc từ 20 xuống 15
    
    total_w = cols * btn_w + (cols - 1) * padding_x
    start_x = (WINDOW_WIDTH - total_w) // 2
    
    # 2. ĐẨY GRID NÚT BẤM LÊN CAO HƠN (Y=270)
    start_y = 270 

    GROUP_COLORS = {
        "Uninformed": (46, 134, 193), 
        "Informed": (39, 174, 96),    
        "Local": (211, 84, 0),        
        "Locked": (70, 75, 80)  
    }

    for i in range(18):
        row = i // cols
        col = i % cols
        x = start_x + col * (btn_w + padding_x)
        y = start_y + row * (btn_h + padding_y)
        
        level_num = i + 1
        
        if level_num <= 3:
            algo, group = ["BFS", "DFS", "IDS"][level_num-1], "Uninformed"
        elif level_num <= 6:
            algo, group = ["Greedy", "A*", "IDA*"][level_num-4], "Informed"
        elif level_num <= 9:
            algo, group = ["Hill", "Sim. Anneal", "Genetic"][level_num-7], "Local"
        else:
            algo, group = "Locked", "Locked" 

        config = {"level": level_num, "algo": algo}
        bg_color = GROUP_COLORS.get(group, (100, 100, 100))
        
        btn = Button(x, y, btn_w, btn_h, f"Lv {level_num}: {algo}", config, bg_color)
        buttons.append(btn)

    # --- TẢI ẢNH LOGO ---
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_dir, "assets", "images", "game_logo.png")
    logo_img = None
    
    if os.path.exists(logo_path):
        raw_logo = pygame.image.load(logo_path).convert_alpha()
        w, h = raw_logo.get_size()
        new_w = 160
        new_h = int(h * (new_w / w))
        logo_img = pygame.transform.smoothscale(raw_logo, (new_w, new_h))

    font_title = pygame.font.SysFont("segoe ui", 46, bold=True)
    font_sub = pygame.font.SysFont("segoe ui", 20, italic=True)

    running = True
    while running:
        screen.fill(APP_BG)
        
        # --- ĐẨY CÁC THÀNH PHẦN PHÍA TRÊN LÊN CAO ---
        
        # 1. Vẽ Logo (Center Y = 85)
        if logo_img:
            logo_rect = logo_img.get_rect(center=(WINDOW_WIDTH // 2, 85))
            screen.blit(logo_img, logo_rect)

        # 2. Vẽ Tiêu đề (Center Y = 180)
        title_text = "RUSH HOUR GAME"
        title_shadow = font_title.render(title_text, True, (0, 0, 0))
        title_surf = font_title.render(title_text, True, (255, 215, 0)) 
        
        screen.blit(title_shadow, (WINDOW_WIDTH//2 - title_shadow.get_width()//2 + 3, 183))
        screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 180))

        

        # 4. Bắt sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            for btn in buttons:
                if "Locked" not in btn.text:
                    selected_config = btn.handle_event(event)
                    if selected_config:
                        return selected_config
        
        # 5. Vẽ lưới nút bấm
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)