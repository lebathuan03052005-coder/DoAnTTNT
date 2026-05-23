# Hướng dẫn cài đặt & chạy Caro AI

## 1. Yêu cầu hệ thống

- **Windows / macOS / Linux**
- **Python 3.8 hoặc cao hơn**
- **pip** (quản lý gói Python)

## 2. Cài đặt Python

Nếu chưa cài Python:

- Tải từ [python.org](https://www.python.org/downloads/)
- Đảm bảo tick **"Add Python to PATH"** khi cài
- Kiểm tra: Mở terminal/cmd gõ `python --version`

## 3. Cài đặt Pygame

Mở terminal/PowerShell và chạy:

```bash
pip install pygame
```

Hoặc cài từ file `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 4. Chạy trò chơi

```bash
python main.py
```

## 5. Cách chơi

- **Menu**: Chọn 3×3 hoặc 5×5
- **Chơi**: Bấm chuột vào ô trống
- **Thắng**: 3 quân (3×3) hoặc 4 quân (5×5) liên tiếp
- **Phím tắt**:
  - `SPACE`: Chơi lại
  - `ESC`: Quay lại menu

## 6. Khắc phục sự cố

### Lỗi: `ModuleNotFoundError: No module named 'pygame'`

→ Cài pygame: `pip install pygame`

### Lỗi: `No module named 'ai_5x5'`

→ Kiểm tra file `ai_5x5.py` có trong thư mục không?
→ Đảm bảo đang chạy từ thư mục đúng: `cd doan_AL`

### Pygame không hoạt động

→ Cài lại: `pip uninstall pygame && pip install pygame`

### Chữ Việt không hiển thị

→ Không liên quan cài đặt (do hệ thống font)
→ Pygame tự chọn font hỗ trợ

## 7. Cấu trúc file cần có

```
doan_AL/
├── main.py         ✓ (chạy file này)
├── logic.py        ✓
├── ai_3x3.py       ✓
├── ai_5x5.py       ✓
├── heuristic.py    ✓
├── ui_menu.py      ✓
├── ui_board.py     ✓
├── requirements.txt ✓
└── .gitignore      (tùy chọn)
```

Tất cả các file trên phải có trong cùng thư mục!

## 8. Chạy trên IDE (VS Code / PyCharm)

### VS Code

1. Cài extension **Python**
2. Mở folder `doan_AL`
3. Bấm F5 hoặc `Ctrl+F5` để chạy

### PyCharm

1. File → Open → Chọn folder `doan_AL`
2. Right-click `main.py` → **Run 'main'**

---
