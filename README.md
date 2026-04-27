# Robot Hello World

A simple Python robot simulation for beginners. Clone, install dependencies, and run!

## Quick Start

```bash
# Step 1: Clone the project
git clone <your-repo-url>
cd robot-hello-world

# Step 2: Install dependencies
pip3 install -r requirements.txt

# Step 3: Run the game
python3 main.py
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Up / W | Move North |
| Arrow Down / S | Move South |
| Arrow Left / A | Move West |
| Arrow Right / D | Move East |
| Space | Scan surroundings (result stays on screen) |
| M | Redraw map |
| R | Reset game |
| Q / ESC | Quit |

## How It Works

- Your robot starts at position (1, 1) facing North
- Use arrow keys (or WASD) to navigate the maze
- Collect all treasures (*) for bonus points
- Reach the goal (G) to win!
- Watch your battery - it drains with each step
- The screen only refreshes when you press a key (scan results won't disappear)

## Dependencies

| Library | Version | What it does |
|---------|---------|-------------|
| colorama | >=0.4.6 | Colored terminal text (works on Windows too) |
| art | >=6.1 | ASCII art text generation (welcome screen) |

Install all at once:
```bash
pip3 install -r requirements.txt
```

## Project Structure

```
robot-hello-world/
  main.py            - Entry point, keyboard controls & game loop
  robot.py           - Robot class (position, movement, battery)
  sensor.py          - Sensor class (scan surroundings)
  world.py           - World/Map class (maze, treasures, goal)
  requirements.txt   - Python dependencies list
  README.md          - This file
```

## Requirements

- Python 3.6+
- Linux / WSL2 terminal (for keyboard input support)
