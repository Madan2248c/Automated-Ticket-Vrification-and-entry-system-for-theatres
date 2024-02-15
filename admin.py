import tkinter as tk
from tkinter import ttk

from databasemanager import DatabaseManager

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Page")
        self.manager = DatabaseManager(
            host='localhost',
            username='root',
            password='Madan@333',
            database='automated_entry_system'
        )
        self.create_widgets()
        
    def create_widgets(self):
        # Create a notebook to contain multiple tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)
        
        # Define styles
        style = ttk.Style()
        style.theme_use('clam')        
        style.configure('Treeview', background='#D3D3D3', foreground='black', rowheight=25, fieldbackground='#D3D3D3')
        style.map('Treeview', background=[('selected', '#347083')])

        # First Tab
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab1, text='Users')
        notebook.add(tab2, text='Booked Tickets')

        # Table for Users
        user_table = ttk.Treeview(tab1, columns=('ID', 'Name', 'Phone', 'Email', 'Username', 'Password', 'Role', 'Salary'), show='headings')
        user_table.heading('ID', text='ID')
        user_table.heading('Name', text='Name')
        user_table.heading('Phone', text='Phone')
        user_table.heading('Email', text='Email')
        user_table.heading('Username', text='Username')
        user_table.heading('Password', text='Password')
        user_table.heading('Role', text='Role')
        user_table.heading('Salary', text='Salary')

        data = self.manager.all_employees()
        for entry in data:
            user_table.insert('', 'end', values=entry)
        
        user_table.pack(fill='both', expand=True)

        # Table for Booked Tickets
        booked_table = ttk.Treeview(tab2, columns=('ID', 'Seat Numbers', 'Number of persons'), show='headings')
        booked_table.heading('ID', text='ID')
        booked_table.heading('Seat Numbers', text='Seat Numbers')
        booked_table.heading('Number of persons', text='Number of persons')

        tickets = self.manager.all_tickets()
        for entry in tickets:
            booked_table.insert('', 'end', values=entry )

        booked_table.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
