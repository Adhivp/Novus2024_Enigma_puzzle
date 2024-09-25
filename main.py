import tkinter as tk
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk
import os

base_dir = os.path.dirname(__file__)

class NovusPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Novus Puzzle Competition 2K24")
        self.root.attributes('-fullscreen', True)  # Fullscreen
        self.points = 0  # Initialize points
        self.current_game = None 
        self.timer_duration_sudoku = 420  #  7 minutes 
        self.timer_duration_2048 = 300 # 5 minutes
        
        # Load background image
        self.bg_image = Image.open(os.path.join(base_dir, "assests", "novus.png"))  # Path to the image you uploaded
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Create a Canvas widget to hold the background image
      # Create a Canvas widget to hold the background image
        self.bg_canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(), highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")


        # Timer label (permanently displayed on all pages)
        self.timer_label = tk.Label(self.root, font=("Fira Code", 20, "bold"), bg="#222831", fg="#FFD369")  # Sleek, techy font
        self.timer_label.place(x=self.root.winfo_screenwidth() - 300, y=20)
 
        # Score label (permanently displayed on all pages)
        self.score_label = tk.Label(self.root, text=f"Score: {self.points}", font=("Fira Code", 20, "bold"), bg="#222831", fg="#FFD369")
        self.score_label.place(x=20, y=20)

        # Start with the first page
        self.first_page()

    def first_page(self):
        self.clear_frame()
        title_label = tk.Label(self.root, text="Novus Puzzle Competition 2K24", font=("Orbitron", 34, "bold"), bg="#393E46", fg="#FFD369")
        title_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Center the title

        start_button = tk.Button(self.root, text="Click to Start Game", font=("Orbitron", 20, "bold"), bg="#00ADB5", fg="white", activebackground="#393E46", activeforeground="#FFD369", command=self.second_page)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def second_page(self):
        self.clear_frame()
        self.current_game = 'sudoku'  # Ensure current_game is set to 'sudoku' for the timer
        self.start_time = time.time()  # Start the timer
        self.update_timer()  # Begin updating the timer for Sudoku

        game_name_label = tk.Label(self.root, text="Sudoku Game", font=("Orbitron", 28, "bold"), bg="#393E46", fg="#FFD369")
        game_name_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        rules_label = tk.Label(self.root, text="Sudoku Rules:\n\n1. Fill the grid.\n2. Ensure each row, column, and 3x3 box contains numbers 1-9.", font=("Fira Code", 18), bg="#222831", fg="#FFD369", justify=tk.LEFT)
        rules_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        next_button = tk.Button(self.root, text="Next", font=("Orbitron", 18), bg="#00ADB5", fg="white", activebackground="#393E46", activeforeground="#FFD369", command=self.third_page)
        next_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


    def third_page(self):
        self.clear_frame()
        self.current_game = 'sudoku'  # Track that we're in the Sudoku game
        SudokuApp(self.root, self)  # Load the Sudoku game

    def fourth_page(self):
        self.clear_frame()
        self.current_game = '2048'  # Now playing the 2048 game
        self.start_time = time.time()  # Start the timer for 2048
        self.update_timer()

        game_name_label = tk.Label(self.root, text="2048 Game", font=("Orbitron", 28, "bold"), bg="#393E46", fg="#FFD369")
        game_name_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        rules_label = tk.Label(self.root, text="2048 Rules:\n\n1. Merge tiles to reach 1024.\n2. Combine similar tiles to grow.", font=("Fira Code", 18), bg="#222831", fg="#FFD369", justify=tk.LEFT)
        rules_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        next_button = tk.Button(self.root, text="Next", font=("Orbitron", 18), bg="#00ADB5", fg="white", activebackground="#393E46", activeforeground="#FFD369", command=self.fifth_page)
        next_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def fifth_page(self):
        self.clear_frame()
        self.load_2048_game()

    def load_2048_game(self):
        Game2048(self.root, self)  # Passing root and main app for score tracking

    def update_timer(self):
        if self.current_game is None:  # Check if there is an active game
            self.timer_label.config(text="No active game to track.")
            return

        elapsed_time = time.time() - self.start_time
        remaining_time = 0  # Initialize remaining_time to avoid uninitialized error

        if self.current_game == 'sudoku':
            remaining_time = self.timer_duration_sudoku - int(elapsed_time)
        elif self.current_game == '2048':
            remaining_time = self.timer_duration_2048 - int(elapsed_time)

        # Now we can safely use remaining_time since it has been initialized
        if remaining_time > 0:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)  # Update timer every second
        else:
            self.timer_label.config(text="Time's up!")
            messagebox.showinfo("Time's up!", "The time is over!")
            if self.current_game == 'sudoku':
                self.credit_points(0)  # Credit points for remaining time
                self.fourth_page()  # Proceed to the next game
            else:
                self.end_game()  # Handle game over scenario


    def end_game(self):
        messagebox.showinfo("Game Over", f"Final Score: {self.points}")
        self.root.quit()

    def credit_points(self, remaining_time):
        if remaining_time > 240:
            self.points += 18
        elif remaining_time > 180:
            self.points += 16
        elif remaining_time > 120:
            self.points += 14
        elif remaining_time > 60:
            self.points += 12
        else:
            self.points += 10
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.points}")

    def clear_frame(self):
        # Clear all widgets except the timer and score labels
        for widget in self.root.winfo_children():
            if widget not in (self.bg_canvas, self.timer_label, self.score_label):
                widget.destroy()


