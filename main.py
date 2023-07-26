from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
FONT_NAME = "Ariel"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ------------------------------ NEXT FLASHCARD --------------------------------- #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

# --------------------------------- FLIP CARD ------------------------------------ #

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# --------------------- KNOWN CARD REMOVAL INTO NEW DECK ------------------------ #

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #

# Images #
window = Tk()
window.title("Flashcards for French to English")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Card Flipper
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=WHITE)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=(FONT_NAME, 40, "italic", "bold"))
card_word = canvas.create_text(400, 263, text="word", font=(FONT_NAME, 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons #
# "X" Button
# The "x" button will keep the flashcard in rotation because it is not known yet.
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Check Button
# When the user presses on the ✅ button, it means that they know the current word on the flashcard and that
# word should be removed from the list of words that might come up.
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)


next_card()







window.mainloop()