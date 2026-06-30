# 🚗 Rush Hour Puzzle - Đồ Án Cuối Kỳ Trí Tuệ Nhân Tạo

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/UI-CustomTkinter-brightgreen" alt="UI Framework">
  <img src="https://img.shields.io/badge/Course-Artificial_Intelligence-orange" alt="Course">
</p>

Dự án này là đồ án cuối kỳ môn **Trí tuệ nhân tạo**. Mục tiêu của dự án là xây dựng một môi trường mô phỏng trò chơi giải đố **Rush Hour** (Giờ cao điểm) và cài đặt đa dạng các thuật toán Trí tuệ nhân tạo để giải quyết các bài toán khác nhau trên môi trường này.

## 🎓 Thông tin nhóm thực hiện

| STT | Họ và tên | MSSV |
|:---:|:---|:---:|
| 1 | **Huỳnh Phạm Hoàng Kha** | 24110237 |
| 2 | **Phạm Vĩ Cận** | 24110169 |
| 3 | **Huỳnh Quảng Tín** | 24110353 |

## 📁 Cấu trúc thư mục (Project Structure)

```text
rush_hour_ai/
├── algorithms/
│   ├── adversarial_search_problem/
│   │   ├── alphabeta_solver.py
│   │   ├── expectimax_solver.py
│   │   └── minimax_solver.py
│   ├── constraint_satisfaction_problem/
│   │   ├── backtracking_solver.py   
│   │   ├── forward_checking.py
│   │   └── min_conflict_solver.py
│   ├── informed_search_algorithm/
│   │   ├── a_star_solver.py
│   │   ├── gsa_solver.py
│   │   └── ida_star.py
│   ├── local_search_algorithm/
│   │   ├── lbs_solver.py
│   │   ├── shc_solver.py
│   │   └── stimulated_annealing_solver.py
│   ├── search_in_complex_environment/
│   │   ├── and_or_graph.py
│   │   ├── belief_goal_solver.py
│   │   └── partial_start_solver.py
│   ├── uninformed_search_algorithm/
│   │   ├── bfs_solver.py
│   │   ├── dfs_solver.py
│   │   └── ids_solver.py
│   ├── base_solver.py
│   └── search_framework.py
├── core/
│   ├── board.py
│   ├── level_config.py
│   └── vehicle.py
├── ui/
│   └── app_window.py
├── main.py
└── README.md
```


---

## 🌟 Tính năng 

<p align="center">
  <img src="https://github.com/user-attachments/assets/a83f01ba-d7b7-483a-b395-73272be10961" alt="Giao diện chính" width="800">
  <br>
  <i>Giao diện chính của ứng dụng với chế độ Dark Mode hiện đại</i>
</p>

- **Giao diện trực quan (GUI):** Xây dựng bằng `CustomTkinter`. Hỗ trợ kéo thả xe thủ công (Interactive play).
- **Mô phỏng đa dạng kịch bản (6 Levels):** Từ giải đố thoát hiểm thông thường, sắp xếp xe có điều kiện, đến môi trường đối kháng (Cảnh sát bắt cướp).
- **Trực quan hóa thuật toán:** Theo dõi log di chuyển từng bước, hiển thị số trạng thái đã duyệt (Visited states).
- **So sánh thuật toán:** Chuyển đổi linh hoạt giữa các thuật toán trong cùng một Level để so sánh hiệu năng.

---

## 🧠 Các thuật toán AI được cài đặt

Dự án bao phủ toàn diện các chủ đề trong môn học AI, được chia thành 6 Levels tương ứng:

### 1. Tìm kiếm mù (Uninformed Search) - *Level 1*
<p align="center">
  <img src="https://github.com/user-attachments/assets/9fe4b88c-e90f-405c-85eb-8b0cd08e6f28" alt="Thuật toán BFS" width="500">
  <br>
  <i>Minh họa thuật toán BFS</i>
</p>

- **BFS (Breadth-First Search):** Đảm bảo tìm được đường đi ngắn nhất, nhưng tốn bộ nhớ.
- **DFS (Depth-First Search):** Tiết kiệm bộ nhớ, nhưng không đảm bảo đường đi tối ưu.
- **IDS (Iterative Deepening Search):** Kết hợp ưu điểm về bộ nhớ của DFS và tính tối ưu của BFS.

