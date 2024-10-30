import numpy as np
import random
from PIL import Image, ImageDraw
import tkinter as tk

def is_valid(board, row, col, num):
    #Check if placing num at board[row][col] is valid under Sudoku rules.
    if num in board[row, :] or num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def solve_sudoku(board):
    #Solve the Sudoku puzzle using backtracking.#
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row, col] = num
                        if solve_sudoku(board):
                            return True
                        board[row, col] = 0
                return False
    return True

def generate_full_board():
    #Generate a fully solved Sudoku board.#
    board = np.zeros((9, 9), dtype=int)
    solve_sudoku(board)
    return board

def remove_numbers(board, clues):
    #Remove numbers from the board to create a puzzle with a given number of clues.#
    puzzle = board.copy()
    empty_cells = 81 - clues
    while empty_cells > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if puzzle[row, col] != 0:
            puzzle[row, col] = 0
            empty_cells -= 1
    return puzzle

def generate_sudoku_puzzle(clues=30):
    #Generate a Sudoku puzzle with a specified number of clues.#
    board = generate_full_board()
    puzzle = remove_numbers(board, clues)
    return puzzle

def print_board(board):
    #Print the Sudoku board in a readable format.#
    for i in range(9):
        row = " ".join(str(num) if num != 0 else '.' for num in board[i])
        print(row)
    print()

def number_to_color(num):
    #Map Sudoku numbers to colors.#
    color_map = {
        1: (255, 0, 0),      # Red
        2: (0, 255, 0),      # Light Green
        3: (0, 0, 255),      # Blue
        4: (255, 255, 0),    # Yellow
        5: (255, 165, 0),    # Orange
        6: (128, 0, 128),    # Purple
        7: (0, 255, 255),    # Cyan
        8: (255, 192, 203),  # Pink
        9: (6, 64, 43),      # Dark Green
        0: (255, 255, 255)   # White for empty cells
    }
    return color_map.get(num, (255, 255, 255))  # Default to white

def get_difficulty():
    #Display a Tkinter GUI for difficulty selection and return a clue count.
    #NOTE: this is the only time UI is used and therefore all Tkinter is handled in this function
    def set_clues(range_min, range_max):
        nonlocal clues
        clues = random.randint(range_min, range_max)
        root.destroy()

    root = tk.Tk()
    root.title("Select Difficulty")
    root.geometry("250x250")

    clues = None #holds chosen # of clues

    tk.Label(root, text="Choose a difficulty level:", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Easy", command=lambda: set_clues(36, 40), font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Medium", command=lambda: set_clues(32, 35), font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Hard", command=lambda: set_clues(28, 31), font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Expert", command=lambda: set_clues(25, 27), font=("Arial", 12)).pack(pady=5)

    root.mainloop()
    return clues

def create_image(board):
    #Create a visual representation of the Sudoku board.#
    cell_size = 50  # Size of each cell in pixels
    output_img = Image.new('RGB', (cell_size * 9, cell_size * 9), (255, 255, 255))
    draw = ImageDraw.Draw(output_img)

    for i, row in enumerate(board):
        for j, num in enumerate(row):
            color = number_to_color(num)
            top_left = (j * cell_size, i * cell_size)
            bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
            draw.rectangle([top_left, bottom_right], fill=color)

    output_img.save('sudoku_colored_output.png')
    output_img.show()

# Run Program
clues = get_difficulty()
# Adjust this value for difficulty (more clues = easier puzzle)
"""
Easy: 36-40 clues
Medium: 32-35 clues
Hard: 28-31 clues
Expert: 25-27 clues
"""
puzzle = generate_sudoku_puzzle(clues)
print("Generated Sudoku Puzzle:")
print_board(puzzle)
create_image(puzzle)
