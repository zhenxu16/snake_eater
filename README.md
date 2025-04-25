# Snake_eater 🐍
This is my first game project, created as a class assignment to present to my instructor.   It was built using Python, with the Tkinter library for the GUI.

### Features:
- The player has **3 lives**. Colliding with the wall will result in losing a life.
- Eating a fruit will **increase the snake’s length**.
- The game uses a **countdown timer**. If the timer reaches zero, the game is over immediately.
- After the game ends, it displays the **highest score** and the **longest snake length** achieved during that play session.

## Tech Stack 🛠
- Python
- Tkinter (for GUI)

## Installation
1. Make sure Python is installed on your system.
2. If tkinter is not available on your system, here’s how you can install it depending on your operating system.
### For some example
##### Linux (Debian/Ubuntu)
```bash
sudo apt-get install python3-tk
```
##### Linux (Fedora)
```bash
sudo dnf install python3-tkinter
```
##### Linux (Arch Linux / Manjaro)
```bash
sudo pacman -S tk
```
After installation, try running
```bash
import tkinter
tkinter._test()
```
If a small window appears, tkinter is working properly.
