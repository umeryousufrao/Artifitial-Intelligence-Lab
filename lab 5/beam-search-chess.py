import chess
import chess.engine
import heapq
from typing import List, Tuple, Dict

class ChessBeamSearch:
    def __init__(self, beam_width: int, search_depth: int):
        self.beam_width = beam_width
        self.search_depth = search_depth
        
    def evaluate_position(self, board: chess.Board) -> float:
        piece_values = {
            chess.PAWN: 1.0,
            chess.KNIGHT: 3.0,
            chess.BISHOP: 3.0,
            chess.ROOK: 5.0,
            chess.QUEEN: 9.0,
            chess.KING: 0.0  # King has special evaluation
        }
        
        score = 0.0
        
        # Material balance
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        
        # Mobility (number of legal moves)
        mobility = len(list(board.legal_moves))
        score += 0.1 * mobility if board.turn == chess.WHITE else -0.1 * mobility
        
        # Center control
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += 0.5
                else:
                    score -= 0.5
                    
        return score if board.turn == chess.WHITE else -score
    
    def get_best_moves(self, board: chess.Board, n: int) -> List[Tuple[float, chess.Move]]:
        moves = []
        for move in board.legal_moves:
            board_copy = board.copy()
            board_copy.push(move)
            score = self.evaluate_position(board_copy)
            moves.append((-score, move))  # Negative because heapq is min-heap
        
        return heapq.nsmallest(n, moves)
    
    def beam_search(self, board: chess.Board) -> Tuple[List[chess.Move], float]:
        if self.search_depth == 0:
            return [], self.evaluate_position(board)
        
        beam = [(0, board.copy(), [])]  # (cumulative_score, board_state, move_sequence)
        
        for depth in range(self.search_depth):
            new_beam = []
            
            for cum_score, current_board, move_seq in beam:
                best_moves = self.get_best_moves(current_board, self.beam_width)
                
                for neg_score, move in best_moves:
                    score = -neg_score  # Convert back to actual score
                    new_board = current_board.copy()
                    new_board.push(move)
                    new_move_seq = move_seq + [move]
                    new_cum_score = cum_score + score
                    new_beam.append((new_cum_score, new_board, new_move_seq))
            
            # Keep only the top beam_width candidates
            beam = heapq.nlargest(self.beam_width, new_beam, key=lambda x: x[0])
        
        # Return the best move sequence and its score
        best_score, _, best_move_seq = max(beam, key=lambda x: x[0])
        return best_move_seq, best_score

def predict_best_move(fen: str, beam_width: int, depth: int) -> Tuple[List[str], float]:
    board = chess.Board(fen)
    searcher = ChessBeamSearch(beam_width, depth)
    moves, score = searcher.beam_search(board)
    return [move.uci() for move in moves], score

if __name__ == "__main__":
    # Example usage
    current_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
    beam_width = 3
    depth = 3
    
    moves, score = predict_best_move(current_fen, beam_width, depth)
    print(f"Best move sequence: {moves}")
    print(f"Evaluation score: {score}")
