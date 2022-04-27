import tkinter as tk
from tkinter import *
from matplotlib.pyplot import plot
from tkmacosx import Button
from stock_quiz import *
from kernel import *

THEME_COLOR = "#375362"

class stockUI:

    def __init__(self, stock_quiz: StockQuiz):
        self.quiz = stock_quiz
        self.window = Tk()
        self.window.title("Stock Risk Evaluation")
        self.window.geometry("850x550")
        self.winWidth = 850
        self.winHeight = 550

        self.display_title()

        self.canvas = Canvas(width = 800, height = 250)
        self.question_text = self.canvas.create_text(400, 125,
                                                    text = "Qestion: ",
                                                    width = 680,
                                                    fill = THEME_COLOR,
                                                    font = ('Ariel', 20, 'italic'))
        
        self.canvas.grid(row = 2, column = 0, columnspan = 2, pady = 50)
        self.display_question()

        self.user_answer = StringVar()
    
        self.display_options()

        self.buttons()

        self.window.mainloop()

    def display_title(self):
        title = Label(self.window, text = "Stock Risk Eval",
                        width=60, bg = 'green', fg = 'white', font = ('ariel', 20, 'bold'))
        
        title.place(x=0, y=2)

    def display_question(self):
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)
    
    def radio_buttons(self, choices):
        choice_list = []
        y_pos = 220
        
        while len(choice_list) < choices:
            radio_btn = Radiobutton(self.window,
                                    text = '',
                                    variable=self.user_answer,
                                    value='',
                                    font = ('ariel', 14))
            choice_list.append(radio_btn)
            radio_btn.place(x=200, y=y_pos)
            y_pos += 40
        
        return choice_list

    def clear_radio_buttons(self, buttons):
        for b in buttons:
            b['text'] = ''
            b['value'] = ''    
    
    def display_options(self):
        val = 0
        qn = 1
        self.user_answer.set(None)
        self.opts = self.radio_buttons(len(self.quiz.current_question.choices))

        for option in self.quiz.current_question.choices:
            option = str(qn) + ".  " + option
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1
            qn += 1
        
    def next_btn(self):

        if self.user_answer.get() == "None":
            tk.messagebox.showinfo(message = "You have to choose one option!")
            return

        self.quiz.cumulate_score(int(self.user_answer.get()[0]))
        if self.quiz.check_left():
            self.display_question()
            self.clear_radio_buttons(self.opts)
            self.display_options()
        else:
            self.ask_stock()
            # self.display_results()
            # self.window.destroy()
    
    def buttons(self):
        self.question_buttons = []
        next_button = Button(self.window, text = "Next",
                            command=self.next_btn,
                            width = 200,
                            bg = 'green',
                            fg = 'white',
                            font = ('ariel', 16, 'bold'))
        next_button.place(x=250, y=450)
        self.question_buttons.append(next_button)

        quit_button = Button(self.window, text = "Quit",
                            command=self.window.destroy,
                            width = 200,
                            bg = 'red',
                            fg = 'white',
                            font = ('ariel', 16, 'bold'))
        quit_button.place(x=450, y=450)
        self.question_buttons.append(quit_button)

    def ask_stock(self):
        self.pop = Toplevel(self.window)
        self.pop.title("What stock do you want to invest?")
        self.pop.geometry("450x300")
        self.pop.config(bg = 'white')

        pop_label = Label(self.pop, text="Input the stock you're interested in (max 5)",
                        bg = "green",
                        fg = "white",
                        width = 100,
                        font = ('ariel', 14, 'bold'))
        pop_label.pack(pady = 10)

        pop_frame = Frame(self.pop, bg = "white")
        pop_frame.pack(pady = 10)

        self.entry_list = []
        for i in range(5):
            self.entry_list.append(Entry(pop_frame))
            self.entry_list[i].grid(row = i, column = 1)

        confirm_btn = Button(pop_frame, text = 'Confirm', 
                            command = lambda:self.display_results(),
                            bg = 'green',
                            fg = 'white',
                            width = 100,
                            font = ('ariel', 14, 'bold'))
        confirm_btn.grid(row=5, column=1)

    def clear_question(self):
        self.canvas.grid_forget()
        for o in self.opts:
            o.place_forget()
        for b in self.question_buttons:
            b.place_forget()

    def res_buttons(self, frame, stock_list):
        self.res_btns = []
        btn_list = ['Raw', 'Cumulative', 'Raw-Box', '30days-rolling', 'sharpe']
        button_wid = 100
        pad = 5

        for bi, b in enumerate(btn_list):
            btn = Button(frame, text = b,
                            command=lambda b=b: self.stock_eval.draw_plot(b),
                            width = button_wid,
                            bg = 'green',
                            fg = 'white',
                            font = ('ariel', 12, 'normal'),
                            activebackground = 'green4')
            btn.grid(row = 0, column = bi, padx=pad)
            self.res_btns.append(btn)
        
        for si, s in enumerate(stock_list):
            if len(s) < 4: continue

            st = str(s) + " MC Sim"
            btn = Button(frame, text = st,
                            command=lambda s=s: self.stock_eval.draw_plot(s),
                            width = button_wid,
                            bg = 'green',
                            fg = 'white',
                            font = ('ariel', 12, 'normal'),
                            activebackground = 'green4')
            btn.grid(row = 1, column = si, padx = pad, pady = pad)
            self.res_btns.append(btn)

    def display_results(self):
        """To display the result using messagebox"""
        stock_list =[i.get() for i in self.entry_list]
        self.clear_question()

        if self.quiz.score <= 17:
            risk_rate = "Low"
            risk_color = 'green'
        elif self.quiz.score >= 18 and self.quiz.score <= 30:
            risk_rate = "Medium"
            risk_color = 'orange'
        else:
            risk_rate = "High"
            risk_color = 'red'

        ## fetch stock data
        stocks_df, success_list , error_list = comb_close(stock_list, 2, 1)
        print(success_list)
        print(error_list)

        result_frame = Frame(self.window, width = self.winWidth, height = 80)
        stock_frame = Frame(self.window, width = 50)
        plot_btn_frame = Frame(self.window, width = self.winWidth-50, height = 80)
        plot_frame = Frame(self.window, width = self.winWidth-50, height=self.winHeight-50)
        self.window.update()

        result_frame.grid(row = 0, column = 0, columnspan = 2)
        stock_frame.grid(row = 1, column = 0, rowspan = 2, sticky = tk.W, padx=10, pady = 20)
        plot_btn_frame.grid(row = 1, column = 1, sticky = tk.N)
        plot_frame.grid(row = 2, column = 1, sticky= tk.SE)

        # draw matplotlibs, get stock_eval
        self.res_buttons(plot_btn_frame, stock_list)
        self.stock_eval = stockEval(stocks_df, plot_frame, success_list, error_list)

        score_text = "Your score is: " + str(self.quiz.score)
        score_label = Label(result_frame, text = score_text,
                            fg = "black",
                            font = ('ariel', 30, 'bold'))
        risk_text = "Risk Rate: "
        risk_label = Label(result_frame, text=risk_text,
                            fg = "black",
                            font = ('ariel', 30, 'bold'))
        risk_grade_label = Label(result_frame, text = risk_rate,
                                fg = risk_color,
                                font = ('ariel',40, 'bold'))
        score_label.grid(row = 0, column = 0, padx = 20, pady = 50)
        risk_label.grid(row = 0, column = 1, padx = 20, pady = 50)
        risk_grade_label.grid(row = 0, column = 2, padx = 20, pady = 50)

        for si, s in enumerate(stock_list):
            if s != "" :
                cur_col = 'black'

                if s in self.stock_eval.stock_risk:
                    r = self.stock_eval.stock_risk[s]
                else: r = "Null"

                if r == "Null":
                    cur_col = 'red'
                    risk_col = 'gray'

                cur_text = str(si + 1) + ". " + s
                cur_label = Label(stock_frame, text = cur_text,
                            fg = cur_col,
                            font = ('ariel', 15, 'bold'))
                cur_label.grid(row = si, column = 0, pady = 5)
                if r == 'High':
                    risk_col = 'red'
                elif r == 'Med':
                    risk_col = 'orange'
                elif r == 'Low':
                    risk_col = 'green'
                
                risk_label = Label(stock_frame, text = r,
                                    fg = risk_col,
                                    font = ('ariel', 20, 'bold'))
                risk_label.grid(row = si, column = 1, pady = 5)

        self.display_title()
        self.pop.destroy()