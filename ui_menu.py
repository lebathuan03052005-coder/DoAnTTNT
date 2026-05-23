import pygame # type: ignore
import sys

# --- MÀU SẮC (khớp với ui_board.py) ---
BG_COLOR      = (245, 245, 220)   # Nền vàng nhạt
TITLE_COLOR   = (50,  50,  50)    # Tiêu đề (đen đậm)
SUBTITLE_COLOR= (100, 100, 100)   # Phụ đề (xám)
BTN_3X3_COLOR = (200, 50,  50)    # Nút 3x3 — đỏ (màu X)
BTN_5X5_COLOR = (50,  150, 200)   # Nút 5x5 — xanh (màu O)
BTN_HOVER_3X3 = (230, 80,  80)    # Hover nút 3x3
BTN_HOVER_5X5 = (80,  180, 230)   # Hover nút 5x5
BTN_TEXT_COLOR= (255, 255, 255)   # Chữ trên nút
BORDER_COLOR  = (50,  50,  50)    # Viền nút
TAG_3X3_COLOR = (255, 235, 235)   # Tag badge 3x3
TAG_5X5_COLOR = (235, 245, 255)   # Tag badge 5x5
TAG_TEXT_3X3  = (200, 50,  50)
TAG_TEXT_5X5  = (50,  150, 200)
DIVIDER_COLOR = (200, 200, 180)   # Đường kẻ phân cách


