import tkinter as tk
from tkinter import messagebox

# Letter points for scoring
LETTER_POINTS = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 
    'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 
    'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 
    'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}  # A-Z

# Load dictionary from file
def load_dictionary(filepath):
    try:
        with open(filepath, "r") as file:
            return set(word.strip().upper() for word in file if word.strip())
    except FileNotFoundError:
        messagebox.showerror("Error", f"Dictionary file '{filepath}' not found!")
        return set()

class WordSquareGame:
    def __init__(self, master, grid_size=5, target_score=10, initial_letters=None, dictionary_file="words.txt"):
        self.master = master
        self.grid_size = grid_size
        self.target_score = target_score
        self.grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
        self.buttons = []
        self.initial_letters = initial_letters or {}
        self.dictionary = load_dictionary(dictionary_file)
        self.current_direction = "horizontal"  # Default typing direction
        self.current_row, self.current_col = 0, 0
        self.init_ui()

    def init_ui(self):
        self.master.title("Word Square Game")
        self.master.configure(bg="#f5f5f5")

        frame = tk.Frame(self.master, bg="#f5f5f5")
        frame.grid(row=0, column=0, padx=10, pady=10)

        # Grid Buttons
        for r in range(self.grid_size):
            row_buttons = []
            for c in range(self.grid_size):
                value = self.initial_letters.get((r, c), " ")
                is_locked = (r, c) in self.initial_letters
                btn = tk.Entry(
                    frame,
                    font=("Arial", 18),
                    justify="center",
                    bg="#ffffff" if not is_locked else "#d3d3d3",
                    fg="#333333",
                    width=2,
                    relief="groove",
                )
                btn.insert(0, value)
                if is_locked:
                    btn.config(state="readonly")  # Make initial letters readonly
                btn.bind("<KeyRelease>", lambda e, r=r, c=c: self.type_letter(e, r, c))
                btn.grid(row=r, column=c, padx=2, pady=2, ipadx=5, ipady=5)
                row_buttons.append(btn)
                self.grid[r][c] = value
            self.buttons.append(row_buttons)

        # Direction label
        self.direction_label = tk.Label(
            self.master, text="Direction: Horizontal", font=("Arial", 14), bg="#f5f5f5", fg="#333333"
        )
        self.direction_label.grid(row=1, column=0, pady=10)

        # Score label
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Arial", 16), bg="#f5f5f5", fg="#333333")
        self.score_label.grid(row=2, column=0, pady=10)

        # Check button
        check_btn = tk.Button(
            self.master,
            text="Check Words",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="#ffffff",
            command=self.check_words,
        )
        check_btn.grid(row=3, column=0, pady=10)

        # Letter Points Display
        points_frame = tk.Frame(self.master, bg="#f5f5f5", relief="groove", bd=2)
        points_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        tk.Label(points_frame, text="Letter Points", font=("Arial", 14, "bold"), bg="#f5f5f5").grid(row=0, column=0, pady=5)
        for i, letter in enumerate(sorted(LETTER_POINTS.keys())):
            tk.Label(
                points_frame,
                text=f"{letter}: {LETTER_POINTS[letter]}",
                font=("Arial", 12),
                bg="#f5f5f5",
            ).grid(row=i + 1, column=0, sticky="w", padx=5)

        # Bind arrow keys for direction switching
        self.master.bind("<Right>", self.set_direction_horizontal)
        self.master.bind("<Left>", self.set_direction_horizontal)
        self.master.bind("<Down>", self.set_direction_vertical)
        self.master.bind("<Up>", self.set_direction_vertical)

    def set_direction_horizontal(self, event=None):
        """Set typing direction to horizontal."""
        self.current_direction = "horizontal"
        self.direction_label.config(text="Direction: Horizontal")

    def set_direction_vertical(self, event=None):
        """Set typing direction to vertical."""
        self.current_direction = "vertical"
        self.direction_label.config(text="Direction: Vertical")

    def type_letter(self, event, row, col):
        """Type a letter or handle backspace and move in the current direction."""
        if event.keysym == "BackSpace":
            self.handle_backspace(row, col)
        else:
            value = event.char.upper()
            if value.isalpha() and len(value) == 1:
                self.grid[row][col] = value
                self.buttons[row][col].delete(0, tk.END)
                self.buttons[row][col].insert(0, value)
                self.move_to_next_cell(row, col)


    def handle_backspace(self, row, col):
        """Handle the backspace key to clear letters in the current direction."""
        self.buttons[row][col].delete(0, tk.END)
        self.grid[row][col] = " "  # Clear the current cell

        if self.current_direction == "horizontal":
            prev_col = (col - 1) % self.grid_size
            prev_row = row if col != 0 else (row - 1) % self.grid_size
        elif self.current_direction == "vertical":
            prev_row = (row - 1) % self.grid_size
            prev_col = col if row != 0 else (col - 1) % self.grid_size
        else:
            prev_row, prev_col = row, col

        self.buttons[prev_row][prev_col].focus_set()


    def move_to_next_cell(self, row, col):
        """Move to the next cell based on the current direction."""
        if self.current_direction == "horizontal":
            next_col = (col + 1) % self.grid_size
            next_row = row if next_col != 0 else (row + 1) % self.grid_size
        elif self.current_direction == "vertical":
            next_row = (row + 1) % self.grid_size
            next_col = col if next_row != 0 else (col + 1) % self.grid_size
        else:
            next_row, next_col = row, col

        self.buttons[next_row][next_col].focus_set()

    def check_words(self):
        # Collect all rows and columns as words
        rows = ["".join(row).strip() for row in self.grid]
        cols = ["".join(col).strip() for col in zip(*self.grid)]

        # Validate words against the dictionary and length criteria
        valid_rows = [row for row in rows if len(row) >= 3 and row in self.dictionary]
        valid_cols = [col for col in cols if len(col) >= 3 and col in self.dictionary]

        # Calculate score only for valid words
        valid_letters = [ch for word in valid_rows + valid_cols for ch in word]
        current_score = sum(LETTER_POINTS.get(ch, 0) for ch in valid_letters)

        self.score_label.config(text=f"Score: {current_score}")

        # Result message
        if valid_rows or valid_cols:
            messagebox.showinfo(
                "Check Complete",
                f"Valid Words:\nRows: {valid_rows}\nColumns: {valid_cols}\nCurrent Score: {current_score}",
            )
        else:
            messagebox.showinfo("Check Complete", "No valid words found!")

        # Check win condition
        if current_score >= self.target_score:
            messagebox.showinfo("Congratulations", "You win!")
            self.reset_game()

    def reset_game(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) in self.initial_letters:
                    self.grid[r][c] = self.initial_letters[(r, c)]
                    self.buttons[r][c].delete(0, tk.END)
                    self.buttons[r][c].insert(0, self.grid[r][c])
                else:
                    self.grid[r][c] = " "
                    self.buttons[r][c].delete(0, tk.END)

        self.score_label.config(text="Score: 0")

# Define initial letters (customizable)
INITIAL_LETTERS = {
    (0, 0): "C",
    (0, 1): "A",
    (0, 2): "T",
    (1, 0): "D",
    (1, 1): "O",
    (1, 2): "G",
}

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = WordSquareGame(root, grid_size=5, target_score=15, initial_letters=INITIAL_LETTERS, dictionary_file="words.txt")
    root.mainloop()
