import math

class TicTacToe:
    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'O'  # Human player starts
        self.ai_player = 'X'
        self.human_player = 'O'
        
    def print_board(self):
        """Print the current state of the board"""
        for i in range(3):
            print('|'.join(self.board[i]))
            if i < 2:
                print('-' * 5)
                
    def is_valid_move(self, row, col):
        """Check if the move is valid"""
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        return self.board[row][col] == ' '
    
    def make_move(self, row, col, player):
        """Make a move on the board"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        """Check if there is a winner"""
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
                
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
            
        return None
    
    def is_board_full(self):
        """Check if the board is full (draw)"""
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True
    
    def game_over(self):
        """Check if the game is over"""
        return self.check_winner() is not None or self.is_board_full()
    
    def get_available_moves(self):
        """Get all available moves"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def minimax(self, depth, is_maximizing):
        """Minimax algorithm implementation"""
        # Terminal states
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10 - depth
        elif winner == self.human_player:
            return depth - 10
        elif self.is_board_full():
            return 0
        
        # Maximizing player (AI)
        if is_maximizing:
            best_score = -math.inf
            for move in self.get_available_moves():
                row, col = move
                self.board[row][col] = self.ai_player
                score = self.minimax(depth + 1, False)
                self.board[row][col] = ' '  # Undo move
                best_score = max(score, best_score)
            return best_score
        
        # Minimizing player (Human)
        else:
            best_score = math.inf
            for move in self.get_available_moves():
                row, col = move
                self.board[row][col] = self.human_player
                score = self.minimax(depth + 1, True)
                self.board[row][col] = ' '  # Undo move
                best_score = min(score, best_score)
            return best_score
    
    def best_move(self):
        """Find the best move for AI using minimax"""
        best_score = -math.inf
        best_move = None
        
        for move in self.get_available_moves():
            row, col = move
            self.board[row][col] = self.ai_player
            score = self.minimax(0, False)
            self.board[row][col] = ' '  # Undo move
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def play_game(self):
        """Main game loop"""
        print("Welcome to Tic-Tac-Toe!")
        print("You are O, AI is X")
        print("Positions are entered as: row column (0-2)")
        
        self.print_board()
        
        while not self.game_over():
            # Human player's turn
            valid_move = False
            while not valid_move:
                try:
                    row, col = map(int, input("Enter row and column (0-2): ").split())
                    valid_move = self.make_move(row, col, self.human_player)
                    if not valid_move:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Please enter two numbers separated by space.")
            
            self.print_board()
            
            # Check if game is over after human's move
            if self.game_over():
                break
                
            # AI's turn
            row, col = self.best_move()
            self.make_move(row, col, self.ai_player)
            print(f"AI places X at position ({row}, {col})")
            
            self.print_board()
        
        # Game over
        winner = self.check_winner()
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a draw!")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
