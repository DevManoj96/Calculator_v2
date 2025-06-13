import tkinter as tk
from tkinter import  messagebox
import datetime
import ast


class Calculator:

    def __init__(self, root):
        self.root = root

        self.root.title("Test Calculator")
        self.root.geometry('520x520')
        self.root.resizable(True, True)
        
        self.expression = ""
        self.is_dark = False

        self.theme_colors = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "btn": "#e0e0e0"
            },
            "dark": {
                "bg": "#121212",
                "fg": "#e0e0e0",
                "btn": "#2a2a2a"
            }
        }



        self.widgets_to_theme = []

        self.history_popup = None
        self.history_widgets = []

        self.display = tk.Entry(self.root, font=("Arial", 24), borderwidth=2, relief="ridge", justify='right', state='readonly')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=10, sticky='nsew')
        self.widgets_to_theme.append(self.display)

        self.menubar = tk.Menu(self.root)

        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="History", command=self.history_check)
        filemenu.add_command(label="Toggle Theme", command=self.toggle_theme)

        self.menubar.add_cascade(label="Options", menu=filemenu)

        self.root.config(menu=self.menubar)


        
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        self.widgets_to_theme.append(self.buttons_frame)

        buttons = [
            ('7', 1, 1), ('8', 1, 2), ('9', 1, 3), ('/', 1, 4),
            ('4', 2, 1), ('5', 2, 2), ('6', 2, 3), ('x', 2, 4),
            ('1', 3, 1), ('2', 3, 2), ('3', 3, 3), ('-', 3, 4),
            ('0', 4, 1), ('.', 4, 2), ('=', 4, 3), ('+', 4, 4),
            ('Exit', 5, 1), ('C', 5, 2), ('⌫', 5, 3)
        ]

        for (text, row, col) in buttons:
            if text == '=':
                cmd = self.calculate
            
            elif text == 'C':
                cmd = self.clear

            elif text == 'Exit':
                cmd = self.root.quit
            
            elif text == '⌫':
                cmd = self.backspace

            else:
                cmd = lambda t=text: self.press(t)


            btn = tk.Button(self.buttons_frame, text=text, command=cmd, font=("Arial", 12), width=10, height=2, relief="flat", borderwidth=1)
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            
            
            self.widgets_to_theme.append(btn)

        
                
        self.root.bind('<Return>', lambda event: self.calculate())
        self.root.bind('<KP_Enter>', lambda event: self.calculate())  # Numpad Enter
        self.root.bind("<BackSpace>", lambda event: self.backspace())
        self.root.bind("<Delete>", lambda event: self.clear())
        self.root.bind("<Escape>", lambda event: self.clear())
        
        
        for i in range(10):
            self.root.bind(str(i), lambda event, num=i: self.press(num))
            self.root.bind(f'<KP_{i}>', lambda event, num=i: self.press(num))
        
        
        self.root.bind('+', lambda event: self.press('+'))
        self.root.bind('<KP_Add>', lambda event: self.press('+'))
        self.root.bind('-', lambda event: self.press('-'))
        self.root.bind('<KP_Subtract>', lambda event: self.press('-'))
        self.root.bind('*', lambda event: self.press('x'))
        self.root.bind('<KP_Multiply>', lambda event: self.press('x'))
        self.root.bind('/', lambda event: self.press('/'))
        self.root.bind('<KP_Divide>', lambda event: self.press('/'))
        self.root.bind('.', lambda event: self.press('.'))
        self.root.bind('<KP_Decimal>', lambda event: self.press('.'))
        self.apply_theme()


    def press(self, symbol):
        self.expression += str(symbol)
        self.update_display()

            
    def clear(self):
        self.expression = ""
        self.update_display()

    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display()

    def update_display(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, str(self.expression))
        self.display.config(state='readonly')

            
    def calculate(self):
        try:
            result = eval(compile(ast.parse(self.expression.replace("x", "*"), mode="eval"), '', 'eval'))
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                             
            self.save_history(result)
            self.expression = str(result)
            self.update_display()

        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide with Zero!")
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.expression = ""
            self.update_display()


    def save_history(self, result):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("calculator_history.txt", "a") as f:
            history = f"{current_time} | {self.expression} = {result}\n"
            f.write(history)
    
    def history_check(self):

        if self.history_popup and self.history_popup.winfo_exists():
            self.history_popup.lift()
            return

        try:
            with open("calculator_history.txt", "r")as f:
                history = f.readlines()
        except FileNotFoundError:
            messagebox.showinfo("History", "No History Found")
            return

        
        self.history_popup = tk.Toplevel(self.root)
        self.history_popup.title("History")
        self.history_popup.geometry("400x400")

        def clear_history():
            with open("calculator_history.txt", "w") as f:
                f.write("")
                messagebox.showinfo("History", "History Cleared")
                self.history_popup.destroy()


        self.listbox = tk.Listbox(self.history_popup, width=40, height=15)
        self.listbox.pack(padx=5 ,pady=5)

        for line in reversed(history):
            self.listbox.insert(0, line.strip())

        self.done_btn = tk.Button(self.history_popup, text="Done", command=self.history_popup.destroy, font=("Arial", 12) ,width=10, height=2, relief="flat", borderwidth=1)
        self.done_btn.pack(padx=5, pady=5)

        self.clear_btn = tk.Button(self.history_popup, text="Clear", command=clear_history, font=("Arial", 12), width=10, height=2, relief="flat", borderwidth=1)
        self.clear_btn.pack(padx=5, pady=5)

        self.history_widgets = [self.history_popup, self.listbox, self.done_btn, self.clear_btn]
        
        self.apply_theme()
        

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def apply_theme(self):
        theme = "dark" if self.is_dark else "light"
        colors = self.theme_colors[theme]
        self.root.configure(bg=colors["bg"])
        self.buttons_frame.config(bg=colors["bg"])
        

        for widget in self.widgets_to_theme:
            if widget != self.display:
                try:
                    widget.configure(bg=colors["btn"], fg=colors["fg"])
                except:
                    pass
        

        try:
            self.display.configure(
                bg=colors["btn"], 
                fg=colors["fg"], 
                insertbackground=colors["fg"],
                readonlybackground=colors["btn"],
                selectbackground=colors["fg"],
                selectforeground=colors["btn"]
            )
        except:
            pass

        if self.history_popup and self.history_popup.winfo_exists():
            self.history_popup.configure(bg=colors["bg"])
            for widget in self.history_widgets:
                try:
                    widget.configure(bg=colors["bg"], fg=colors["fg"])
                except:
                    pass
if __name__ == '__main__':

    root = tk.Tk()
    app = Calculator(root)

    root.mainloop()