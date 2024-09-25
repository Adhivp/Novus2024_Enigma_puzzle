import tkinter as tk
from tkinter import messagebox
from turtle import *
from freegames import path
from random import shuffle

# Points and game completion status
points = 20  # Start with 20 points
game_completed = False
time_left = 600  # 10 minutes in seconds
time_elapsed = 0  # Track elapsed time to adjust points every minute

# Function to calculate points
def calculate_points():
    global points
    return points

# Start the game (First page)
def start_game(root):
    root.destroy()  # Close start screen
    rules_page()  # Open rules page

# Display the rules page
def rules_page():
    rules_window = tk.Tk()
    rules_window.title("Game Rules")

    # Game rules text
    tk.Label(rules_window, text="Game Rules", font=("Arial", 24)).pack(pady=20)
    tk.Label(rules_window, text="1. Complete the game to earn points.", font=("Arial", 14)).pack(pady=5)

    # Score label
    score_label = tk.Label(rules_window, text=f"Score: {points}", font=("Arial", 14))
    score_label.pack(pady=10)

    # Next button to start the game
    next_button = tk.Button(rules_window, text="Next", command=lambda: start_puzzle_game(rules_window))
    next_button.pack(pady=20)

    rules_window.mainloop()

# Timer function
def update_timer():
    global time_left, time_elapsed, points, game_completed
    if time_left > 0 and not game_completed:
        time_left -= 1
        time_elapsed += 1

        # Decrease points every minute (every 60 seconds)
        if time_elapsed % 60 == 0 and points > 0:
            points -= 1
            score_label.config(text=f"Score: {points}")

        minutes, seconds = divmod(time_left, 60)
        timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
        screen.ontimer(update_timer, 1000)
    elif time_left <= 0:
        final_score_display()
        bye()  # Close the turtle graphics window

# Display the final score when the game ends
def final_score_display():
    global points
    messagebox.showinfo("Time's Up!", f"Time is up! Your final score is {points} points.")

# Puzzle Game (Memory Game from turtle)
def start_puzzle_game(rules_window):
    global game_completed
    rules_window.destroy()  # Close the rules window

    # Initialize the turtle graphics window
    screen = Screen()
    screen.setup(width=800, height=850)  # Increased height to accommodate the timer
    screen.title("Puzzle Game")
    car = path("car.gif")
    tiles = list(range(32)) * 2
    shuffle(tiles)
    state = {"mark": None}
    hide = [True] * 64

    def square(x, y):
        "Draw white square with black outline at (x, y)."
        up()
        goto(x, y)
        down()
        color("black", "white")
        begin_fill()
        for count in range(4):
            forward(50)
            left(90)
        end_fill()

    def index(x, y):
        "Convert (x, y) coordinates to tiles index."
        return int((x + 200) // 50 + ((y + 200) // 50) * 8)

    def xy(count):
        "Convert tiles count to (x, y) coordinates."
        return (count % 8) * 50 - 200, (count // 8) * 50 - 200

    def tap(x, y):
        "Update mark and hidden tiles based on tap."
        spot = index(x, y)
        # Ensure the tap is within valid bounds
        if spot < 0 or spot >= len(tiles):
            return  # Ignore taps outside the grid
        mark = state["mark"]
        if mark is None or mark == spot or tiles[mark] != tiles[spot]:
            state["mark"] = spot
        else:
            hide[spot] = False
            hide[mark] = False
            state["mark"] = None

        # Check if the game is completed
        if all(not hidden for hidden in hide):
            global game_completed
            game_completed = True
            global points
            points = calculate_points()
            messagebox.showinfo("Game Completed", f"You've earned {points} points!")
            bye()  # Close the turtle graphics window

    def draw():
        "Draw image and tiles."
        clear()
        goto(0, 0)
        shape(car)
        stamp()
        for count in range(64):
            if hide[count]:
                x, y = xy(count)
                square(x, y)
        mark = state["mark"]
        if mark is not None and hide[mark]:
            x, y = xy(mark)
            up()
            goto(x + 2, y)
            color("black")
            write(tiles[mark], font=("Arial", 30, "normal"))

        update()
        ontimer(draw, 100)

    # Shuffle and start the game
    addshape(car)
    hideturtle()
    tracer(False)
    onscreenclick(tap)
    update_timer()  # Start the timer
    draw()
    done()

# Main Interface
def main():
    root = tk.Tk()
    root.title("Final Round - Nova's Puzzle Competition")

    # Title and button
    tk.Label(root, text="Final Round", font=("Arial", 32)).pack(pady=20)
    tk.Label(root, text="Nova's Puzzle Competition", font=("Arial", 24)).pack(pady=20)

    start_button = tk.Button(root, text="Start the Game", font=("Arial", 16), command=lambda: start_game(root))
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    screen = Screen()
    timer_label = tk.Label(screen._root, text="Time Left: 10:00", font=("Arial", 16))
    timer_label.pack()
    score_label = tk.Label(screen._root, text=f"Score: {points}", font=("Arial", 16))
    score_label.pack()
    main()
