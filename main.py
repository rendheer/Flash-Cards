from tkinter import *
from tkinter import messagebox
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# words_learned_list = []
# words_to_learn_list = []

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    # Here if this file does not exist then we need to use another file
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    # This above is the other file we need to use when the exception occurs
    to_learn = original_data.to_dict(orient="records")
    # Then we are going to set to_learn dict to the original data
    # For this we made to_learn dict a global dict
else:
    to_learn = data.to_dict(orient="records")

# words_to_learn_list = to_learn
def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer) # We do this so everytime we initiate next card, the timer starts over.
    current_card = random.choice(to_learn)
    print(current_card)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# def learned_list():
#     words_learned_list.append(current_card)
#     print(words_learned_list)
#     next_card()
#     df = pandas.DataFrame(words_learned_list)
#     df.to_csv("data/words_learned.csv", index=False)
#     words_to_learn_list.remove(current_card)
#
# def need_to_learn():
#    print(words_to_learn_list)
#    data = pandas.DataFrame(words_to_learn_list)
#    data.to_csv("data/words_to_learn.csv", index=False)
#    next_card()

def is_known():
    to_learn.remove(current_card)
    # When the green check button is clicked that dict of word is removed in the above line
    # The remaining words are added to the file below using pandas
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    # Index is set to false, so it does not add the index created by pandas dataframe to each record on the file
    print(len(data))
    print(len(to_learn))
    next_card()



window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)


check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)


next_card()

window.mainloop()