### 2. Tìm kiếm có thông tin (Informed Search) - *Level 2*
<p align="center">
  <img src="https://github.com/user-attachments/assets/0029a6c9-6d8c-42ed-873d-e557c9a42f53" alt="Thuật toán A*" width="500">
  <br>
  <i>Minh họa thuật toán A*</i>
</p>

- **GSA (Greedy Search Algorithm):** Ưu tiên mở rộng trạng thái gần đích nhất theo hàm Heuristic, tốc độ duyệt nhanh nhưng không đảm bảo đường đi tối ưu.
- **A* (A-Star):** Kết hợp chi phí thực tế $g(n)$ và hàm Heuristic $h(n)$, đảm bảo tìm được đường đi ngắn nhất và tối ưu tuyệt đối.
- **IDA* (Iterative Deepening A*):** Là phiên bản biến thể của A*, giới hạn độ sâu duyệt theo một ngưỡng chi phí nhằm tiết kiệm tối đa không gian bộ nhớ.

### 3. Tìm kiếm cục bộ (Local Search) - *Level 3*
<p align="center">
  <img src="https://github.com/user-attachments/assets/cb8a8e56-b07a-4cba-9571-1de73518a862" alt="Thuật toán LBS" width="500">
  <br>
  <i>Minh họa thuật toán LBS</i>
</p>

- **SHC (Stochastic Hill Climbing):** Lựa chọn ngẫu nhiên một trạng thái kề tốt hơn hiện tại để đi tiếp, giúp tránh việc bị kẹt ở mức tối ưu cục bộ.
- **LBS (Local Beam Search):** Duy trì $k$ trạng thái tốt nhất ở mỗi bước đi thay vì chỉ một trạng thái, tăng khả năng tìm thấy giải pháp.
- **SAA (Simulated Annealing):** Thuật toán mô phỏng quá trình luyện kim, chấp nhận các bước đi xấu hơn với xác suất giảm dần theo thời gian để có cơ hội thoát khỏi tối ưu cục bộ.

### 4. Tìm kiếm trong môi trường phức tạp - *Level 4*
<p align="center">
  <img src="https://github.com/user-attachments/assets/4991ac63-5779-415d-93e2-4250697a7591" alt="Môi trường không chắc chắn" width="600">
  <br>
  <i>Minh họa duyệt Partial-Start Search</i>
</p>

- **BGS (Belief-Goal Search):** Tìm kiếm không gian đích dựa trên các tập trạng thái niềm tin (belief states), cụ thể là belief goal khi bài toán không cho phép quan sát toàn bộ môi trường.
- **PSS (Partial-Start Search):** Giải quyết bài toán có môi trường chỉ nhìn thấy 1 phần.
- **AOG (And-Or-Graph):** Duyệt cây đồ thị And-Or nhằm xây dựng các kế hoạch dự phòng cho những hành động mang tính không xác định.

### 5. Thỏa mãn ràng buộc (CSP) - *Level 5 (Sắp xếp xe)*
<p align="center">
  <img src="https://github.com/user-attachments/assets/0553faeb-5029-43af-94a9-f46716d5080d" alt="Môi trường có ràng buộc" width="600">
  <br>
  <i>Minh họa Min Conflict</i>
</p>

- **Backtracking:** Thử gán vị trí cho từng chiếc xe, nếu phát hiện vi phạm ràng buộc (đè lên nhau, đè lên tường) thì lập tức quay lui để thử hướng khác.
- **Forward Checking:** Kiểm tra tiến kết hợp với quay lui, giúp loại bỏ sớm các vị trí chắc chắn gây ra xung đột trong tương lai, thu hẹp không gian tìm kiếm.
- **Min-Conflicts:** Khởi tạo ngẫu nhiên bàn cờ, sau đó liên tục chọn các xe đang bị lỗi và dịch chuyển chúng sao cho số lượng xung đột giảm đi ít nhất có thể.

