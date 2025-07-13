# MaganePK Python Project 1: Board Game

Welcome to the repository for our tactical board game project! This is a Python-based, two-player strategy board game featuring both text and GUI modes. The game is designed for players who enjoy deep strategy, tactical movement, and unique piece abilities.

---

## 📸 Screenshots

<
Add your screenshots below. Example:
![Text Mode Screenshot](/gameBoard/images/text.png)
![GUI Mode Screenshot](/gameBoard/images/gui.png)


---

## 🎮 Game Features

- **Two-player tactical gameplay**: Compete as "light" or "dark" teams.
- **Multiple piece types**: Each with unique movement and abilities.
- **Obstacles and sinks**: Add complexity and challenge to the board.
- **Text and GUI modes**: Play in the terminal or with a graphical interface.
- **Configurable board size**: Choose between 8x8, 9x9, or 10x10 boards.
- **Custom board setup**: Define your own starting positions via input files.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **Tkinter** (for GUI mode)
- **Standard Library** (no external dependencies for core game)

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/MaganePK-Python-project1-Board-Game.git
cd MaganePK-Python-project1-Board-Game
```

### 2. Create a Virtual Environment (Recommended)

```sh
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Required Libraries

For GUI mode, ensure Tkinter is installed (usually included with Python).  
If not, install with:

```sh
pip install tk
```

### 4. How to Run

**Text Mode:**
```sh
python -m gameBoard.gameBoard 8 8 0
```

**GUI Mode:**
```sh
python -m gameBoard.gameBoard 8 8 1
```

Replace `8 8` with your desired board size (`8`, `9`, or `10`).  
The third argument is the mode: `0` for text, `1` for GUI.

#### Using an Input File

To use a custom board setup and moves:

```sh
Get-Content input.txt | python -m gameBoard.gameBoard 8 8 0
```

---

## 📄 Input File Format

**Board setup:**
```
s 1 0 0      # Place a sink at (0,0)
x 2 2        # Place an obstacle at (2,2)
l a 3 3      # Place a light small piece at (3,3)
d a 4 4      # Place a dark small piece at (4,4)
#            # End setup with #
```

**Moves:**
```
row col direction   # e.g., 3 3 r moves the piece at (3,3) right
```

---

## 📝 Project Structure

```
gameBoard/
    gameBoard.py         # Main game logic and entry point
    gameBoardText.py     # Text mode logic
    gameBoardGUI.py      # GUI mode logic (if implemented)
    input.txt            # Example input file
README.md
```

---

## ⚠️ Known Issues

- Move validation is not fully comprehensive.
- Special moves (like bombs) are not yet implemented.

---

## 🤝 Contributing

Pull requests and suggestions are welcome! Please open an issue to discuss changes or improvements.

---

## 📧 Contact

For questions or feedback, open an issue or contact the project maintainers.

---

You can now add images/screenshots in the "Screenshots" section by uploading them to your repo and referencing their paths.