class SudokuApp:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app  # Reference to the main app
        self.root.title("Sudoku Game")

        # Frame to center the Sudoku game
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the grid
        self.grid = [[0] * 9 for _ in range(9)]
        self.entries = [[None] * 9 for _ in range(9)]

        self.create_widgets()
        self.generate_puzzle()

    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.frame, width=3, font=('Arial', 18), borderwidth=1, relief='solid', justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                self.entries[i][j] = entry

        self.check_button = tk.Button(self.frame, text="Check", command=self.check_solution)
        self.check_button.grid(row=10, columnspan=9, pady=5)

        self.skip_button = tk.Button(self.frame, text="Skip", command=self.skip_to_next_game)
        self.skip_button.grid(row=11, column=3, columnspan=3, pady=5, sticky=tk.E)

        self.next_button = tk.Button(self.frame, text="Next", state=tk.DISABLED, command=self.main_app.fourth_page)
        self.next_button.grid(row=11, column=6, columnspan=3, pady=5, sticky=tk.E)

    def skip_to_next_game(self):
        self.main_app.fourth_page()

    def generate_puzzle(self):
        self.solve(self.grid)

        for _ in range(50):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            self.grid[row][col] = 0

        self.update_grid_display()

    def update_grid_display(self):
        for i in range(9):
            for j in range(9):
                value = self.grid[i][j]
                self.entries[i][j].delete(0, tk.END)
                if value != 0:
                    self.entries[i][j].insert(0, str(value))
                    self.entries[i][j].config(state='disabled')

    def check_solution(self):
        user_grid = [[0] * 9 for _ in range(9)]

        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value:
                    try:
                        value = int(value)
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Please enter only numbers.")
                        return
                    user_grid[i][j] = value
                else:
                    messagebox.showinfo("Incomplete", "Please complete the Sudoku.")
                    return

        if self.is_complete(user_grid) and self.is_valid_sudoku(user_grid):
            messagebox.showinfo("Congratulations", "You successfully completed the Sudoku!")
            elapsed_time = time.time() - self.main_app.start_time
            remaining_time = self.main_app.timer_duration - int(elapsed_time)
            self.main_app.credit_points(remaining_time)
            self.next_button.config(state=tk.NORMAL)  # Enable the Next button
        else:
            messagebox.showinfo("Incorrect", "The Sudoku is incorrect. Try again.")

    def is_complete(self, grid):
        for row in grid:
            if 0 in row:
                return False
        return True

    def is_valid_sudoku(self, grid):
        def is_valid_row(row):
            return len(set(row)) == 9

        def is_valid_col(col):
            return len(set(col)) == 9

        def is_valid_box(box):
            return len(set(box)) == 9

        for i in range(9):
            if not is_valid_row([grid[i][j] for j in range(9)]):
                return False
            if not is_valid_col([grid[j][i] for j in range(9)]):
                return False

        for box_x in range(3):
            for box_y in range(3):
                box = [grid[i][j] for i in range(box_y*3, (box_y+1)*3) for j in range(box_x*3, (box_x+1)*3)]
                if not is_valid_box(box):
                    return False

        return True

    def find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, grid, num, pos):
        row, col = pos

        for i in range(9):
            if grid[row][i] == num and i != col:
                return False

        for i in range(9):
            if grid[i][col] == num and i != row:
                return False

        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, (box_y + 1) * 3):
            for j in range(box_x * 3, (box_x + 1) * 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self, grid):
        empty = self.find_empty(grid)
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(grid, num, (row, col)):
                grid[row][col] = num

                if self.solve(grid):
                    return True

                grid[row][col] = 0

        return False


