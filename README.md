# 🎱 8-Ball Pool Game

Welcome to the **8-Ball Pool Game**! This is a Python-based simulation of the classic 8-ball pool game, complete with realistic physics, smooth gameplay, and an attractive user interface. Whether you're a seasoned player or just looking for some fun, this game provides an engaging experience.

## 📖 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [License](#license)
- [Contributing](#contributing)

## 🌟 Features

- **Realistic Physics**: The game implements realistic ball collisions and movements to simulate the experience of playing on a real pool table.
- **Textured Table and Balls**: The game features a visually appealing pool table and ball textures, enhancing the game's overall aesthetics.
- **Smooth Gameplay**: Responsive controls and intuitive gameplay mechanics.
- **Player Indication**: The game clearly indicates whose turn it is and displays the type of balls (solid or stripes) assigned to each player.
- **Foul Detection**: The game detects and displays fouls according to standard 8-ball pool rules.

## 📸 Screenshots

<img width="796" alt="screenshot1" src="https://github.com/user-attachments/assets/2359598d-96a6-4d19-9ad9-53eb5acb4725">
<img width="796" alt="screenshot2" src="https://github.com/user-attachments/assets/7e4737bf-a92d-47fa-9380-0124ba3391ee">
<img width="796" alt="screenshot3" src="https://github.com/user-attachments/assets/f13a663c-f7e9-44c8-b88e-dd05f8a626fa">
<img width="796" alt="screenshot4" src="https://github.com/user-attachments/assets/5e3af7e3-2c5c-4b18-9cd6-b5655cb7d8fd">


## 🛠️ Installation

To run this game locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hbarquanta/8-Ball-Pool-Game.git
   ```
   
2. **Navigate to the Project Directory**:
   ```bash
   cd 8-Ball-Pool-Game
   ```

3. **Install the Dependencies**:
   - Make sure you have Python installed.
   - Install required libraries using pip:
     ```bash
     pip install pygame numpy
     ```

4. **Run the Game**:
   ```bash
   python main.py
   ```

## 🎮 How to Play

- **Objective**: The goal is to pocket all of your assigned balls (solids or stripes) and then legally pocket the 8-ball.
- **Controls**:
  - Use your mouse to aim the cue.
  - Adjust the power of your shot using the power slider.
  - Click "Shoot" to take your shot.
  
## 🕹️ Game Rules

- **Player 1 always starts**.
- Players must first pocket all of their assigned balls (solids or stripes) before attempting to pocket the 8-ball.
- **Turn Switching**:
  - A player continues to play as long as they legally pocket one of their assigned balls.
  - If a player fails to pocket a ball or commits a foul, their turn ends.
- **Fouls**:
  - Pocketing the cue ball.
  - Pocketing an opponent's ball.
  - Failing to hit any balls with the cue ball.
- The game ends when the 8-ball is legally pocketed by the player who has pocketed all their assigned balls.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request. Please ensure your code follows the project's coding standards.