### 6. Tìm kiếm đối kháng (Adversarial Search) - *Level 6 (Tẩu thoát)*
<p align="center">
  <img src="https://github.com/user-attachments/assets/45c9fdf2-e394-4ad0-b06b-356317878a5e" alt="Cảnh sát rượt đuổi - Minimax" width="600">
  <br>
  <i>Minh họa thuật toán Minimax</i>
</p>

- **Minimax:** Đánh giá các nước đi bằng cách tối đa hóa điểm số của phe mình (MAX) đồng thời giảm thiểu tối đa điểm số của đối thủ (MIN).
- **Alpha-Beta Pruning:** Kỹ thuật cắt tỉa các nhánh vô ích trong cây trò chơi, giúp thuật toán Minimax chạy nhanh và duyệt sâu hơn.
- **Expectimax:** Mô phỏng sự ngẫu nhiên, cho phép tính toán các nước đi khi đối thủ (hoặc môi trường) có những phản ứng không thể đoán trước (Chance nodes).

---

## ⚙️ Cài đặt và Chạy chương trình (Installation & Running)

Làm theo các bước dưới đây để thiết lập và khởi chạy dự án trên máy tính của bạn (hướng dẫn dành riêng cho hệ điều hành Windows):

### Bước 1: Tải dự án (Clone or Download)
Giải nén file `.zip` của dự án vừa tải về vào thư mục mong muốn trên máy tính. Nếu đang sử dụng Git, có thể clone trực tiếp repository này về máy.

### Bước 2: Cài đặt thư viện yêu cầu (Install Required Libraries)
Mở terminal (Command Prompt hoặc PowerShell trên Windows) và điều hướng (`cd`) đến thư mục gốc của dự án. Tiếp theo, hãy cài đặt thư viện giao diện `customtkinter` thông qua `pip` bằng lệnh sau:

```bash
pip install customtkinter
```

### Bước 3: Khởi chạy dự án (Running)
Sau khi các thư viện phụ thuộc đã được cài đặt đầy đủ và cấu trúc thư mục hoàn chỉnh, khởi động chương trình bằng cách chạy file `main.py` hoặc script chính trong terminal bằng dòng lệnh sau:

```bash
python main.py
```

## 🎯 Kết luận và Hướng phát triển (Conclusion & Future Work)

### 1. Tổng kết dự án
Dự án **Rush Hour AI** đã hoàn thành các mục tiêu đề ra trong môn học :
* Mô phỏng thành công môi trường trò chơi Rush Hour với giao diện đồ họa (`customtkinter`) tương tác trực quan.
* Cài đặt và kiểm chứng toàn diện các họ thuật toán cốt lõi của AI: Tìm kiếm mù, Tìm kiếm có thông tin, Tìm kiếm cục bộ, Thỏa mãn ràng buộc (CSP), và Tìm kiếm đối kháng (Adversarial Search).
* So sánh và đánh giá trực quan hiệu suất của các thuật toán thông qua không gian trạng thái (số node đã duyệt) và độ dài đường đi. Dự án làm nổi bật sự ưu việt của các thuật toán sử dụng Heuristic (như A*, GSA) so với các thuật toán quét cạn (BFS, DFS) trong những không gian trạng thái lớn, cũng như cách xử lý linh hoạt của AI trong các môi trường không chắc chắn (Partial-Start, Belief-Goal).

### 2. Hướng phát triển tương lai
Mặc dù hệ thống đã có tính hoàn thiện cao, dự án vẫn mở ra nhiều tiềm năng phát triển trong tương lai:
* **Nghiên cứu Heuristic nâng cao:** Thiết kế và thử nghiệm các hàm Heuristic phức tạp hơn để tối ưu hóa thời gian chạy cho thuật toán A* trên các bàn cờ có kích thước lớn hơn (ví dụ: 8x8 hoặc 10x10).
* **Tích hợp Trình tạo màn chơi (Level Generator):** Xây dựng thuật toán sinh ngẫu nhiên các thế cờ hợp lệ, có độ khó tùy chỉnh để người chơi hoặc AI thử sức.
* **Tiếp cận Học máy (Machine Learning):** Áp dụng Học tăng cường (Reinforcement Learning - Q-Learning/Deep Q-Network) để huấn luyện một Agent có khả năng "tự học" cách giải thoát xe thay vì phụ thuộc vào các thuật toán truyền thống.

---






