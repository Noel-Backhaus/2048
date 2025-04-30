# Ersteller: Noel Backhaus
# Datum: 29.11.2024

from random import randint
from pynput.keyboard import Key
from pynput import keyboard
from tkinter import *
from tkinter import ttk
import threading

# Variablen

values = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
value_vars = []
labels = []
direction = " "
score = 0
esc = False

# Unterprogramme

 # Grundfunktionen

def calculate_score():
    global score

    score = 0
    for x in range(4):
        for y in range(4):
            score += values[x][y]

def change(x, y, num):
    if(y == 0):
        values[0][x] = num
    if(y == 1):
        values[1][x] = num
    if(y == 2):
        values[2][x] = num
    if(y == 3):
        values[3][x] = num

def startnumbers():
    i = 0
    while(i < 3):
        x = randint(0, 3)
        y = randint(0, 3)
        change(x, y, 2)
        converttoStringVar()
        i += 1

def generate_numbers():
    while True:
        x = randint(0, 3)
        y = randint(0, 3)
        if coords(x, y) == 0:
            change(x, y, 2)
            break
        elif full() == True:
            break

def coords(x_spec, y_spec):
    y_count = 0
    for u in values:
        x_count = 0
        for i in u:
            if x_count == x_spec and y_count == y_spec:
                return i
            x_count += 1
        y_count += 1
    return None

 # GUI Funktionen

def initiate_gui():
    global mainWin
    global mainFrame
    global subFrame
    global labels
    global text_label
    global value_vars
    global score_var

    mainWin = Tk()
    mainWin.title('2048')

    subFrame = ttk.Frame(mainWin, borderwidth=2, padding ='20 10 20 10')
    subFrame.grid(row=0)
    mainFrame = ttk.Frame(mainWin, borderwidth=2, padding='20 0 20 20')
    mainFrame.grid(row=1)

    score_var = StringVar()
    score_var.set("Punkte: " + str(score))
    text_label = ttk.Label(subFrame, textvariable=score_var, font=("Arial", 13), width=22, anchor='e')
    text_label.grid()

    converttoStringVar()
    labels = []
    i = 0
    for y in range(4):
        for x in range(4):
            label = ttk.Label(mainFrame, textvariable=value_vars[i], width=8, relief='sunken', padding='0 15', anchor='center', background='white')
            label.grid(column=x, row=y)
            labels.append(label)
            i += 1

def update_gui():
    global labels
    global text_label
    global value_vars
    global score_var

    text_label.config(textvariable=score_var)

    i = 0
    for y in range(4):
        for x in range(4):
            labels[i].config(textvariable=value_vars[i])
            i += 1

def converttoStringVar():
    global score
    global score_var
    global value_vars

    score_var = StringVar()
    score_var.set("Punkte: " + str(score))

    value_vars = []
    for x in range(4):
        for y in range(4):
            value_var = StringVar()
            if values[x][y] == 0:
                value_var.set(" ")
            else:
                value_var.set(str(values[x][y]))
            value_vars.append(value_var)

 # Keyboard Funktionen

def on_press(key):
    global direction
    global esc
    try:
        if key == Key.left:
            direction = "left"
        elif key == Key.right:
            direction = "right"
        elif key == Key.up:
            direction = "up"
        elif key == Key.down:
            direction = "down"
        elif key == keyboard.Key.esc:
            esc = True
        else:
            direction = ""
        # Stop listener
        return False
    except AttributeError:
        pass

def on_release(key):
    global direction
    
    try:
        if key == key.left:
            direction == ""
        if key == key.right:
            direction == ""
        if key == key.up:
            direction = ""
        if key == key.down:
            direction = ""
    except AttributeError:
        pass

def monitor_keyboard():
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

 # Bewegungsfunktionen

def heinzmann_backhaus_algorithmus(array):
    laenge = len(array)

    # Nullen auf die rechte Seite bringen
    zaehler1 = 0
    while zaehler1 < laenge-1:
        zaehler2 = zaehler1
        while zaehler2 < laenge and zaehler2 >= zaehler1:
            if array[zaehler2] == 0:
                zaehler2 += 1
            else:
                zaehler2 -= 1
                if zaehler2 >= 0 and array[zaehler2] == 0: 
                    del array[zaehler2]
                    array.append(0)
        zaehler1 += 1

    # Zahlen addieren
    for zaehler1 in range(laenge-1):
        if array[zaehler1] == array[zaehler1+1]:
            array[zaehler1] *= 2
            del array[zaehler1+1]
            array.append(0)
    
    # Liste ausgeben
    return array

def move_Down():
    global values
    values_temp = []

    # down -> Spalte nach oben
    for x in range(4):
        values_temp = [values[3][x], values[2][x], values[1][x], values[0][x]]
        values_temp = heinzmann_backhaus_algorithmus(values_temp)
        values[3][x] = values_temp[0]
        values[2][x] = values_temp[1]
        values[1][x] = values_temp[2]
        values[0][x] = values_temp[3]

def move_Up():
    global values
    values_temp = []

    # up -> Spalte nach unten
    for x in range(4):
        values_temp = [values[0][x], values[1][x], values[2][x], values[3][x]]
        values_temp = heinzmann_backhaus_algorithmus(values_temp)
        values[0][x] = values_temp[0]
        values[1][x] = values_temp[1]
        values[2][x] = values_temp[2]
        values[3][x] = values_temp[3]

def move_Right():
    global values
    values_temp = []

    # right -> Reihe nach rechts
    for x in range(4):
        values_temp = list(reversed(values[x]))
        values_temp = heinzmann_backhaus_algorithmus(values_temp)
        values[x] = list(reversed(values_temp))

def move_Left():
    global values
    values_temp = []
     
    # left -> Reihe nach links
    for x in range(4):
        values_temp = values[x]
        values_temp = heinzmann_backhaus_algorithmus(values_temp)
        values[x] = values_temp

def movement():
    if direction == "down":
        move_Down()
    if direction == "up":
        move_Up()
    if direction == "right":
        move_Right()
    if direction == "left":
        move_Left()

 # Endfunktionen
 
def full():
    for u in values:
        for i in u:
            if i == 0:
                return False
    return True

def check_end():
    global values

    values_save = values.copy()
    if full() == True:
        direction = "left"
        move_Left()
        direction = "right"
        move_Right()
        direction = "up"
        move_Up()
        direction = "down"
        move_Down()
        if values == values_save:
            return True        
    values = values_save
    return False

# Hauptprogramm

def background():
    while esc == False and check_end() == False:
        converttoStringVar()
        update_gui()
        generate_numbers()
        monitor_keyboard()
        movement()
        calculate_score()
    converttoStringVar()
    update_gui()

def main():
    initiate_gui()    
    t1 = threading.Thread(target=background)
    t1.start()
    startnumbers()
    mainWin.mainloop()

if __name__ == "__main__":
    main()