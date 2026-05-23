# ============================================================
# main.py  –  Điểm khởi động toàn bộ trò chơi
# Ráp nối: ui_menu.py + ui_board.py (Người 1) + logic.py (Người 2)
# Người 3 (Thuần) chỉ cần thêm: from ai_5x5 import get_ai_move
# ============================================================

import pygame
import sys

from ui_menu  import show_menu
from ui_board import (draw_board, draw_piece, draw_win_line,
                      draw_game_over, WIDTH, HEIGHT)
from logic    import (GameLogic, EMPTY, PLAYER, AI,
                      STATE_PLAYING, STATE_PLAYER_WIN,
                      STATE_AI_WIN, STATE_DRAW)

# ── Thử import AI (Người 3 sẽ tạo file này) ──────────────────────────────────
try:
    from ai_5x5 import get_ai_move as ai_5x5_move   # Alpha-Beta
    AI_5X5_READY = True
except ImportError:
    AI_5X5_READY = False

try:
    from ai_3x3 import get_ai_move as ai_3x3_move   #     pygame.time.delay(200)  # Delay 200ms trước khi AI đi    pygame.time.delay(200)  # Delay 200ms trước khi AI điMinimax thuần
    AI_3X3_READY = True
except ImportError:
    AI_3X3_READY = False

# ── Cấu hình luật thắng theo bàn ─────────────────────────────────────────────
WIN_LENGTH = {3: 3, 5: 4}   # 3x3 → 3 quân; 5x5 → 4 quân liên tiếp


def piece_to_char(piece: int) -> str:
    """Chuyển hằng số PLAYER/AI → ký tự 'X'/'O' cho ui_board."""
    return 'X' if piece == PLAYER else 'O'


def find_win_endpoints(game: GameLogic) -> tuple | None:
    """
    Tìm ô đầu – cuối của chuỗi thắng để vẽ draw_win_line.
    Quét lại toàn bàn sau khi game_state != playing.
    Trả về ((r1,c1), (r2,c2)) hoặc None nếu là HÒA.
    """
    if game.game_state == STATE_DRAW:
        return None

    board = game.board
    size  = game.size
    wl    = game.win_length
    piece = PLAYER if game.game_state == STATE_PLAYER_WIN else AI

    DIRS = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(size):
        for c in range(size):
            if board[r][c] != piece:
                continue
            for dr, dc in DIRS:
                # Đếm chuỗi
                cells = [(r, c)]
                nr, nc = r + dr, c + dc
                while (0 <= nr < size and 0 <= nc < size
                       and board[nr][nc] == piece):
                    cells.append((nr, nc))
                    nr += dr; nc += dc
                if len(cells) >= wl:
                    return cells[0], cells[-1]
    return None


def run_game(screen: pygame.Surface, size: int) -> str:
    """
    Vòng lặp một ván cờ.

    Trả về
    ------
    'menu'   → quay về menu
    'quit'   → thoát hẳn
    'replay' → chơi lại cùng kích thước
    """
    game   = GameLogic(size=size, win_length=WIN_LENGTH[size])
    clock  = pygame.time.Clock()

    # Bàn cờ chiếm toàn màn hình: gốc toạ độ (0, 0)
    ORIGIN_X, ORIGIN_Y = 0, 0
    CELL = WIDTH // size

    # Vẽ bàn trống lần đầu
    draw_board(screen, size)
    pygame.display.flip()

    ai_thinking = False   # cờ để trì hoãn 1 frame trước khi AI tính

    while True:
        clock.tick(60)

        # ── Xử lý sự kiện ────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
                if event.key == pygame.K_SPACE:
                    if game.game_state != STATE_PLAYING:
                        return 'replay'

            # Click chuột → lượt NGƯỜI
            if (event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and game.is_playing()
                    and game.current_turn == PLAYER):

                moved = game.handle_click(
                    event.pos[0], event.pos[1],
                    ORIGIN_X, ORIGIN_Y, CELL
                )
                if moved:
                    # Vẽ lại toàn bàn sau mỗi nước
                    _redraw_all(screen, game, size)
                    if game.is_playing():
                        ai_thinking = True   # báo cho AI chuẩn bị

        # ── Lượt AI ───────────────────────────────────────────────────────────
        if ai_thinking and game.is_playing() and game.current_turn == AI:
            ai_thinking = False
            _do_ai_move(game, size)
            _redraw_all(screen, game, size)

        # ── Màn hình kết thúc ─────────────────────────────────────────────────
        if game.game_state != STATE_PLAYING:
            # Vẽ đường thắng
            endpoints = find_win_endpoints(game)
            if endpoints:
                draw_win_line(screen, endpoints[0], endpoints[1], size)

            # Thông báo
            msg_map = {
                STATE_PLAYER_WIN : "X THẮNG!",
                STATE_AI_WIN     : "O THẮNG!",
                STATE_DRAW       : "HÒA!",
            }
            draw_game_over(screen, msg_map[game.game_state])
            # draw_game_over đã gọi pygame.display.update() bên trong

        pygame.display.flip()


# ── Vẽ lại toàn bộ quân cờ ───────────────────────────────────────────────────

def _redraw_all(screen: pygame.Surface, game: GameLogic, size: int) -> None:
    """Xoá + vẽ lại bàn cờ và tất cả quân."""
    draw_board(screen, size)
    for r in range(size):
        for c in range(size):
            p = game.board[r][c]
            if p != EMPTY:
                draw_piece(screen, r, c, piece_to_char(p), size)
    pygame.display.flip()


# ── Gọi AI tính nước ─────────────────────────────────────────────────────────

def _do_ai_move(game: GameLogic, size: int) -> None:
    """
    Gọi hàm AI phù hợp rồi áp dụng nước đi vào game.
    Nếu AI chưa sẵn sàng → đánh ô đầu tiên còn trống (placeholder).
    """
    if size == 5 and AI_5X5_READY:
        row, col = ai_5x5_move(game)
    elif size == 3 and AI_3X3_READY:
        row, col = ai_3x3_move(game)
    else:
        # ── Placeholder: AI random ô trống đầu tiên ──────────────────────────
        # Thay bằng hàm AI thật khi Người 3 hoàn thành
        empties = game.get_empty_cells()
        if empties:
            row, col = empties[0]
        else:
            return

    game.apply_move(row, col, AI)


# ── Vòng lặp chính ───────────────────────────────────────────────────────────

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Caro AI")

    while True:
        # Màn hình Menu
        size = show_menu(screen)      # trả về 3 hoặc 5
        if size is None:
            break

        # Vòng lặp ván cờ (có thể replay nhiều lần)
        action = 'replay'
        while action == 'replay':
            action = run_game(screen, size)

        if action == 'quit':
            break
        # action == 'menu' → vòng while ngoài tiếp tục

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