class Game2048:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app  # Reference to the main app
        self.score = 0  # Initialize the game score
        self.root.title("2048 Game")

        # Frame to center the 2048 game
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the grid
        self.grid = [[0] * 4 for _ in range(4)]
        self.tiles = [[None] * 4 for _ in range(4)]

        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        for i in range(4):
            for j in range(4):
                tile = tk.Label(self.frame, text="", width=4, height=2, font=("Arial", 24), borderwidth=2, relief="solid", anchor="center")
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[i][j] = tile

        self.restart_button = tk.Button(self.frame, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.quit_game)
        self.quit_button.grid(row=4, column=2, columnspan=2, pady=10)

        self.root.bind("<KeyPress>", self.handle_keypress)

    def initialize_game(self):
        self.add_random_tile()
        self.add_random_tile()
        self.update_grid_display()

    def add_random_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = random.choice([2, 4])

    def update_grid_display(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                if value != 0:
                    self.tiles[i][j].config(text=str(value))
                else:
                    self.tiles[i][j].config(text="")

    def slide_and_combine(self, row):
        new_row = [value for value in row if value != 0]
        combined_row = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                combined_value = new_row[i] * 2
                combined_row.append(combined_value)
                self.score += combined_value
                
                # Credit points based on the combined value
                if combined_value == 64:
                    self.main_app.points += 5
                    self.main_app.update_score()
                elif combined_value == 128:
                    self.main_app.points += 10
                    self.main_app.update_score()
                
                skip = True
            else:
                combined_row.append(new_row[i])
        combined_row += [0] * (len(row) - len(combined_row))
        return combined_row, self.score

    def move_left(self):
        new_grid = []
        for row in self.grid:
            new_row, _ = self.slide_and_combine(row)
            new_grid.append(new_row)
        self.grid = new_grid

    def move_right(self):
        new_grid = []
        for row in self.grid:
            new_row, _ = self.slide_and_combine(row[::-1])
            new_grid.append(new_row[::-1])
        self.grid = new_grid

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_down(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        self.move_right()
        self.grid = [list(row) for row in zip(*self.grid)]

    def handle_keypress(self, event):
        key = event.keysym

        if key == "Left":
            self.move_left()
        elif key == "Right":
            self.move_right()
        elif key == "Up":
            self.move_up()
        elif key == "Down":
            self.move_down()

        self.add_random_tile()
        self.update_grid_display()

        if self.is_game_over():
            messagebox.showinfo("Game Over", f"Game Over!")
            self.main_app.end_game()  # Exit the game when the game is over

    def restart_game(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.main_app.points = 0  # Reset points
        self.initialize_game()

    def quit_game(self):
        self.main_app.end_game()  # Use main app's end_game method to exit

    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False

        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j + 1] or self.grid[j][i] == self.grid[j + 1][i]:
                    return False

        return True
if __name__ == "__main__":
    root = tk.Tk()
    app = NovusPuzzleApp(root)
    root.mainloop()
