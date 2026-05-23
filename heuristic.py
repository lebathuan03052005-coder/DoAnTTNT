
from logic import EMPTY, PLAYER, AI   # dùng chung hằng số
# BẢNG ĐIỂM
# Chuỗi càng dài → điểm càng cao (hàm mũ)
# Hai đầu thoáng (open) > một đầu chặn (half) > bị chặn hoàn toàn (0)
_SCORE_TABLE: dict[tuple[int, int], int] = {
    # (độ dài chuỗi, số đầu thoáng)
    (5, 2): 1_000_000,   # Thắng ngay
    (5, 1): 1_000_000,
    (4, 2):   100_000,   # Chuỗi 4 hai đầu thoáng → gần như chắc thắng
    (4, 1):    10_000,   # Chuỗi 4 một đầu chặn
    (3, 2):     5_000,   # Chuỗi 3 hai đầu thoáng
    (3, 1):       500,   # Chuỗi 3 một đầu chặn
    (2, 2):       100,   # Chuỗi 2 hai đầu thoáng
    (2, 1):        10,   # Chuỗi 2 một đầu chặn
    (1, 2):         2,
    (1, 1):         1,
}


def evaluate_board(board: list[list[int]], size: int = 5) -> int:
    """
    Chấm điểm toàn bộ bàn cờ theo góc nhìn của AI (quân O).

    Điểm > 0  → AI đang có lợi thế.
    Điểm < 0  → Người chơi đang có lợi thế.
    Điểm = 0  → Cân bằng.

    Thuật toán
    ----------
    Duyệt mọi ô trên bàn × 4 hướng.
    Với mỗi hướng, đếm chuỗi liên tiếp cùng loại quân, kiểm tra
    2 đầu của chuỗi có thoáng không (loang 4 hướng – y hệt _check_win).
    Mỗi chuỗi chỉ được tính 1 lần (đánh dấu visited).

    Tham số
    -------
    board : bàn cờ 2D (lấy từ GameLogic.get_board())
    size  : kích thước bàn (mặc định 5)

    Trả về
    ------
    int  – điểm tổng (AI_score - PLAYER_score)
    """
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

    ai_score     = 0
    player_score = 0

    # visited[r][c][d] = True nếu ô (r,c) theo hướng d đã được đếm
    visited = [[[False] * 4 for _ in range(size)] for _ in range(size)]

    for r in range(size):
        for c in range(size):
            piece = board[r][c]
            if piece == EMPTY:
                continue

            for d_idx, (dr, dc) in enumerate(DIRECTIONS):
                if visited[r][c][d_idx]:
                    continue  # Chuỗi này đã tính từ ô trước

                # ── Đếm độ dài chuỗi ──────────────────────
                length = 1
                visited[r][c][d_idx] = True

                nr, nc = r + dr, c + dc
                while 0 <= nr < size and 0 <= nc < size \
                        and board[nr][nc] == piece:
                    visited[nr][nc][d_idx] = True
                    length += 1
                    nr += dr
                    nc += dc

                # ── Kiểm tra 2 đầu có thoáng không ────────
                # Đầu sau (chiều thuận): (nr, nc) là ô ngay sau chuỗi
                open_end_forward = (
                    0 <= nr < size and 0 <= nc < size
                    and board[nr][nc] == EMPTY
                )

                # Đầu trước (chiều ngược): ô ngay trước điểm bắt đầu
                pr, pc = r - dr, c - dc
                open_end_backward = (
                    0 <= pr < size and 0 <= pc < size
                    and board[pr][pc] == EMPTY
                )

                open_ends = int(open_end_forward) + int(open_end_backward)

                # Chuỗi bị chặn cả 2 đầu → vô nghĩa, bỏ qua
                if open_ends == 0:
                    continue

                # ── Tra bảng điểm ─────────────────────────
                score = _SCORE_TABLE.get((length, open_ends), 0)

                if piece == AI:
                    ai_score += score
                else:
                    player_score += score

    return ai_score - player_score


# ──────────────────────────────────────────────
# HÀM TIỆN ÍCH CHO UI VÀ AI
# ──────────────────────────────────────────────

def is_terminal(board: list[list[int]], size: int = 5,
                win_length: int = 5) -> tuple[bool, int | None]:
    """
    Kiểm tra nhanh xem bàn cờ đã kết thúc chưa.

    Trả về
    ------
    (True,  AI)     – AI thắng
    (True,  PLAYER) – Người thắng
    (True,  None)   – Hoà (hết ô)
    (False, None)   – Trận đang tiếp diễn

    Lưu ý: hàm này quét toàn bộ bàn (chậm hơn _check_win vì không biết
    ô vừa đặt). Người 3 nên dùng GameLogic.get_game_state() khi có thể;
    chỉ gọi hàm này khi cần kiểm tra board thuần tuý không có GameLogic.
    """
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    empty_exists = False

    for r in range(size):
        for c in range(size):
            piece = board[r][c]
            if piece == EMPTY:
                empty_exists = True
                continue

            for dr, dc in DIRECTIONS:
                count = 1
                nr, nc = r + dr, c + dc
                while 0 <= nr < size and 0 <= nc < size \
                        and board[nr][nc] == piece:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= win_length:
                    return True, piece

    if not empty_exists:
        return True, None   # Hoà

    return False, None


def get_candidate_moves(board: list[list[int]],
                        size: int = 5,
                        radius: int = 2) -> list[tuple[int, int]]:
    """
    Trả về danh sách ô trống LÂN CẬN những quân đã đặt (trong bán kính
    `radius` ô). Giúp Alpha-Beta không phải duyệt 25 ô mà chỉ ~8-15 ô.

    Người 3 gọi hàm này thay cho GameLogic.get_empty_cells() để tăng tốc.

    Tham số
    -------
    board  : bàn cờ 2D
    size   : kích thước bàn
    radius : bán kính tìm kiếm (2 là đủ cho bàn 5x5)
    """
    candidates: set[tuple[int, int]] = set()

    for r in range(size):
        for c in range(size):
            if board[r][c] == EMPTY:
                continue
            # Thêm các ô trống trong vùng lân cận
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < size and 0 <= nc < size
                            and board[nr][nc] == EMPTY):
                        candidates.add((nr, nc))

    # Nếu bàn trống hoàn toàn, trả về ô trung tâm
    if not candidates:
        mid = size // 2
        return [(mid, mid)]

    return list(candidates)
