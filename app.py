import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ck

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import datetime
import db

import pandas as pd
import sqlite3

ck.set_appearance_mode("dark")
ck.set_default_color_theme("dark-blue")

class App(ck.CTk):
    WIDTH = 1200
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Expenses Tracker")
        self.resizable(0,0)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.input_balance = db.select_balance()
        print("Input Balance from database:", self.input_balance)

        self.balance = 0.0

        self.total_expenses = db.sum_all()
        print("Total Expenses from database:", self.total_expenses)
        

        # Sidebar
        self.sidebar_frame = ck.CTkFrame(self, fg_color="#725373",  width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        # Logo
        logo_img_data = Image.open("image/logo.png")
        self.logo_img = ck.CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
        self.logo_label = ck.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img).pack(pady=(38, 0), anchor="center")

        #Main View
        self.main_view = ck.CTkFrame(self, fg_color="#1a1e24",  width=1400, height=1000, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        # Define function to clear the main_view frame
        def clear_main_view():
            for widget in self.main_view.winfo_children():
                widget.destroy()

        def switch_to_Dashboard():
            clear_main_view()
            # Insert button
            self.InsertButton = ck.CTkButton(
                self.main_view,
                text=None,
                fg_color="#654a64",
                corner_radius=50,
                width=50,
                height=50,
                hover=False,
                command= self.toggleEntryForm,
            )

            self.InsertButton.place(x=460, y=530)

            self.PlusLabel = ck.CTkLabel(
                self.InsertButton,
                bg_color="#654a64",
                text="+",
            )

            self.PlusLabel.place(
                relx=0.5, rely=0.5, anchor="center"
            )

            #cardBalance
            self.CardBalance = ck.CTkFrame(
                self.main_view, 
                fg_color="#654a64", 
                corner_radius=10,
                width=400, 
                height=120
            )
            self.CardBalance.place(x=30, y=30)


            self.BalanceButton = ck.CTkButton(
                self.main_view,
                text="Add Balance",
                fg_color="#654a64",
                width=100,
                height=30,
                hover=False,
                font=("Cascadia Code", 12),
                command= self.buttonBalance,
            )

            self.BalanceButton.place(x=320, y=40)


            #cardExpenses
            self.CardExpenses = ck.CTkFrame(
                self.main_view, 
                fg_color="#654a64", 
                corner_radius=10,
                width=400, 
                height=120
            )
            self.CardExpenses.place(x=500, y=30)

            #lable
            self.TitleBalance = ck.CTkLabel(
                self.main_view, text= "BALANCE", 
                fg_color="#654a64", 
                font=("Franklin Gothic Medium", 22),
                width = 20 ,
                height =10
            )
            self.TitleBalance.place(x=60, y=40)

            self.TitleExpenses = ck.CTkLabel(
                self.main_view, text= "EXPENSES", 
                fg_color="#654a64", 
                font=("Franklin Gothic Medium", 22),
                width = 20 ,
                height =10
            )
            self.TitleExpenses.place(x=520, y=40)

            self.BALANCE = ck.CTkLabel(
                self.main_view, 
                text= f"$ {self.balance}", 
                fg_color="#654a64", 
                width=20, 
                height=10, 
                font=("Cascadia Code", 55)
            )
            self.BALANCE.place(x=65, y=70)

            
            self.Expenses = ck.CTkLabel(
                self.main_view, 
                text=f"-$ {self.total_expenses}", 
                fg_color="#654a64", 
                width=20, 
                height=10, 
                font=("Cascadia Code", 55)
            )
            self.Expenses.place(x=530, y=70)

            self.ExpensesHistory = ck.CTkLabel(
                self.main_view, 
                text="Expenses History", 
                fg_color="#1a1e24", 
                width=20, 
                height=10, 
                font=("Cascadia Code", 18)
            )
            self.ExpensesHistory.place(x=30, y=170)

            ## EntryForm 

            self.entryForm = ck.CTkFrame(self.main_view, fg_color="#482f47", width=400, height=360, corner_radius=40)
            self.entryForm.grid_columnconfigure((0,3), minsize=200)

            # Description
            self.DescriptionLabel = ck.CTkLabel(self.entryForm, 
                                                text="Description", 
                                                fg_color="#482f47", 
                                                font=("Arial Bold", 18), 
                                                justify="left")
            
            self.DescriptionLabel.place(x=30, y=30)

            self.DescriptionEntry = ck.CTkEntry(self.entryForm, fg_color="#482f47", font=("Arial Bold", 18), border_width= 0, width= 300)
            self.DescriptionEntry.place(x=30, y=60)

            self.UnderLineEntry = ck.CTkFrame(self.entryForm, fg_color="white", height=3, width=300)
            self.UnderLineEntry.place(x=30, y=90)

            # Cost
            self.CostLabel = ck.CTkLabel(self.entryForm, 
                                                text="Cost", 
                                                fg_color="#482f47", 
                                                font=("Arial Bold", 18), 
                                                justify="left")
            
            self.CostLabel.place(x=30, y=120)

            self.CostEntry = ck.CTkEntry(self.entryForm, fg_color="#482f47", font=("Arial Bold", 18), border_width= 0, width= 300)
            self.CostEntry.place(x=30, y=150)

            self.UnderLineCostEntry = ck.CTkFrame(self.entryForm, fg_color="white", height=3, width=300)
            self.UnderLineCostEntry.place(x=30, y=180)

            # menu category

            self.Category = ck.CTkOptionMenu(self.entryForm,
                                             state="readonly",
                                             fg_color="#2b1c2a",
                                             button_color="#ada2ad",
                                             values=["Food", 
                                                     "Transport", 
                                                     "Entertainment", 
                                                     "Health", 
                                                     "Education", 
                                                     "Others"],
                                             font=("Arial Bold", 18),
                                             width= 250
                                             )
            self.Category.set("Select Category")
            self.Category.place(x=30, y=210)

            # Button submit and cancel
            self.SubmitButton = ck.CTkButton(self.entryForm,
                                             text="Submit",
                                             fg_color="#2b1c2a",
                                             corner_radius=10,
                                             width=0,
                                             font=("Arial Bold", 18),
                                             hover_color="#1c2026",
                                             command=self.submitExpense
                                            )
            self.SubmitButton.place(x=100, y=300)

            self.CancelButton = ck.CTkButton(self.entryForm,
                                             text="Cancel",
                                             fg_color="#2b1c2a",
                                             corner_radius=10,
                                             width=0,
                                             font=("Arial Bold", 18),
                                             command= self.clearEntry,
                                             hover_color="#1c2026",
                                        
                                            )
            self.CancelButton.place(x=180, y=300)

            # Table

            table_data = self.getData()
            header = ["ID","Expense_Name", "Category", "Cost", "Time"]

            self.table_frame = tk.Frame(self.main_view)
            self.table_frame.place(x=100, y=270)

            #add style
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", 
                            background="#1a1e24", 
                            foreground="white", 
                            rowheight=25,
                            fieldbackground="#1a1e24",
                            font=("Arial Bold", 14)

                            )
            
            style.map("Treeview", background=[('selected', '#482f47')])

            self.table = ttk.Treeview(self.table_frame, columns=header, show='headings',style="Treeview" , height=14)

            for column in header:
                self.table.heading(column, text=column)

            for row in table_data:
                self.table.insert('', 'end', values=row)

            self.table.pack(expand=True)
            self.table.bind("<Double-Button-1>", self.deleteRow)


            self.button_save = ck.CTkButton(master= self.main_view, 
                                            text="Save Expenses in excel", 
                                            command=self.save_expenses
                                            )
            self.button_save.place(x=100, y=525)

            self.update_balance()

        def switch_to_Analytics():
            clear_main_view()

            # Create a connection to the database
            conn = sqlite3.connect('expense.db')

            # Write a SQL query to get the 'Category' and 'amount' columns
            query = "SELECT Category, Cost FROM expenses"
            # Use pandas to run the query and store the result in a DataFrame
            df_category = pd.read_sql_query(query, conn)
            # Group by category and sum amounts
            grouped = df_category.groupby('Category').sum()

            # Sort categories by total cost in ascending order
            grouped = grouped.sort_values('Cost', ascending=True)

            # Create bar plot

            fig_1 = Figure(figsize=(6, 6), facecolor="#725373")
            ax_1 = fig_1.add_subplot()
            ax_1.bar(grouped.index, grouped['Cost'], width= 0.7)
            ax_1.set_xlabel('Category')
            ax_1.set_ylabel('Total Cost')
            ax_1.set_title('Expenses by Category')

            canvas = FigureCanvasTkAgg(figure=fig_1, master=self.main_view)
            canvas.draw()
            canvas.get_tk_widget().place(x=20, y=20)


            # Create pie chart
            fig_2 = Figure(figsize=(6, 6), facecolor="#725373")
            ax2 = fig_2.add_subplot()
            ax2.pie(grouped['Cost'], labels = grouped.index, autopct='%1.1f%%')
            ax2.set_title('Expenses by Category')

            canvas = FigureCanvasTkAgg(figure=fig_2, master=self.main_view)
            canvas.draw()
            canvas.get_tk_widget().place(x=600, y=20)


            self.button_open_plot = ck.CTkButton(master= self.main_view, text="Show Expenses Plot", command=self.show_expenses_plot)
            self.button_open_plot.place(x=100, y=525)
            

        def switch_to_Save():
            clear_main_view()
            ck.CTkLabel(master=self.main_view, text="save Content").pack()
        

        # Buttons
        expen_img_data = Image.open("image/home.png")
        self.expen_img = ck.CTkImage(light_image=expen_img_data, dark_image=expen_img_data, size=(43, 43))
        self.btnExpen = ck.CTkButton(master=self.sidebar_frame, 
                                    image=self.expen_img, 
                                    text="Dashboard", 
                                    fg_color="#725373", 
                                    font=("Arial Bold", 14),
                                    text_color="#efe5ef", 
                                    hover_color="#1c2026", 
                                    anchor="w", 
                                    command=switch_to_Dashboard).pack(anchor="center", ipady=5, pady=(60, 0))
        
        analytic_img_data = Image.open("image/analytics.png")
        self.analytic_img = ck.CTkImage(light_image=analytic_img_data, dark_image=analytic_img_data, size=(43, 43))
        self.btnAnalytic = ck.CTkButton(master=self.sidebar_frame, 
                                        image=self.analytic_img, 
                                        text="Analytics", 
                                        fg_color="#725373", 
                                        font=("Arial Bold", 14), 
                                        text_color="#efe5ef", 
                                        hover_color="#1c2026", 
                                        anchor="w", 
                                        command=switch_to_Analytics).pack(anchor="center", ipady=5, pady=(16, 0))

        save_img_data = Image.open("image/download.png")
        self.save_img = ck.CTkImage(light_image=save_img_data, dark_image=save_img_data, size=(43, 43))
        self.Save = ck.CTkButton(master=self.sidebar_frame, 
                                image=self.save_img, 
                                text="Read File", 
                                fg_color="#725373", 
                                font=("Arial Bold", 14), 
                                text_color="#efe5ef", 
                                hover_color="#1c2026", 
                                anchor="w", 
                                command=switch_to_Save).pack(anchor="center", ipady=5, pady=(16, 0))
        
        switch_to_Dashboard()

    # entry animation when the button is clicked
    def entryAnimation(self):
        self.entryForm.update()
        self.entryForm.place(relx = 0.5, y=360, anchor="center")
        self.entryForm.lift()

    def toggleEntryForm(self):
        if self.entryForm.winfo_viewable(): 
            self.entryForm.place_forget() 
        else: 
            self.entryAnimation() 

    def buttonBalance(self):
        dialog = ck.CTkInputDialog(text="Type in your balance:", title="Add Balance")
        self.input_balance = dialog.get_input() 
        print("Balance:", self.input_balance)

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.insert_balance(self.input_balance,time)

        # Update expenses
        self.updateExpenses()
        # Update balance
        self.update_balance()

    def clearEntry(self):
        self.Category.set('Select Category')  # Assuming self.Category is a StringVar
        self.DescriptionEntry.delete(0, 'end')
        self.CostEntry.delete(0, 'end')

    def submitExpense(self):
        # Retrieve information
        expense_name = self.DescriptionEntry.get()
        category = self.Category.get()
        cost = self.CostEntry.get()

        if not expense_name or not cost or category == "Select Category":
            tk.messagebox.showinfo("Error", "Please fill in all fields!")
            return

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert into database
        db.insert_groceries(expense_name, category, cost, time)
        tk.messagebox.showinfo("Success", "Expense submitted successfully!")

        # Update total_expenses
        self.total_expenses = db.sum_all()
        # Update the Expenses label
        self.updateExpenses()
        # Update balance
        self.update_balance()
        # Refresh the table
        self.refresh_table()

    def getData(self):
        data = db.select_all()
        return data
    
    def deleteRow(self, event):
        # Get the clicked row
        clicked_row = self.table.identify_row(event.y)
        # Get the data for the clicked row
        clicked_row_data = self.table.item(clicked_row, 'values')
        id = clicked_row_data[0]

        if tk.messagebox.askyesno("Confirmation", f"Do you want to delete the expense with ID {id}?"):
            # Delete from database
            db.delete_one(id)

            # Update total_expenses
            self.total_expenses = db.sum_all()
             # Update balance
            self.update_balance()
            # Update the Expenses label
            self.updateExpenses()
            # Delete from table
            self.table.delete(clicked_row)
            # Refresh the table
            self.refresh_table()
            
    def refresh_table(self):
        # Clear the table
        for row in self.table.get_children():
            self.table.delete(row)

        # Get the new data
        table_data = self.getData()

        # Insert the new data into the table
        for row in table_data:
            self.table.insert('', 'end', values=row)

    def updateExpenses(self):
        self.Expenses.configure(text=f"-$ {self.total_expenses}")
        self.Expenses.update_idletasks()

    def update_balance(self):
        if self.input_balance is None:
            print("Input balance is not set.")
            return
        expenses = db.sum_all()
        self.balance = float(self.input_balance) - expenses
        print("Balance:", self.balance)

        self.BALANCE.configure(text=f"$ {self.balance}")
        self.BALANCE.update_idletasks()

    def save_expenses(self):
        # Prompt the user for the name of the Excel file
        dialog = ck.CTkInputDialog(text="Type in the name of the Excel file:", title="Save Excel File")
        filename = dialog.get_input() 

        # If the user clicked close or cancel, don't save the file
        if filename is None:
            return

        # Get data from the database
        data = db.select_all()
        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=['ID', 'Expense_Name', 'Category', 'Cost', 'Time'])
        # Save the DataFrame to an Excel file with the specified name
        df.to_excel(f'{filename}.xlsx', index=False)
        tk.messagebox.showinfo("Success", "Excel file saved successfully!")


    def show_expenses_plot(self):
        # Create a new Tk window
        new_window = tk.Toplevel(self)
        
        # Rest of your code...
        conn = sqlite3.connect('expense.db')
        query = "SELECT Time, Cost FROM expenses LIMIT 30"
        df = pd.read_sql_query(query, conn)
        conn.close()
        df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%m-%d')
        grouped = df.groupby('Time').sum()
        grouped = grouped.sort_values('Time')

        fig_1 = Figure(figsize=(15, 7), facecolor="#725373")
        ax_1 = fig_1.add_subplot()
        ax_1.plot(grouped.index, grouped['Cost'])
        ax_1.set_xlabel('Time')
        ax_1.set_xticklabels(grouped.index, rotation=45, ha='right')
        ax_1.set_xlabel('Cost')
        ax_1.grid(visible=True)

        ax_1.xaxis.set_label_position('top')
        ax_1.set_xlabel('Expenses Over Time', fontsize=15, labelpad=10)

        # Draw the plot on the new Tkinter canvas
        canvas = FigureCanvasTkAgg(figure=fig_1, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack() 

if __name__ == "__main__":
    app = App()
    app.mainloop()

