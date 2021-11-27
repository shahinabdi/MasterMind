import tkinter as tk
from tkinter.constants import NW
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import collections


class Mastermind:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tk.Canvas(parent)
        self.draw_board()

    def draw_board(self, event=None):
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.parent, bg='gray', width=600, height=800)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=bg, anchor=NW)

        self.color_bag = {'r': self.canvas.create_oval(55, 700, 105, 750, fill='red', outline='red'),
                          'o': self.canvas.create_oval(115, 700, 165, 750, fill='orange', outline='orange'),
                          'y': self.canvas.create_oval(175, 700, 225, 750, fill='yellow', outline='yellow'),
                          'g': self.canvas.create_oval(235, 700, 285, 750, fill='green', outline='green'),
                          'b': self.canvas.create_oval(295, 700, 345, 750, fill='blue', outline='blue'),
                          'p': self.canvas.create_oval(355, 700, 405, 750, fill='purple', outline='purple')
                          }

        self.ids = {v: k for k, v in self.color_bag.items()}

        self.colors = {'r': 'red', 'o': 'orange', 'y': 'yellow',
                       'g': 'green', 'b': 'blue', 'p': 'purple'}

        self.guesses = ['']  # User Selections

        self.canvas.bind('<1>', self.check)
        self.parent.bind('<Control-n>', self.draw_board)
        self.parent.bind('<Control-N>', self.draw_board)

        self.pattern = [random.choice('roygbp') for _ in range(4)]

        print(self.pattern)
        self.counted = collections.Counter(self.pattern)
        print(self.counted)

    def check(self, event=None):

        # ID Object 1: GUI, 2: Red, ...
        id = self.canvas.find_withtag("current")[0]

        if id == 1:
            pass
        else:
            guess = self.ids[id]  # r, o, y, g, b, p

            self.guesses[-1] += guess

            x_offset = (len(self.guesses[-1]) - 1) * 45
            y_offset = (len(self.guesses) - 1) * 70
            self.canvas.create_oval(x_offset+20, y_offset+20,
                                    x_offset+50, y_offset+50,
                                    fill=self.colors[guess],
                                    outline=self.colors[guess])

            if len(self.guesses[-1]) < 4:
                return

            guess_count = collections.Counter(self.guesses[-1])
            close = sum(min(self.counted[k], guess_count[k])
                        for k in self.counted)
            exact = sum(pattern == guesses for pattern,
                        guesses in zip(self.pattern, self.guesses[-1]))
            close -= exact
            colors = exact*['black'] + close*['white']

            key_coordinates = [(270, y_offset+20, 295, y_offset+45),
                               (300, y_offset+20, 325, y_offset+45),
                               (270, y_offset+50, 295, y_offset+75),
                               (300, y_offset+50, 325, y_offset+75)]  # [(x0,y0,x1,y1), ..., ..., ...]

            for color, coord in zip(colors, key_coordinates):
                self.canvas.create_oval(coord, fill=color, outline=color)

            if exact == 4:
                msgbox = messagebox.showinfo(
                    'Info', 'Effectivement! \nCtrl+N to new game')
                self.canvas.unbind('<1>')
            elif len(self.guesses) > 7:
                msgbox = messagebox.showinfo(
                    'Info', 'Out of guesses. The correct answer is \n{}.'.format(self.pattern))
                self.canvas.unbind('<1>')
            else:
                self.guesses.append('')


root = tk.Tk()
root.resizable(0, 0)
root.title('MasterMind')
bg = ImageTk.PhotoImage(Image.open('bg.png'))
game = Mastermind(root)
root.mainloop()
