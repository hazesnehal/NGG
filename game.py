import random
import json
from datetime import datetime

class NumberGuessingGame:
    def __init__(self):
        self.min_number = 1
        self.max_number = 100
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 7
        self.game_active = False
        self.player_name = ""
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_high_scores(self):
        """Save high scores to file"""
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f, indent=2)
    
    def start_new_game(self, player_name="Player", min_num=1, max_num=100, max_attempts=7):
        """Initialize a new game"""
        self.player_name = player_name
        self.min_number = min_num
        self.max_number = max_num
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_num, max_num)
        self.attempts = 0
        self.game_active = True
        
        return {
            "status": "game_started",
            "message": f"Welcome {player_name}! I'm thinking of a number between {min_num} and {max_num}.",
            "attempts_left": max_attempts,
            "range": {"min": min_num, "max": max_num}
        }
    
    def make_guess(self, guess):
        """Process a player's guess"""
        if not self.game_active:
            return {"status": "error", "message": "No active game. Start a new game first!"}
        
        try:
            guess = int(guess)
        except ValueError:
            return {"status": "error", "message": "Please enter a valid number!"}
        
        if guess < self.min_number or guess > self.max_number:
            return {
                "status": "error", 
                "message": f"Guess must be between {self.min_number} and {self.max_number}!"
            }
        
        self.attempts += 1
        attempts_left = self.max_attempts - self.attempts
        
        if guess == self.secret_number:
            # Player won!
            self.game_active = False
            score = self.calculate_score()
            self.add_high_score(score)
            
            return {
                "status": "won",
                "message": f"🎉 Congratulations {self.player_name}! You guessed it!",
                "secret_number": self.secret_number,
                "attempts_used": self.attempts,
                "score": score,
                "game_over": True
            }
        
        elif attempts_left == 0:
            # Game over - no attempts left
            self.game_active = False
            return {
                "status": "lost",
                "message": f"💀 Game Over! The number was {self.secret_number}.",
                "secret_number": self.secret_number,
                "attempts_used": self.attempts,
                "game_over": True
            }
        
        else:
            # Give hint and continue
            if guess < self.secret_number:
                hint = "📈 Too low! Try a higher number."
            else:
                hint = "📉 Too high! Try a lower number."
            
            return {
                "status": "continue",
                "message": hint,
                "attempts_left": attempts_left,
                "attempts_used": self.attempts,
                "last_guess": guess
            }
    
    def calculate_score(self):
        """Calculate score based on attempts used"""
        # Better score for fewer attempts
        base_score = 1000
        penalty_per_attempt = 100
        score = max(100, base_score - (self.attempts - 1) * penalty_per_attempt)
        return score
    
    def add_high_score(self, score):
        """Add score to high scores list"""
        high_score_entry = {
            "player": self.player_name,
            "score": score,
            "attempts": self.attempts,
            "date": datetime.now().isoformat(),
            "range": f"{self.min_number}-{self.max_number}"
        }
        
        self.high_scores.append(high_score_entry)
        # Sort by score (descending) and keep top 10
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_high_scores()
    
    def get_high_scores(self):
        """Return top high scores"""
        return {
            "status": "success",
            "high_scores": self.high_scores[:10]
        }
    
    def get_game_status(self):
        """Get current game status"""
        if not self.game_active:
            return {"status": "no_game", "message": "No active game"}
        
        return {
            "status": "active",
            "player": self.player_name,
            "attempts_used": self.attempts,
            "attempts_left": self.max_attempts - self.attempts,
            "range": {"min": self.min_number, "max": self.max_number}
        }

# Game API/Interface functions
def create_game_session():
    """Factory function to create a new game session"""
    return NumberGuessingGame()

# Example usage and CLI interface
def play_console_game():
    """Console-based game interface for testing"""
    game = create_game_session()
    
    print("🎮 Welcome to the Number Guessing Game!")
    print("=" * 40)
    
    # Get player name
    name = input("Enter your name: ").strip() or "Player"
    
    # Game difficulty selection
    print("\nSelect difficulty:")
    print("1. Easy (1-50, 8 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard (1-200, 6 attempts)")
    
    choice = input("Choose (1-3): ").strip()
    
    if choice == "1":
        result = game.start_new_game(name, 1, 50, 8)
    elif choice == "3":
        result = game.start_new_game(name, 1, 200, 6)
    else:
        result = game.start_new_game(name, 1, 100, 7)
    
    print(f"\n{result['message']}")
    print(f"You have {result['attempts_left']} attempts.")
    
    # Game loop
    while game.game_active:
        try:
            guess = input("\nEnter your guess: ")
            result = game.make_guess(guess)
            
            print(result['message'])
            
            if result['status'] == 'continue':
                print(f"Attempts left: {result['attempts_left']}")
            elif result['status'] in ['won', 'lost']:
                if result['status'] == 'won':
                    print(f"Your score: {result['score']}")
                break
                
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
    
    # Show high scores
    high_scores = game.get_high_scores()
    if high_scores['high_scores']:
        print("\n🏆 High Scores:")
        print("-" * 50)
        for i, score in enumerate(high_scores['high_scores'][:5], 1):
            print(f"{i}. {score['player']} - {score['score']} pts ({score['attempts']} attempts)")

if __name__ == "__main__":
    play_console_game()