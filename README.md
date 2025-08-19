# Number Guessing Game 🎲
A fun and interactive Number Guessing Game built in Python 🐍.
Test your luck and logic as you try to guess the secret number within limited attempts.
Includes difficulty levels, scoring system, and a high score tracker.

Features
🔢 Randomly generated secret number.
🎚️ Difficulty levels:
Easy → Range 1-50 with 8 attempts.
Medium → Range 1-100 with 7 attempts.
Hard → Range 1-200 with 6 attempts.
🏆 High scores saved in high_scores.json.
💯 Scoring system → Higher score for fewer attempts.
🎮 Console-based interactive gameplay.

1. Clone the Repository
git clone https://github.com/your-username/NGG.git
cd NGG

2. Run the Game
python3 game.py

📖 Gameplay Instructions
Enter your name.
Choose a difficulty level.
Try to guess the secret number within the allowed attempts.
Get hints:
📈 Too low → Guess higher.
📉 Too high → Guess lower.
Win 🎉 if you guess correctly before attempts run out!
Check the 🏆 High Scores after the game.

NGG/
│── game.py             # Main game logic
│── high_scores.json    # Stores high scores (auto-generated)
│── README.md           # Project documentation


🎮 Welcome to the Number Guessing Game!
========================================
Enter your name: Snehal

Select difficulty:
1. Easy (1-50, 8 attempts)
2. Medium (1-100, 7 attempts)
3. Hard (1-200, 6 attempts)

Choose (1-3): 2

Welcome Snehal! I'm thinking of a number between 1 and 100.
You have 7 attempts.

Enter your guess: 45
📉 Too high! Try a lower number.
Attempts left: 6


