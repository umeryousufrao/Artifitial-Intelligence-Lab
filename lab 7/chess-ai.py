import math

class Piece:
    def __init__(self, color, piece_type, value):
        self.color = color  # 'white' or 'black'
        self.type = piece_type  # 'pawn', 'knight', 'bishop', 'rook', 'queen', 'king'
        self.value = value  # Numerical value of piece
        self.has_moved = False
    
    def __str__(self):
        symbols = {
            'white': {'pawn': '♙', 'knight': '♘', 'bishop': '♗', 'rook': '♖', 'queen': '♕', 'king': '♔'},
            'black': {'pawn': '♟', 'knight': '♞', 'bishop': '♝', 'rook': '♜', 'queen': '♛', 'king': '♚'}
        }
        return symbols[self.color][self.type]

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.initialize_board()
        
    def initialize_board(self):
        """Set up the initial chess board"""
        # Piece values from classical chess theory
        # Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9, King=∞ (represented as 100)
        
        # Set up pawns
        for col in range(8):
            self.board[1][col] = Piece('black', 'pawn', 1)
            self.board[6][col] = Piece('white', 'pawn', 1)
            
        # Set up rooks
        self.board[0][0] = Piece('black', 'rook', 5)
        self.board[0][7] = Piece('black', 'rook', 5)
        self.board[7][0] = Piece('white', 'rook', 5)
        self.board[7][7] = Piece('white', 'rook', 5)
        
        # Set up knights
        self.board[0][1] = Piece('black', 'knight', 3)
        self.board[0][6] = Piece('black', 'knight', 3)
        self.board[7][1] = Piece('white', 'knight', 3)
        self.board[7][6] = Piece('white', 'knight', 3)
        
        # Set up bishops
        self.board[0][2] = Piece('black', 'bishop', 3)
        self.board[0][5] = Piece('black', 'bishop', 3)
        self.board[7][2] = Piece('white', 'bishop', 3)
        self.board[7][5] = Piece('white', 'bishop', 3)
        
        # Set up queens
        self.board[0][3] = Piece('black', 'queen', 9)
        self.board[7][3] = Piece('white', 'queen', 9)
        
        # Set up kings
        self.board[0][4] = Piece('black', 'king', 100)
        self.board[7][4] = Piece('white', 'king', 100)
    
    def print_board(self):
        """Print the current state of the board"""
        print("  a b c d e f g h")
        print(" +-----------------+")
        for i in range(8):
            print(f"{8-i}|", end=" ")
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    print(".", end=" ")
                else:
                    print(piece, end=" ")
            print(f"|{8-i}")
        print(" +-----------------+")
        print("  a b c d e f g h")
        
    def is_valid_position(self, row, col):
        """Check if a position is within the board boundaries"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece_at(self, row, col):
        """Get the piece at a specific position"""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def get_all_moves(self, color):
        """Get all possible moves for a specific color"""
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece is not None and piece.color == color:
                    moves = self.get_piece_moves(row, col)
                    for move in moves:
                        all_moves.append(((row, col), move))
        return all_moves
    
    def get_piece_moves(self, row, col):
        """Get all possible moves for a piece at a specific position"""
        piece = self.get_piece_at(row, col)
        if piece is None:
            return []
            
        moves = []
        
        # Pawn moves
        if piece.type == 'pawn':
            moves = self.get_pawn_moves(row, col, piece.color)
            
        # Knight moves
        elif piece.type == 'knight':
            moves = self.get_knight_moves(row, col, piece.color)
            
        # Bishop moves
        elif piece.type == 'bishop':
            moves = self.get_bishop_moves(row, col, piece.color)
            
        # Rook moves
        elif piece.type == 'rook':
            moves = self.get_rook_moves(row, col, piece.color)
            
        # Queen moves (combination of bishop and rook)
        elif piece.type == 'queen':
            moves = self.get_bishop_moves(row, col, piece.color) + self.get_rook_moves(row, col, piece.color)
            
        # King moves
        elif piece.type == 'king':
            moves = self.get_king_moves(row, col, piece.color)
            
        return moves
        
    def get_pawn_moves(self, row, col, color):
        """Get all possible moves for a pawn"""
        moves = []
        direction = -1 if color == 'white' else 1
        start_row = 6 if color == 'white' else 1
        
        # Move forward one square
        new_row = row + direction
        if self.is_valid_position(new_row, col) and self.get_piece_at(new_row, col) is None:
            moves.append((new_row, col))
            
            # Move forward two squares from starting position
            if row == start_row:
                new_row = row + 2 * direction
                if self.is_valid_position(new_row, col) and self.get_piece_at(new_row, col) is None:
                    moves.append((new_row, col))
        
        # Capture diagonally
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            new_row = row + direction
            if self.is_valid_position(new_row, new_col):
                target_piece = self.get_piece_at(new_row, new_col)
                if target_piece is not None and target_piece.color != color:
                    moves.append((new_row, new_col))
        
        return moves
        
    def get_knight_moves(self, row, col, color):
        """Get all possible moves for a knight"""
        moves = []
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for row_offset, col_offset in offsets:
            new_row, new_col = row + row_offset, col + col_offset
            if self.is_valid_position(new_row, new_col):
                target_piece = self.get_piece_at(new_row, new_col)
                if target_piece is None or target_piece.color != color:
                    moves.append((new_row, new_col))
        
        return moves
        
    def get_bishop_moves(self, row, col, color):
        """Get all possible moves for a bishop"""
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        
        for row_dir, col_dir in directions:
            for distance in range(1, 8):
                new_row, new_col = row + row_dir * distance, col + col_dir * distance
                if not self.is_valid_position(new_row, new_col):
                    break
                    
                target_piece = self.get_piece_at(new_row, new_col)
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
        
    def get_rook_moves(self, row, col, color):
        """Get all possible moves for a rook"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Horizontal and vertical directions
        
        for row_dir, col_dir in directions:
            for distance in range(1, 8):
                new_row, new_col = row + row_dir * distance, col + col_dir * distance
                if not self.is_valid_position(new_row, new_col):
                    break
                    
                target_piece = self.get_piece_at(new_row, new_col)
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
        
    def get_king_moves(self, row, col, color):
        """Get all possible moves for a king"""
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for row_dir, col_dir in directions:
            new_row, new_col = row + row_dir, col + col_dir
            if self.is_valid_position(new_row, new_col):
                target_piece = self.get_piece_at(new_row, new_col)
                if target_piece is None or target_piece.color != color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def make_move(self, from_pos, to_pos):
        """Make a move on the board"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece_at(from_row, from_col)
        if piece is None:
            return False
            
        # Mark the piece as moved
        piece.has_moved = True
        
        # Make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Switch current player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
    
    def undo_move(self, from_pos, to_pos, captured_piece=None):
        """Undo a move on the board"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece_at(to_row, to_col)
        if piece is None:
            return False
            
        # Undo the move
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured_piece
        
        # Switch current player back
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
    
    def is_check(self, color):
        """Check if the king of the specified color is in check"""
        # Find the king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece is not None and piece.color == color and piece.type == 'king':
                    king_pos = (row, col)
                    break
            if king_pos:
                break
                
        if not king_pos:
            return False  # No king found
            
        # Check if any opponent's piece can capture the king
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece is not None and piece.color == opponent_color:
                    moves = self.get_piece_moves(row, col)
                    if king_pos in moves:
                        return True
                        
        return False
    
    def is_checkmate(self, color):
        """Check if the king of the specified color is in checkmate"""
        if not self.is_check(color):
            return False
            
        # Check if any move can get the king out of check
        for from_row in range(8):
            for from_col in range(8):
                piece = self.get_piece_at(from_row, from_col)
                if piece is not None and piece.color == color:
                    moves = self.get_piece_moves(from_row, from_col)
                    for to_row, to_col in moves:
                        # Try the move
                        captured_piece = self.get_piece_at(to_row, to_col)
                        self.make_move((from_row, from_col), (to_row, to_col))
                        
                        # Check if still in check
                        still_in_check = self.is_check(color)
                        
                        # Undo the move
                        self.undo_move((from_row, from_col), (to_row, to_col), captured_piece)
                        
                        if not still_in_check:
                            return False  # Found a move that gets out of check
        
        return True  # No move can get out of check
    
    def is_stalemate(self, color):
        """Check if the king of the specified color is in stalemate"""
        if self.is_check(color):
            return False
            
        # Check if any move is possible
        for from_row in range(8):
            for from_col in range(8):
                piece = self.get_piece_at(from_row, from_col)
                if piece is not None and piece.color == color:
                    moves = self.get_piece_moves(from_row, from_col)
                    if moves:
                        return False  # Found a possible move
        
        return True  # No move is possible
    
    def evaluate_board(self):
        """Evaluate the current board position"""
        # Simple evaluation: sum of piece values
        white_score = 0
        black_score = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece is not None:
                    if piece.color == 'white':
                        white_score += piece.value
                    else:
                        black_score += piece.value
        
        return white_score - black_score
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0:
            return self.evaluate_board()
            
        if maximizing_player:
            best_score = -math.inf
            for from_pos, to_pos in self.get_all_moves('white'):
                # Make move
                captured_piece = self.get_piece_at(to_pos[0], to_pos[1])
                self.make_move(from_pos, to_pos)
                
                # Recursive evaluation
                score = self.minimax(depth - 1, alpha, beta, False)
                
                # Undo move
                self.undo_move(from_pos, to_pos, captured_piece)
                
                # Update best score and alpha
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
                    
            return best_score
            
        else:  # Minimizing player
            best_score = math.inf
            for from_pos, to_pos in self.get_all_moves('black'):
                # Make move
                captured_piece = self.get_piece_at(to_pos[0], to_pos[1])
                self.make_move(from_pos, to_pos)
                
                # Recursive evaluation
                score = self.minimax(depth - 1, alpha, beta, True)
                
                # Undo move
                self.undo_move(from_pos, to_pos, captured_piece)
                
                # Update best score and beta
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
                    
            return best_score
    
    def get_best_move(self, color, depth=3):
        """Find the best move for the specified color using minimax with alpha-beta pruning"""
        best_move = None
        
        if color == 'white':
            best_score = -math.inf
            for from_pos, to_pos in self.get_all_moves('white'):
                # Make move
                captured_piece = self.get_piece_at(to_pos[0], to_pos[1])
                self.make_move(from_pos, to_pos)
                
                # Evaluate
                score = self.minimax(depth - 1, -math.inf, math.inf, False)
                
                # Undo move
                self.undo_move(from_pos, to_pos, captured_piece)
                
                # Update best move
                if score > best_score:
                    best_score = score
                    best_move = (from_pos, to_pos)
                    
        else:  # color == 'black'
            best_score = math.inf
            for from_pos, to_pos in self.get_all_moves('black'):
                # Make move
                captured_piece = self.get_piece_at(to_pos[0], to_pos[1])
                self.make_move(from_pos, to_pos)
                
                # Evaluate
                score = self.minimax(depth - 1, -math.inf, math.inf, True)
                
                # Undo move
                self.undo_move