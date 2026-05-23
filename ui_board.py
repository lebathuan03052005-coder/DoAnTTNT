import pygame
import sys

# --- MÀU SẮC (khớp toàn bộ dự án) ---
WIDTH, HEIGHT  = 600, 600
BG_COLOR       = (245, 245, 220)   # Nền vàng nhạt
LINE_COLOR     = (80,  80,  70)    # Đường kẻ bàn cờ
LINE_COLOR_LIGHT = (210, 208, 190) # Đường kẻ mờ (nền)
X_COLOR        = (200, 50,  50)    # Quân X — đỏ
O_COLOR        = (50,  150, 200)   # Quân O — xanh
LINE_WIDTH     = 3
OVERLAY_COLOR  = (20,  20,  20)    # Nền mờ game over
WIN_LINE_COLOR = (255, 220, 50)    # Đường thắng — vàng


def get_viet_font():
    """Tự động chọn font hỗ trợ tiếng Việt trên mọi hệ điều hành."""
    priority = [
        "segoeui",        # Windows 10/11
        "arial",          # Windows cũ / macOS
        "tahoma",         # Windows fallback
        "helveticaneue",  # macOS
        "dejavusans",     # Linux
        "freesans",       # Linux
        "liberationsans", # Linux
    ]
    available = pygame.font.get_fonts()
    return next((f for f in priority if f in available), None)


def draw_board(screen, size):
    """
    Vẽ lưới bàn cờ động — tự co giãn theo size.
    :param screen: pygame.Surface
    :param size: 3 hoặc 5
    """
    screen.fill(BG_COLOR)
    cell = WIDTH // size

    # Lưới trang trí mờ phía sau (giống ui_menu)
    for x in range(0, WIDTH + cell, cell):
        pygame.draw.line(screen, LINE_COLOR_LIGHT, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT + cell, cell):
        pygame.draw.line(screen, LINE_COLOR_LIGHT, (0, y), (WIDTH, y), 1)

    # Đường kẻ chính của bàn cờ
    for i in range(1, size):
        pygame.draw.line(screen, LINE_COLOR,
                         (0,       i * cell), (WIDTH,  i * cell), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR,
                         (i * cell, 0),       (i * cell, HEIGHT), LINE_WIDTH)

    # Viền ngoài bàn cờ
    pygame.draw.rect(screen, LINE_COLOR, (0, 0, WIDTH, HEIGHT), LINE_WIDTH)


def draw_piece(screen, row, col, piece_type, size):
    """
    Vẽ quân X hoặc O tự động co giãn theo kích thước ô.
    :param screen:     pygame.Surface
    :param row, col:   vị trí ô (0-indexed)
    :param piece_type: 'X' hoặc 'O'
    :param size:       3 hoặc 5
    """
    cell    = WIDTH // size
    cx      = col * cell + cell // 2
    cy      = row * cell + cell // 2
    padding = cell // 5          # padding nhỏ hơn cũ → quân to hơn, dễ nhìn

    if piece_type == 'O':
        radius = cell // 2 - padding
        # Bóng nhẹ
        pygame.draw.circle(screen, (180, 210, 230),
                           (cx + 2, cy + 2), radius, LINE_WIDTH + 2)
        # Vòng tròn chính
        pygame.draw.circle(screen, O_COLOR,
                           (cx, cy), radius, LINE_WIDTH + 2)

    elif piece_type == 'X':
        offset = cell // 2 - padding
        # Bóng nhẹ
        pygame.draw.line(screen, (220, 170, 170),
                         (cx - offset + 2, cy - offset + 2),
                         (cx + offset + 2, cy + offset + 2), LINE_WIDTH + 3)
        pygame.draw.line(screen, (220, 170, 170),
                         (cx - offset + 2, cy + offset + 2),
                         (cx + offset + 2, cy - offset + 2), LINE_WIDTH + 3)
        # Hai nét chéo chính
        pygame.draw.line(screen, X_COLOR,
                         (cx - offset, cy - offset),
                         (cx + offset, cy + offset), LINE_WIDTH + 3)
        pygame.draw.line(screen, X_COLOR,
                         (cx - offset, cy + offset),
                         (cx + offset, cy - offset), LINE_WIDTH + 3)


def draw_win_line(screen, start_rc, end_rc, size):
    """
    Vẽ đường gạch ngang qua chuỗi thắng.
    :param start_rc: (row, col) ô đầu chuỗi thắng
    :param end_rc:   (row, col) ô cuối chuỗi thắng
    :param size:     kích thước bàn cờ
    """
    cell = WIDTH // size
    x1   = start_rc[1] * cell + cell // 2
    y1   = start_rc[0] * cell + cell // 2
    x2   = end_rc[1]   * cell + cell // 2
    y2   = end_rc[0]   * cell + cell // 2
    pygame.draw.line(screen, WIN_LINE_COLOR, (x1, y1), (x2, y2), LINE_WIDTH + 4)


