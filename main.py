from tkinter import *
import pandas
import random

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/yoruba_data.csv")
finally:
    dictionary = data.to_dict(orient="records")
    card = {}


def the_front_card():
    # assigning value(dictionary) to the card in outer space from this function,to access card in the back card function
    global card, time_check
    # after_cancel class is used to allow user access the French without the timer
    window.after_cancel(time_check)
    card = random.choice(dictionary)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(canvas_lang, text="Yoruba", fill="black")
    canvas.itemconfig(canvas_word, text=card["Yoruba"], fill="black")
    canvas.itemconfig(canvas_select, fill="red")
    time_check = window.after(3000, the_back_card)


def the_back_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(canvas_lang, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=card["English"], fill="white")
    canvas.itemconfig(canvas_select, fill="green")


# to remove known words from the dictionary
def known_word():
    dictionary.remove(card)
    new_data = pandas.DataFrame(dictionary)
    # setting the index of the csv to false
    new_data.to_csv("data/words_to_learn.csv", index=False)
    print(len(new_data))
    the_front_card()


BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("fLASH CARD")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)
# checking the card after 3secs(3000 milliseconds)
time_check = window.after(3000, the_back_card)


right_image = PhotoImage(file="images/right.png")
left_image = PhotoImage(file="images/wrong.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
canvas = Canvas(width=801, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas_select = canvas.create_text(400, 30, text="(click ❌ to skip word and ✅ to remove word)",
                                   font=("Arial", 15, "italic"))
canvas_lang = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
canvas_word = canvas.create_text(400, 300, text="", font=("Arial", 60, "italic"))
canvas.grid(row=0, column=0, columnspan=2)

known_button = Button(image=right_image, highlightthickness=0, command=known_word)
known_button.grid(row=1, column=1)
unknown_button = Button(image=left_image, highlightthickness=0, command=the_front_card)
unknown_button.grid(row=1, column=0)

the_front_card()
window.mainloop()
