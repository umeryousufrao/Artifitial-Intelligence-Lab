import math

class CoinGame:
    def __init__(self, coins):
        self.coins = coins
        self.max_score = 0
        self.min_score = 0
        
    def print_game_state(self, coins, max_score, min_score):
        """Print the current state of the game"""
        print(f"Coins: {coins}")
        print(f"Max score: {max_score}, Min score: {min_score}")
        
    def alpha_beta_minimax(self, coins, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        # Base case: If no coins left
        if len(coins) == 0:
            return 0
            
        if is_maximizing:
            best_score = -math.inf
            
            # Try taking the leftmost coin
            value = coins[0]
            score = value + self.alpha_beta_minimax(coins[1:], depth + 1, alpha, beta, False)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            
            # Try taking the rightmost coin
            if len(coins) > 1 and alpha < beta:  # Skip if already pruned
                value = coins[-1]
                score = value + self.alpha_beta_minimax(coins[:-1], depth + 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                
            # Alpha-beta pruning
            if beta <= alpha:
                return best_score
                
            return best_score
            
        else:  # Minimizing player
            best_score = math.inf
            
            # Try taking the leftmost coin
            score = self.alpha_beta_minimax(coins[1:], depth + 1, alpha, beta, True)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            
            # Try taking the rightmost coin
            if len(coins) > 1 and alpha < beta:  # Skip if already pruned
                score = self.alpha_beta_minimax(coins[:-1], depth + 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                
            # Alpha-beta pruning
            if beta <= alpha:
                return best_score
                
            return best_score
    
    def get_best_move(self, coins):
        """Determine the best move for Max player using alpha-beta pruning"""
        take_left_score = coins[0] + self.alpha_beta_minimax(coins[1:], 0, -math.inf, math.inf, False)
        take_right_score = coins[-1] + self.alpha_beta_minimax(coins[:-1], 0, -math.inf, math.inf, False)
        
        if take_left_score >= take_right_score:
            return 'left', take_left_score
        else:
            return 'right', take_right_score
    
    def min_player_move(self, coins):
        """Min player's strategy: take the coin with the minimum value"""
        if coins[0] <= coins[-1]:
            return 'left'
        else:
            return 'right'
    
    def play_game(self):
        """Play the coin game"""
        print(f"Initial Coins: {self.coins}")
        
        current_coins = self.coins.copy()
        current_player = 'Max'  # Max goes first
        
        while current_coins:
            if current_player == 'Max':
                # Max's turn
                move, _ = self.get_best_move(current_coins)
                
                if move == 'left':
                    coin_value = current_coins[0]
                    print(f"Max picks {coin_value}, Remaining Coins: {current_coins[1:]}")
                    self.max_score += coin_value
                    current_coins = current_coins[1:]
                else:  # move == 'right'
                    coin_value = current_coins[-1]
                    print(f"Max picks {coin_value}, Remaining Coins: {current_coins[:-1]}")
                    self.max_score += coin_value
                    current_coins = current_coins[:-1]
                    
                current_player = 'Min'
                
            else:  # Min's turn
                move = self.min_player_move(current_coins)
                
                if move == 'left':
                    coin_value = current_coins[0]
                    print(f"Min picks {coin_value}, Remaining Coins: {current_coins[1:]}")
                    self.min_score += coin_value
                    current_coins = current_coins[1:]
                else:  # move == 'right'
                    coin_value = current_coins[-1]
                    print(f"Min picks {coin_value}, Remaining Coins: {current_coins[:-1]}")
                    self.min_score += coin_value
                    current_coins = current_coins[:-1]
                    
                current_player = 'Max'
        
        # Game over
        print(f"Final Scores - Max: {self.max_score}, Min: {self.min_score}")
        if self.max_score > self.min_score:
            print("Winner: Max")
        elif self.min_score > self.max_score:
            print("Winner: Min")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    # Sample coins as given in the example
    coins = [3, 9, 1, 2, 7, 5]
    game = CoinGame(coins)
    game.play_game()
