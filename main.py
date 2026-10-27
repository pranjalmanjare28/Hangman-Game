
import tkinter as tk
import random

# Word bank: word -> category and clue
WORDS = {
    "TIGER": ("Animals", "A striped wild cat"),
    "ELEPHANT": ("Animals", "A large animal with a trunk"),
    "RABBIT": ("Animals", "A small animal with long ears"),
    "PYTHON": ("Technology", "A popular programming language"),
    "KEYBOARD": ("Technology", "Used to type on a computer"),
    "ROBOT": ("Technology", "A machine that can perform tasks"),
    "PIZZA": ("Food", "A round dish with cheese and toppings"),
    "BURGER": ("Food", "A sandwich with a patty"),
    "INDIA": ("Countries", "A country in South Asia"),
    "JAPAN": ("Countries", "A country famous for Mount Fuji"),
}

BG = "#F5F3FF"
PURPLE = "#6C4AB6"
DARK = "#29243A"
GREEN = "#25855A"
RED = "#D94F70"
WHITE = "#FFFFFF"


class Hangman:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman - Word Challenge")
        self.root.geometry("540x760")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.word = ""
        self.category = ""
        self.clue = ""
        self.guessed = set()
        self.wrong = 0
        self.over = False
        self.keyboard_buttons = {}

        tk.Label(
            root, text="HANGMAN",
            font=("Arial", 25, "bold"),
            bg=BG, fg=PURPLE
        ).pack(pady=(15, 2))

        tk.Label(
            root, text="Guess the word, one letter at a time",
            font=("Arial", 10),
            bg=BG, fg="#777087"
        ).pack(pady=(0, 8))

        # Drawing area for the stick figure and gallows
        self.canvas = tk.Canvas(
            root, width=300, height=245,
            bg=WHITE, highlightthickness=0
        )
        self.canvas.pack(pady=5)

        self.category_label = tk.Label(
            root, font=("Arial", 11, "bold"),
            bg=BG, fg=PURPLE
        )
        self.category_label.pack(pady=(8, 2))

        self.clue_label = tk.Label(
            root, font=("Arial", 11),
            bg=BG, fg=DARK, wraplength=450
        )
        self.clue_label.pack(pady=3)

        self.word_label = tk.Label(
            root, font=("Courier New", 22, "bold"),
            bg=BG, fg=DARK
        )
        self.word_label.pack(pady=10)

        self.status_label = tk.Label(
            root, font=("Arial", 10, "bold"),
            bg=BG, fg="#777087"
        )
        self.status_label.pack(pady=2)

        # QWERTY keyboard
        self.keyboard_frame = tk.Frame(root, bg=BG)
        self.keyboard_frame.pack(pady=12)

        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        for row_index, letters in enumerate(rows):
            row_frame = tk.Frame(self.keyboard_frame, bg=BG)
            row_frame.pack(pady=3)

            for letter in letters:
                button = tk.Button(
                    row_frame,
                    text=letter,
                    font=("Arial", 11, "bold"),
                    width=3,
                    height=1,
                    bg=WHITE,
                    fg=DARK,
                    activebackground="#E8DFFF",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda ch=letter: self.guess(ch)
                )
                button.pack(side="left", padx=3)
                self.keyboard_buttons[letter] = button

        tk.Button(
            root, text="New Game",
            font=("Arial", 11, "bold"),
            bg=PURPLE, fg=WHITE,
            activebackground="#55369A",
            activeforeground=WHITE,
            relief="flat", cursor="hand2",
            padx=20, pady=7,
            command=self.new_game
        ).pack(pady=(4, 12))

        # Allow typing letters on the physical keyboard
        self.root.bind("<KeyPress>", self.physical_key)

        self.new_game()

    def new_game(self):
        self.word = random.choice(list(WORDS.keys()))
        self.category, self.clue = WORDS[self.word]
        self.guessed = set()
        self.wrong = 0
        self.over = False

        self.category_label.config(
            text=f"CATEGORY: {self.category.upper()}"
        )
        self.clue_label.config(text=f"Clue: {self.clue}")

        for button in self.keyboard_buttons.values():
            button.config(
                state="normal",
                bg=WHITE,
                fg=DARK
            )

        self.update_game()

    def draw_hangman(self):
        c = self.canvas
        c.delete("all")

        # Gallows in the same simple line-art style as the reference
        line_color = "#25212B"
        width = 5

        # Base, upright pole, top beam and rope
        c.create_line(30, 220, 145, 220,
                      fill=line_color, width=width)
        c.create_line(65, 220, 65, 20,
                      fill=line_color, width=width)
        c.create_line(65, 20, 180, 20,
                      fill=line_color, width=width)
        c.create_line(180, 20, 180, 43,
                      fill=line_color, width=3)

        # Head
        if self.wrong >= 1:
            c.create_oval(
                157, 42, 203, 88,
                outline=line_color, fill=WHITE, width=3
            )

            # Facial expressions drawn directly on the head
            if self.over and self.wrong >= 6:
                # Crying face
                c.create_oval(167, 57, 172, 62,
                              fill=line_color, outline=line_color)
                c.create_oval(188, 57, 193, 62,
                              fill=line_color, outline=line_color)
                c.create_arc(
                    171, 67, 189, 83,
                    start=200, extent=140,
                    style="arc", outline=line_color, width=2
                )
                c.create_line(168, 63, 165, 73,
                              fill="#499DE0", width=2)
                c.create_line(192, 63, 195, 73,
                              fill="#499DE0", width=2)

            elif self.wrong >= 4:
                # Sad face
                c.create_oval(167, 56, 173, 62,
                              fill=line_color, outline=line_color)
                c.create_oval(188, 56, 194, 62,
                              fill=line_color, outline=line_color)
                c.create_arc(
                    171, 69, 190, 84,
                    start=20, extent=140,
                    style="arc", outline=line_color, width=2
                )

            else:
                # Happy face
                c.create_oval(167, 55, 173, 61,
                              fill=line_color, outline=line_color)
                c.create_oval(188, 55, 194, 61,
                              fill=line_color, outline=line_color)
                c.create_arc(
                    170, 61, 191, 78,
                    start=200, extent=140,
                    style="arc", outline=line_color, width=2
                )

        # Body
        if self.wrong >= 2:
            c.create_line(180, 88, 180, 145,
                          fill=line_color, width=4)

        # Left and right arms
        if self.wrong >= 3:
            c.create_line(180, 103, 158, 126,
                          fill=line_color, width=4)

        if self.wrong >= 4:
            c.create_line(180, 103, 202, 126,
                          fill=line_color, width=4)

        # Left and right legs
        if self.wrong >= 5:
            c.create_line(180, 145, 162, 190,
                          fill=line_color, width=4)
            c.create_line(162, 190, 153, 218,
                          fill=line_color, width=4)

        if self.wrong >= 6:
            c.create_line(180, 145, 198, 190,
                          fill=line_color, width=4)
            c.create_line(198, 190, 207, 218,
                          fill=line_color, width=4)

    def guess(self, letter):
        if self.over or letter in self.guessed:
            return

        self.guessed.add(letter)
        button = self.keyboard_buttons[letter]
        button.config(state="disabled")

        if letter in self.word:
            button.config(bg="#D9F4E4", fg=GREEN)
        else:
            self.wrong += 1
            button.config(bg="#FFE0E7", fg=RED)

        if all(ch in self.guessed for ch in self.word):
            self.over = True
            self.status_label.config(
                text="You won! Great job!",
                fg=GREEN
            )

        elif self.wrong >= 6:
            self.over = True
            self.status_label.config(
                text=f"Game over! The word was {self.word}.",
                fg=RED
            )

        self.update_game()

    def update_game(self):
        shown = " ".join(
            letter if letter in self.guessed else "_"
            for letter in self.word
        )
        self.word_label.config(text=shown)

        if not self.over:
            remaining = 6 - self.wrong
            self.status_label.config(
                text=f"Wrong guesses: {self.wrong}/6  |  Chances left: {remaining}",
                fg="#777087"
            )

        self.draw_hangman()

    def physical_key(self, event):
        letter = event.char.upper()
        if letter in self.keyboard_buttons:
            self.guess(letter)


if __name__ == "__main__":
    root = tk.Tk()
    game = Hangman(root)
    root.mainloop()
