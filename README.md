# Gaming Environment Setup Script

This Python script automatically arranges windows and launches applications to create a clean gaming setup with one click.

## Features
- Detects and positions windows based on their titles  
- Automatically launches Chrome or other applications  
- Moves and resizes windows across multiple monitors  
- Creates a consistent layout every time

## File
- **gaming.py** – the main script

## How to Run
Run the script from the console:

```bash
python gaming.py

## Optional: Run with a .bat file
If you prefer starting the script with a double-click, create a file named `start_gaming.bat` in the same directory with the following content:

```bat
@echo off
python "%~dp0gaming.py"
