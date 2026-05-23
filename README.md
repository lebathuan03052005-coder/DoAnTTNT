# Caro AI – Trò Chơi Caro vs Máy Tính

Một trò chơi Caro (Tic-Tac-Toe mở rộng) tương tác với giao diện đồ họa Pygame. Người chơi có thể chơi trên bàn **3×3** hoặc **5×5** chống lại AI.

## 📋 Yêu cầu

- **Python 3.8+**
- **Pygame 2.1.0+**

## 🚀 Cài đặt

1. Clone hoặc tải xuống dự án:

```bash
git clone <repository-url>
cd doan_AL
```

2. Cài đặt các thư viện phụ thuộc:

```bash
pip install -r requirements.txt
```

## 🎮 Cách chơi

1. Chạy chương trình chính:

```bash
python main.py
```

2. Một cửa sổ menu sẽ xuất hiện cho phép bạn chọn:
   - **3×3**: Bàn cờ 3×3 (3 quân liên tiếp thắng)
   - **5×5**: Bàn cờ 5×5 (4 quân liên tiếp thắng)

3. Bạn chơi với quân **X** (đỏ), AI chơi với quân **O** (xanh)

4. **Điều khiển**:
   - **Chuột**: Bấm vào ô trống để đặt quân
   - **SPACE**: Chơi lại (khi trò chơi kết thúc)
   - **ESC**: Quay lại menu

## 📁 Cấu trúc dự án

```
doan_AL/
├── main.py              # Điểm khởi động (vòng lặp chính)
├── logic.py             # Logic trò chơi (xử lý nước đi, kiểm tra thắng)
├── ai_3x3.py            # AI cho bàn 3×3 (Minimax)
├── ai_5x5.py            # AI cho bàn 5×5 (Alpha-Beta Pruning)
├── heuristic.py         # Hàm đánh giá heuristic cho 5×5
├── ui_menu.py           # Giao diện menu chọn chế độ
├── ui_board.py          # Giao diện vẽ bàn cờ và quân cờ
├── test.py              # File kiểm tra/demo
├── requirements.txt     # Danh sách thư viện phụ thuộc
├── .gitignore           # File ignore cho Git
└── README.md            # File này
```

## 🤖 Chi tiết AI

### Bàn 3×3

- **Thuật toán**: Minimax với Alpha-Beta Pruning
- **Chiến lược**: AI không bao giờ thua trên bàn 3×3
- **File**: `ai_3x3.py`

### Bàn 5×5

- **Thuật toán**: Alpha-Beta Pruning
- **Heuristic**: Đánh giá dựa trên độ dài chuỗi và số đầu thoáng
- **Độ sâu tìm kiếm**: 4 lớp (tối ưu hóa cho hiệu suất)
- **File**: `ai_5x5.py`, `heuristic.py`

## 🎨 Giao diện

- **Menu**: Chọn kích thước bàn cờ
- **Bàn cờ**: Hiển thị quân X (đỏ) và O (xanh) với lưới động
- **Thắng**: Vẽ đường vàng qua chuỗi quân thắng
- **Game Over**: Thông báo kết quả (Thắng/Thua/Hòa)

## 🔧 Tùy chỉnh

Bạn có thể tùy chỉnh các hằng số trong các file:

- **Kích thước cửa sổ**: `ui_board.py` → `WIDTH`, `HEIGHT`
- **Màu sắc**: `ui_board.py`, `ui_menu.py`
- **Độ sâu tìm kiếm AI**: `ai_5x5.py` → hàm `get_ai_move()`

## 👥 Thành viên dự án

- **Người 1 (Đăng)**: UI Menu & Board (`ui_menu.py`, `ui_board.py`)
- **Người 2 (Trần Cao Nguyên)**: Logic & Heuristic (`logic.py`, `heuristic.py`)
- **Người 3 (Thuần)**: AI (`ai_3x3.py`, `ai_5x5.py`)

## 📝 Ghi chú

- Trò chơi sử dụng font `DejaVuSans` để hỗ trợ tiếng Việt tốt nhất
- Nếu font không tìm thấy, Pygame sẽ tự chọn font thay thế
- Mã nguồn được viết bằng tiếng Việt để dễ hiểu

## 🐛 Xử lý sự cố

**Lỗi: "ModuleNotFoundError: No module named 'pygame'"**
→ Cài đặt pygame: `pip install pygame`

**Lỗi: "ModuleNotFoundError: No module named 'ai_5x5'"**
→ File `ai_5x5.py` thiếu hoặc không ở đúng thư mục

**Chữ tiếng Việt không hiển thị đúng**
→ Đảm bảo có font hỗ trợ (DejaVuSans, Segoe UI, Arial)

## 📄 Giấy phép

Dự án này là phần của bài tập lập trình nhóm.
