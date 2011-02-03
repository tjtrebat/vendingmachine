__author__ = 'Tom'

from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox

class VendingMachine:
    def __init__(self, root):
        root.title("Vending Machine")
        self.frame = Frame(root, padx=15, pady=15)
        self.frame.grid()
        self.add_snacks()
        self.add_panel()

    def add_snacks(self):
        frame = Frame(self.frame, bd=1, relief=SUNKEN)
        frame.pack(side=LEFT)
        snacks = ('cookie', 'gum', 'pretzel', 'soda')
        prices = {'cookie': .70, 'gum': .90, 'pretzel': .60, 'soda': .80}
        self.values = {}
        self.letters = map(chr, range(65, 68))  # list of caps (A to C)
        for i in range(3):
            for j, snack in enumerate(snacks):
                # add snack image
                lbl_snack = self.get_image_label("%s.jpg" % snack, frame)
                lbl_snack.grid(row=2 * i, column=j, padx=5, pady=10)
                # add snack number
                id_snack = "%s%s" % (self.letters[i], j + 1)
                self.values[id_snack] = prices[snack]
                Label(frame, text=id_snack).grid(row=2 * i + 1, column=j)

    def add_panel(self):
        # add Frame on right side
        top_frame = Frame(self.frame)
        top_frame.pack(side=RIGHT, padx=15, anchor="n")
        # add selection screen
        self.tv_selection = StringVar()
        Label(top_frame, textvariable=self.tv_selection, bd=1, relief=SOLID, width=20, height=4).grid(sticky="w")
        # add selection buttons
        self.add_button_panel(top_frame) 
        # add payment panel and widgets
        frame = self.add_money_panel(top_frame, "Payment", 'payment_amt')
        self.payment = [Spinbox(frame, width=2, from_=0, to=99, command=self.change_amount) for i in range(4)]
        self.add_coins(frame, self.payment)
        # add change panel and widgets
        frame = self.add_money_panel(top_frame, "Change", 'change_amt')
        self.tv_change = [StringVar() for i in range(4)]
        self.change = [Entry(frame, width=2, textvariable=self.tv_change[i], state=DISABLED) for i in range(4)]
        self.add_coins(frame, self.change)

    def add_button_panel(self, frame):
        lbl_frame = LabelFrame(frame, text="Please make selection", padx=35, pady=5)
        lbl_frame.grid(sticky="w")
        frame = Frame(lbl_frame)
        frame.grid(column=1)
        for i, letter in enumerate(self.letters):  # add letter buttons
            Button(frame, text=letter, command=lambda x= letter:self.num_click_handler(x)).grid(row=0, column=i)
        frame = Frame(lbl_frame)
        frame.grid(column=1)
        for i in range(4):  # add number buttons
            Button(frame, text=1 + i, command=lambda x= str(1 + i):self.num_click_handler(x)).grid(row=1 + (i // 2), column=(i % 2))

    def num_click_handler(self, num):
        selection = self.tv_selection.get()
        if len(selection) > 1:
            selection = ""
        selection += num
        if self.tv_payment_amt.get().strip():
            amount = round(float(self.tv_payment_amt.get()), 2)
            if ((len(selection) == 2 and amount > 0) and
                ((selection[0] in self.letters) and (int(selection[1]) in range(1, 5))) and
                (amount >= self.values[selection])):
                for spin_box in self.payment:
                    for i in range(int(spin_box.get())):
                        spin_box.invoke('buttondown')
                self.tv_payment_amt.set("")
                change = round(amount - self.values[selection], 2)
                self.tv_change_amt.set("%0.2f" % change)
                for i in reversed(range(4)):
                    num_coins = int(change // self.coins[i])
                    self.tv_change[i].set(str(num_coins))
                    change = round(change - (num_coins * self.coins[i]), 2)
        self.tv_selection.set(selection)

    def add_money_panel(self, frame, label, entry):
        lbl_frame = LabelFrame(frame, text=label)
        lbl_frame.grid()
        tv = "tv_%s" % entry
        setattr(self, tv, StringVar())
        setattr(self, entry, self.get_payment(lbl_frame, getattr(self, tv)))
        return lbl_frame

    def get_payment(self, frame, tv):
        Label(frame, text="Amount:").grid(row=0, column=0)
        entry = Entry(frame, width=10, textvariable=tv, state=DISABLED)
        entry.grid(row=0, column=1)
        return entry

    def add_coins(self, frame, widgets):
        coins = ('penny.jpg', 'nickel.jpg', 'dime.jpg', 'quarter.jpg')
        for i in range(4):
            self.get_image_label(coins[i], frame).grid(row=0, column=2 + i, padx=3)
            widgets[i].grid(row=1, column=(2 + i))

    def change_amount(self):
        amount = 0
        self.coins = (.01, .05, .10, .25)
        for i, spin_box in enumerate(self.payment):
            amount += int(spin_box.get()) * self.coins[i]
        self.tv_payment_amt.set("%0.2f" % round(amount, 2))
        self.tv_selection.set("")

    def get_image_label(self, img, frame):
        image = Image.open(img)
        photo = ImageTk.PhotoImage(image)
        label = Label(frame, image=photo)
        label.image = photo
        return label

root = Tk()
atm = VendingMachine(root)
root.mainloop()