import tkinter as tk

root = tk.Tk()

libraryGames=["The Witcher 3: Wild Hunt GOTE", "Jurassic World: Evolution", "Red Dead Redemption 2","Mass Effect Trilogy","Subnautica",]

class GUI:
    def __init__(self, parent):
        frame1 = tk.Frame(parent)
        frame1.pack()
        self.holder_list = []

        for num,game in enumerate(libraryGames):
            rb = tk.Radiobutton(frame1, bg="#000000",fg="#ffffff",
                                value=game, text=game,command= "",selectcolor="grey")
            rb.grid(row = num, column=0, columnspan = 2,padx=25,sticky=tk.W,)
            self.holder_list.append(rb)

        frame2 = tk.Frame(parent)
        frame2.pack()
        tk.Button(frame2,text="Purchased",command=self.purchase).pack()

    def purchase(self):
        print (self.holder_list)
        for widget in self.holder_list:
            widget.grid_forget()

GUI(root)
root.mainloop()