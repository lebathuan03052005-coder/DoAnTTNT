# ============================================================
# ai_5x5.py  –  AI cho bàn 5x5 bằng Alpha-Beta Pruning
#               Sử dụng heuristic từ heuristic.py
# main.py gọi: from ai_5x5 import get_ai_move
# ============================================================

from logic import GameLogic, PLAYER, AI, EMPTY
from heuristic import evaluate_board, is_terminal, get_candidate_moves


def get_ai_move(game: GameLogic) -> tuple[int, int]:
    """
    Tính nước đi tối ưu cho AI (bàn 5x5) dùng Alpha-Beta Pruning.
    
    Tham số
    -------
    game : GameLogic
        Trạng thái trò chơi hiện tại.
    
    Trả về
    ------
    (row, col) : tọa độ nước đi tối ưu.
    """
    # ── Tối ưu: Nước đầu tiên luôn đặt ở giữa nếu còn trống ──
    if game.move_count == 1 and game.board[2][2] == EMPTY:
        return (2, 2)
    
    best_move = None
    best_score = -float('inf')
    
    # Duyệt các nước ứng viên
    candidates = get_candidate_moves(game.board, size=5, radius=2)
    
    for row, col in candidates:
        if game.board[row][col] != EMPTY:
            continue
        
        # Thử đặt quân AI
        game.board[row][col] = AI
        
        # Gọi Minimax với Alpha-Beta (depth=3 để nhanh hơn)
        score = _alpha_beta(game, depth=3, is_maximizing=False, 
                           alpha=-float('inf'), beta=float('inf'))
        
        # Hoàn tác
        game.board[row][col] = EMPTY
        
        # Cập nhật nước đi tốt nhất
        if score > best_score:
            best_score = score
            best_move = (row, col)
    
    # Nếu không tìm được nước (trường hợp hiếm), đặt ở giữa
    if best_move is None:
        return (2, 2)
    
    return best_move


def _alpha_beta(game: GameLogic, depth: int, is_maximizing: bool,
                alpha: float, beta: float) -> int:
    """
    Alpha-Beta Pruning Minimax.
    
    Tham số
    -------
    game : GameLogic
        Trạng thái trò chơi (sẽ được sửa đổi).
    depth : int
        Độ sâu tìm kiếm còn lại.
    is_maximizing : bool
        True nếu tìm max (AI), False nếu tìm min (Người chơi).
    alpha, beta : float
        Giới hạn alpha-beta.
    
    Trả về
    ------
    int : điểm heuristic của nút hiện tại.
    """
    # Kiểm tra điều kiện dừng
    is_terminal_state, winner = is_terminal(game.board, size=5, win_length=4)
    
    if is_terminal_state:
        if winner == AI:
            return 10000  # AI thắng
        elif winner == PLAYER:
            return -10000  # Người chơi thắng
        else:
            return 0  # Hòa
    
    if depth == 0:
        # Đánh giá heuristic
        return evaluate_board(game.board, size=5)
    
    if is_maximizing:
        # Tìm nước đi tối ưu cho AI (max)
        max_eval = -float('inf')
        candidates = get_candidate_moves(game.board, size=5, radius=2)
        
        for row, col in candidates:
            if game.board[row][col] != EMPTY:
                continue
            
            # Thử đặt quân AI
            game.board[row][col] = AI
            eval_score = _alpha_beta(game, depth - 1, False, alpha, beta)
            game.board[row][col] = EMPTY
            
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            
            # Cắt nhánh (beta cutoff)
            if beta <= alpha:
                break
        
        return max_eval
    
    else:
        # Tìm nước đi tối ưu cho Người chơi (min)
        min_eval = float('inf')
        candidates = get_candidate_moves(game.board, size=5, radius=2)
        
        for row, col in candidates:
            if game.board[row][col] != EMPTY:
                continue
            
            # Thử đặt quân Người chơi
            game.board[row][col] = PLAYER
            eval_score = _alpha_beta(game, depth - 1, True, alpha, beta)
            game.board[row][col] = EMPTY
            
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            
            # Cắt nhánh (alpha cutoff)
            if beta <= alpha:
                break
        
        return min_eval
