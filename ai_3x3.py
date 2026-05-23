# ============================================================
# ai_3x3.py  –  Minimax thuần túy cho bàn 3x3
#               Tự xác định lượt → AI không bao giờ thua
# main.py gọi: from ai_3x3 import get_ai_move
# ============================================================

from logic import GameLogic, PLAYER, AI, EMPTY

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6),
]


def _check_winner(board_1d: list) -> int | None:
    for a, b, c in WIN_LINES:
        if board_1d[a] != EMPTY and board_1d[a] == board_1d[b] == board_1d[c]:
            return board_1d[a]
    if all(cell != EMPTY for cell in board_1d):
        return 0
    return None


def _minimax(board_1d: list, is_maximizing: bool,
             alpha: int, beta: int, depth: int) -> int:
    result = _check_winner(board_1d)
    if result == AI:     return +10 - depth
    if result == PLAYER: return -10 + depth
    if result == 0:      return 0

    if is_maximizing:
        best = -999
        for i in range(9):
            if board_1d[i] == EMPTY:
                board_1d[i] = AI
                score = _minimax(board_1d, False, alpha, beta, depth + 1)
                board_1d[i] = EMPTY
                best  = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = +999
        for i in range(9):
            if board_1d[i] == EMPTY:
                board_1d[i] = PLAYER
                score = _minimax(board_1d, True, alpha, beta, depth + 1)
                board_1d[i] = EMPTY
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


def get_ai_move(game: GameLogic) -> tuple[int, int]:
    board_2d = game.get_board()
    board_1d = [board_2d[r][c] for r in range(3) for c in range(3)]

    best_score, best_index = -999, None
    for i in range(9):
        if board_1d[i] == EMPTY:
            board_1d[i] = AI
            score = _minimax(board_1d, False, -999, 999, 0)
            board_1d[i] = EMPTY
            if score > best_score:
                best_score = score
                best_index = i

    return best_index // 3, best_index % 3