def draw_rounded_rect(surface, color, rect, radius=16, border=0, border_color=None):
    """Vẽ hình chữ nhật bo góc (dùng nhiều lần)."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


def show_menu(screen, width=600, height=600):
    """
    Hiển thị màn hình Menu chọn chế độ.

    Trả về:
        3  → người dùng chọn bàn 3x3
        5  → người dùng chọn bàn 5x5
        None → người dùng đóng cửa sổ
    """
    # ── Font (dùng DejaVuSans để hiển thị tiếng Việt đúng dấu) ────────────────
    pygame.font.init()
    FONT = "dejavusans"
    font_title    = pygame.font.SysFont(FONT, 42, bold=True)
    font_subtitle = pygame.font.SysFont(FONT, 18)
    font_btn      = pygame.font.SysFont(FONT, 22, bold=True)
    font_desc     = pygame.font.SysFont(FONT, 15)
    font_tag      = pygame.font.SysFont(FONT, 13, bold=True)
    font_footer   = pygame.font.SysFont(FONT, 13)

    # ── Kích thước nút ─────────────────────────────────────────────────────────
    btn_w, btn_h = 220, 64
    gap          = 32                          # khoảng cách giữa 2 nút
    btn_y        = height // 2 - btn_h // 2 + 30
    btn_3x3_x    = width // 2 - btn_w - gap // 2
    btn_5x5_x    = width // 2 + gap // 2

    btn_3x3_rect = pygame.Rect(btn_3x3_x, btn_y, btn_w, btn_h)
    btn_5x5_rect = pygame.Rect(btn_5x5_x, btn_y, btn_w, btn_h)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        hover_3x3 = btn_3x3_rect.collidepoint(mouse_pos)
        hover_5x5 = btn_5x5_rect.collidepoint(mouse_pos)

        # ── Sự kiện ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_3x3:
                    return 3
                if hover_5x5:
                    return 5

        # ── Vẽ nền ─────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Lưới trang trí mờ phía sau
        cell = 60
        for x in range(0, width + cell, cell):
            pygame.draw.line(screen, DIVIDER_COLOR, (x, 0), (x, height), 1)
        for y in range(0, height + cell, cell):
            pygame.draw.line(screen, DIVIDER_COLOR, (0, y), (width, y), 1)

        # ── Tiêu đề ────────────────────────────────────────────────────────────
        title_surf = font_title.render("CARO AI", True, TITLE_COLOR)
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 120)))

        subtitle_surf = font_subtitle.render("Chọn chế độ chơi", True, SUBTITLE_COLOR)
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(width // 2, 168)))

        # Đường kẻ dưới subtitle
        pygame.draw.line(screen, DIVIDER_COLOR,
                         (width // 2 - 80, 188), (width // 2 + 80, 188), 1)

        # ── Nút 3x3 ────────────────────────────────────────────────────────────
        color_3x3 = BTN_HOVER_3X3 if hover_3x3 else BTN_3X3_COLOR
        draw_rounded_rect(screen, color_3x3, btn_3x3_rect, radius=14,
                          border=2, border_color=BORDER_COLOR)

        # Badge tag
        tag_rect = pygame.Rect(btn_3x3_rect.x + 8, btn_3x3_rect.y - 14, 58, 22)
        draw_rounded_rect(screen, TAG_3X3_COLOR, tag_rect, radius=6)
        tag_surf = font_tag.render("Cổ điển", True, TAG_TEXT_3X3)
        screen.blit(tag_surf, tag_surf.get_rect(center=tag_rect.center))

        btn3_surf = font_btn.render("Bàn  3 × 3", True, BTN_TEXT_COLOR)
        screen.blit(btn3_surf, btn3_surf.get_rect(
            center=(btn_3x3_rect.centerx, btn_3x3_rect.centery - 8)))

        desc3_surf = font_desc.render("Minimax thuần túy", True, (255, 220, 220))
        screen.blit(desc3_surf, desc3_surf.get_rect(
            center=(btn_3x3_rect.centerx, btn_3x3_rect.centery + 16)))

        # ── Nút 5x5 ────────────────────────────────────────────────────────────
        color_5x5 = BTN_HOVER_5X5 if hover_5x5 else BTN_5X5_COLOR
        draw_rounded_rect(screen, color_5x5, btn_5x5_rect, radius=14,
                          border=2, border_color=BORDER_COLOR)

        tag5_rect = pygame.Rect(btn_5x5_rect.x + 8, btn_5x5_rect.y - 14, 62, 22)
        draw_rounded_rect(screen, TAG_5X5_COLOR, tag5_rect, radius=6)
        tag5_surf = font_tag.render("Nâng cao", True, TAG_TEXT_5X5)
        screen.blit(tag5_surf, tag5_surf.get_rect(center=tag5_rect.center))

        btn5_surf = font_btn.render("Bàn  5 × 5", True, BTN_TEXT_COLOR)
        screen.blit(btn5_surf, btn5_surf.get_rect(
            center=(btn_5x5_rect.centerx, btn_5x5_rect.centery - 8)))

        desc5_surf = font_desc.render("Alpha-Beta + Heuristic", True, (220, 240, 255))
        screen.blit(desc5_surf, desc5_surf.get_rect(
            center=(btn_5x5_rect.centerx, btn_5x5_rect.centery + 16)))

        # ── Chú thích bên dưới nút ─────────────────────────────────────────────
        note_y = btn_y + btn_h + 28
        note_surf = font_desc.render("Luật ăn: 3 quân liên tiếp (3x3)  |  4 quân liên tiếp (5x5)", True, SUBTITLE_COLOR)
        screen.blit(note_surf, note_surf.get_rect(center=(width // 2, note_y)))

        # ── Footer ─────────────────────────────────────────────────────────────
        footer_surf = font_footer.render(
            "Đăng  •  Thuần  •  Nguyên  —  Đồ án Trí tuệ Nhân tạo", True, SUBTITLE_COLOR)
        screen.blit(footer_surf, footer_surf.get_rect(center=(width // 2, height - 28)))

        pygame.display.flip()
        clock.tick(60)


# ── Chạy thử độc lập ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Caro AI — Menu")

    choice = show_menu(screen)
    print(f"[TEST] Người dùng chọn bàn: {choice}x{choice}")

    pygame.quit()
    sys.exit()