def draw_game_over(screen, thong_bao):
    """
    Vẽ overlay màn hình kết thúc (đẹp hơn với tag badge).
    :param screen:    pygame.Surface
    :param thong_bao: 'X THẮNG!', 'O THẮNG!', 'HÒA!'
    """
    FONT = get_viet_font()

    # Lớp phủ mờ
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 20, 190))
    screen.blit(overlay, (0, 0))

    # Hộp thông báo bo góc
    box_w, box_h = 420, 200
    box_x = WIDTH  // 2 - box_w // 2
    box_y = HEIGHT // 2 - box_h // 2
    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

    # Xác định màu theo kết quả
    if "X" in thong_bao:
        accent = X_COLOR
        tag_bg = (255, 235, 235)
        tag_text_color = X_COLOR
        tag_label = "CHIẾN THẮNG"
    elif "O" in thong_bao:
        accent = O_COLOR
        tag_bg = (235, 245, 255)
        tag_text_color = O_COLOR
        tag_label = "CHIẾN THẮNG"
    else:
        accent = (180, 160, 100)  # Vàng nâu cho HÒA
        tag_bg = (255, 250, 200)
        tag_text_color = (180, 160, 100)
        tag_label = "HÒA NHÂN CẢ"

    # Nền hộp chính
    pygame.draw.rect(screen, (245, 245, 220), box_rect, border_radius=18)
    pygame.draw.rect(screen, accent, box_rect, 4, border_radius=18)

    # Dải màu gradient trên đầu hộp
    top_bar = pygame.Rect(box_x, box_y, box_w, 8)
    pygame.draw.rect(screen, accent, top_bar, border_radius=18)

    # Tag badge nhỏ
    tag_rect = pygame.Rect(box_x + 16, box_y - 18, 140, 32)
    pygame.draw.rect(screen, tag_bg, tag_rect, border_radius=10)
    pygame.draw.rect(screen, tag_text_color, tag_rect, 2, border_radius=10)
    font_tag = pygame.font.SysFont(FONT, 14, bold=True)
    tag_surf = font_tag.render(tag_label, True, tag_text_color)
    screen.blit(tag_surf, tag_surf.get_rect(center=tag_rect.center))

    # Chữ thông báo lớn
    font_big = pygame.font.SysFont(FONT, 56, bold=True)
    text_surf = font_big.render(thong_bao, True, accent)
    screen.blit(text_surf, text_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 20)))

    # Dòng mô tả
    font_desc = pygame.font.SysFont(FONT, 15)
    if "X" in thong_bao:
        desc = "Bạn thắng rồi! 🎉"
    elif "O" in thong_bao:
        desc = "Máy tính thắng! 🤖"
    else:
        desc = "Cân bằng giữa hai bên! ⚖️"
    desc_surf = font_desc.render(desc, True, (100, 100, 100))
    screen.blit(desc_surf, desc_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 22)))

    # Dòng hướng dẫn nhỏ
    font_sub = pygame.font.SysFont(FONT, 15)
    sub_surf = font_sub.render(
        "Nhấn  SPACE  để chơi lại  —  ESC  để về Menu",
        True, (120, 120, 100))
    screen.blit(sub_surf, sub_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 65)))

    pygame.display.update()


# ── Chạy thử độc lập ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Caro AI — UI Board Test")

    BOARD_SIZE = 5   # Đổi thành 3 để test bàn 3x3

    draw_board(screen, BOARD_SIZE)

    # Vài quân cờ mẫu
    draw_piece(screen, 0, 0, 'X', BOARD_SIZE)
    draw_piece(screen, 1, 1, 'O', BOARD_SIZE)
    draw_piece(screen, 2, 2, 'X', BOARD_SIZE)
    draw_piece(screen, 3, 3, 'O', BOARD_SIZE)
    draw_piece(screen, 4, 4, 'X', BOARD_SIZE)

    # Đường thắng mẫu (chéo chính)
    draw_win_line(screen, (0, 0), (4, 4), BOARD_SIZE)

    pygame.display.update()

    # Đợi 1.5 giây rồi hiện game over
    pygame.time.delay(1500)
    draw_game_over(screen, "X THẮNG!")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    # Test: vẽ lại bàn cờ mới
                    draw_board(screen, BOARD_SIZE)
                    draw_piece(screen, 2, 1, 'O', BOARD_SIZE)
                    draw_piece(screen, 2, 2, 'O', BOARD_SIZE)
                    draw_piece(screen, 2, 3, 'O', BOARD_SIZE)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    draw_game_over(screen, "HÒA!")

    pygame.quit()
    sys.exit()
