# ============================================================
# logic.py  –  Trần Cao Nguyên (Người 2)
# Nhiệm vụ: Xử lý click chuột, quản lý mảng 2 chiều,
#           quét thắng/thua động theo 4 hướng.
# Giao tiếp:
#   - Người 1 (Đăng)  : gọi handle_click(), get_board(), get_game_state()
#   - Người 3 (Thuần) : nhận board 2D qua get_board(); gọi apply_move()
# ============================================================

# ──────────────────────────────────────────────
# HẰNG SỐ  (dùng chung toàn project)
# ──────────────────────────────────────────────
EMPTY  = 0
PLAYER = 1   # X – người chơi
AI     = 2   # O – máy

# Trạng thái trận đấu  (game_state)
STATE_PLAYING     = "playing"
STATE_PLAYER_WIN  = "player_win"
STATE_AI_WIN      = "ai_win"
STATE_DRAW        = "draw"


# ──────────────────────────────────────────────
# CLASS CHÍNH
# ──────────────────────────────────────────────
class GameLogic:
    """
    Quản lý toàn bộ logic một ván cờ (3x3 hoặc 5x5).

    Tham số khởi tạo
    ----------------
    size : int
        Kích thước bàn cờ (3 hoặc 5).
    win_length : int | None
        Số quân liên tiếp để thắng.
        Mặc định: bằng size (3→3, 5→5).
    """

    def __init__(self, size: int = 3, win_length: int | None = None):
        self.size       = size
        self.win_length = win_length if win_length is not None else size

        # Bàn cờ: mảng 2 chiều size×size, giá trị EMPTY/PLAYER/AI
        self.board: list[list[int]] = [
            [EMPTY] * size for _ in range(size)
        ]

        self.current_turn: int = PLAYER   # Lượt hiện tại
        self.game_state: str   = STATE_PLAYING
        self.move_count: int   = 0        # Số nước đã đi
        self.last_move: tuple[int, int] | None = None  # (row, col) vừa đánh

    # ── Giao diện dùng chung ──────────────────

    def get_board(self) -> list[list[int]]:
        """Trả về bàn cờ 2D hiện tại (Người 3 dùng để chạy AI)."""
        return self.board

    def get_game_state(self) -> str:
        """Trả về trạng thái trận (Người 1 dùng để vẽ màn hình)."""
        return self.game_state

    def get_current_turn(self) -> int:
        """Trả về lượt hiện tại: PLAYER hoặc AI."""
        return self.current_turn

    def is_playing(self) -> bool:
        return self.game_state == STATE_PLAYING

    # ── Xử lý click chuột (Người 1 gọi) ──────

    def handle_click(self, pixel_x: int, pixel_y: int,
                     board_origin_x: int, board_origin_y: int,
                     cell_size: int) -> bool:
        """
        Chuyển toạ độ pixel → ô cờ, đánh nước cho NGƯỜI CHƠI.

        Tham số
        -------
        pixel_x, pixel_y       : toạ độ chuột (pygame event.pos)
        board_origin_x/y       : góc trên-trái của bàn cờ trên màn hình
        cell_size              : kích thước mỗi ô (pixel)

        Trả về
        ------
        True  nếu nước đi hợp lệ và đã được áp dụng.
        False nếu ô đã có quân, ngoài bàn, hoặc không phải lượt người.
        """
        if not self.is_playing():
            return False
        if self.current_turn != PLAYER:
            return False

        col = (pixel_x - board_origin_x) // cell_size
        row = (pixel_y - board_origin_y) // cell_size

        return self.apply_move(row, col, PLAYER)

    # ── Áp dụng nước đi (Người 3 cũng gọi để đặt quân AI) ──

    def apply_move(self, row: int, col: int, piece: int) -> bool:
        """
        Đặt quân `piece` vào ô (row, col).

        Trả về True nếu hợp lệ; cập nhật trạng thái trận sau mỗi nước.
        """
        if not self._is_valid(row, col):
            return False

        self.board[row][col] = piece
        self.move_count += 1
        self.last_move = (row, col)

        # Kiểm tra kết quả
        if self._check_win(row, col, piece):
            self.game_state = (
                STATE_PLAYER_WIN if piece == PLAYER else STATE_AI_WIN
            )
        elif self.move_count == self.size * self.size:
            self.game_state = STATE_DRAW
        else:
            # Đổi lượt
            self.current_turn = AI if piece == PLAYER else PLAYER

        return True

    # ── Reset trận mới ────────────────────────

    def reset(self, size: int | None = None,
              win_length: int | None = None) -> None:
        """Khởi động lại ván cờ (có thể đổi kích thước bàn)."""
        if size is not None:
            self.size = size
        self.win_length = win_length if win_length is not None else self.size
        self.board = [[EMPTY] * self.size for _ in range(self.size)]
        self.current_turn = PLAYER
        self.game_state   = STATE_PLAYING
        self.move_count   = 0
        self.last_move    = None

    # ── Tiện ích cho AI (Người 3) ─────────────

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """Trả về danh sách (row, col) còn trống – AI dùng để duyệt nước."""
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == EMPTY
        ]

    def clone(self) -> "GameLogic":
        """
        Tạo bản sao độc lập để AI mô phỏng mà không làm hỏng trận thật.
        Người 3 dùng bên trong vòng lặp Minimax / Alpha-Beta.
        """
        import copy
        cloned = GameLogic.__new__(GameLogic)
        cloned.size        = self.size
        cloned.win_length  = self.win_length
        cloned.board       = copy.deepcopy(self.board)
        cloned.current_turn = self.current_turn
        cloned.game_state  = self.game_state
        cloned.move_count  = self.move_count
        cloned.last_move   = self.last_move
        return cloned

    # ── Nội bộ ───────────────────────────────

    def _is_valid(self, row: int, col: int) -> bool:
        """Ô có nằm trong bàn và còn trống không?"""
        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and self.board[row][col] == EMPTY
        )

    def _check_win(self, row: int, col: int, piece: int) -> bool:
        """
        Quét thắng/thua ĐỘNG theo 4 hướng xuất phát từ ô (row, col).

        4 hướng kiểm tra (mỗi hướng loang 2 phía):
          → ngang      : (0, +1) / (0, -1)
          ↓ dọc        : (+1, 0) / (-1, 0)
          ↘ chéo chính : (+1,+1) / (-1,-1)
          ↗ chéo phụ   : (+1,-1) / (-1,+1)
        """
        DIRECTIONS = [
            (0, 1),   # ngang
            (1, 0),   # dọc
            (1, 1),   # chéo chính
            (1, -1),  # chéo phụ
        ]

        for dr, dc in DIRECTIONS:
            count = 1  # tính ô vừa đặt

            # Loang theo chiều thuận
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size \
                    and self.board[r][c] == piece:
                count += 1
                r += dr
                c += dc

            # Loang theo chiều ngược
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size \
                    and self.board[r][c] == piece:
                count += 1
                r -= dr
                c -= dc

            if count >= self.win_length:
                return True

        return False
