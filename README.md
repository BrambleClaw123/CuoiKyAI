# 🚗 Rush Hour AI System

**Rush Hour AI System** là một hệ thống mô phỏng Trí tuệ Nhân tạo (AI) được xây dựng bằng Python và Pygame. Dự án này mô hình hóa trò chơi giải đố kinh điển "Rush Hour" (Giờ cao điểm) thành một bài toán Không gian trạng thái (State Space) và sử dụng các thuật toán tìm kiếm để tự động tìm ra đường thoát ngắn nhất cho chiếc xe mục tiêu.

## ✨ Tính năng nổi bật

* **Động cơ AI mạnh mẽ:** Cốt lõi hệ thống hiện tại sử dụng thuật toán **Breadth-First Search (BFS)** để quét hàng vạn trạng thái, đảm bảo tìm ra lời giải với số bước đi ngắn nhất (Optimal Path) hoặc phát hiện chính xác các bản đồ bị khóa chết (Deadlock).
* **Giao diện Đồ họa Chuyên nghiệp:** * Thiết kế Dark Theme hiện đại chia thành 2 Panel độc lập (Sa bàn và Bảng điều khiển).
    * Hệ thống Menu tích hợp đồ họa bóng bẩy, chia nhóm thuật toán rõ ràng.
    * Sàn xe lót vân đường nhựa (Tile mapping) cùng hiệu ứng đổ bóng (Drop shadow) cho xe nổi khối 3D.
* **Đồ họa Xe Động (Dynamic Sprites):** Hỗ trợ tự động nhận diện và vẽ các loại xe có độ dài từ 2 đến 6 ô. Các biến thể xe được chọn ngẫu nhiên (Random Variants) giúp sa bàn sinh động.
* **Trải nghiệm Người dùng (UX):** Có hệ thống Scroll log (cuộn lịch sử di chuyển) bằng chuột/phím, hiển thị tiến độ tính toán theo thời gian thực để không bị "đơ" màn hình.
* **Cấu trúc Mở rộng (Scalable):** Thiết kế theo mô hình OOP, dễ dàng cắm (plug-in) thêm các bản đồ mới thông qua file JSON hoặc tích hợp các thuật toán AI mới (A*, DFS, Genetic...) mà không ảnh hưởng tới Core Game.

## 📂 Cấu trúc dự án

```text
rush_hour_ai/
│
├── algorithms/              # Chứa các module thuật toán AI
│   ├── base_solver.py       # Class trừu tượng cho mọi thuật toán
│   └── uninformed/
│       └── bfs.py           # Thuật toán Tìm kiếm theo chiều rộng (BFS)
│
├── assets/                  # Tài nguyên đồ họa
│   └── images/              # Logo, sprite xe (car/truck), nền sàn (board_bg)
│
├── core/                    # Lõi logic của game
│   ├── constants.py         # Kích thước, bảng màu, thông số hệ thống
│   ├── game_state.py        # Định nghĩa class Vehicle và GameState (Luật chơi)
│   └── level_loader.py      # Trình đọc map từ file JSON
│
├── levels/                  # Thư viện lưu trữ bản đồ
│   └── level_01.json        # Bản đồ cấp độ 1
│
├── ui/                      # Giao diện người dùng
│   ├── components.py        # Các component dùng chung (Nút bấm, Panel)
│   ├── game_window.py       # Render sa bàn và animation xe chạy
│   └── menu_window.py       # Render màn hình Menu chính
│
├── main.py                  # File khởi chạy toàn bộ hệ thống
└── README.md                # Tài liệu dự án
