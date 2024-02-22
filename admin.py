import tkinter as tk
from tkinter import ttk
from databasemanager import DatabaseManager
from tet import EmployeeFormApp

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
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Treeview', background='#D3D3D3', foreground='black', rowheight=25, fieldbackground='#D3D3D3', font=('Arial', 10))
        style.map('Treeview', background=[('selected', '#347083')])

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        notebook.add(tab1, text='Employees')
        notebook.add(tab2, text='Booked Tickets')
        notebook.add(tab3, text='Entered Tickets')
        notebook.add(tab4, text='Exit Tickets')
        
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
        if data:
            for entry in data:
                user_table.insert('', 'end', values=entry)
        else:
            user_table.insert('', 'end', values=('No data available',))

        user_table.pack(fill='both', expand=True)

        add_employee_button = ttk.Button(tab1, text="Add Employee", command=self.add_employee)
        add_employee_button.pack()

        booked_table = ttk.Treeview(tab2, columns=('ID', 'Seat Numbers','Number of persons','Number of clildren'))
        booked_table.heading('ID', text='ID')
        booked_table.heading('Seat Numbers', text='Seat Numbers')
        booked_table.heading('Number of persons', text='Number of persons')
        booked_table.heading('Number of clildren', text='Number of children')

        tickets = self.manager.all_tickets()
        if tickets:
            for entry in tickets:
                booked_table.insert('', 'end', values=entry)
        else:
            booked_table.insert('', 'end', values=('No data available',))

        booked_table.pack(fill='both', expand=True)


        entry_table = ttk.Treeview(tab3, columns=('Ticket_ID',))
        entry_table.heading('Ticket_ID', text='Ticket ID')
     
        entries = self.manager.all_entered_tickets()
        if entries:
            for entry in entries:
                entry_table.insert('', 'end', values=(entry[0],))
        else:
            entry_table.insert('', 'end', values=('No data available',))

        entry_table.pack(fill='both', expand=True)

        exit_table = ttk.Treeview(tab4, columns=('Ticket_ID','Number of persons left'))
        exit_table.heading('Ticket_ID', text='Ticket ID')
        exit_table.heading('Number of persons left', text='Number of persons left')

        exits = self.manager.all_exit_tickets()
        if exits:
            for entry in exits:
                exit_table.insert('', 'end', values=entry)
        else:
            exit_table.insert('', 'end', values=('No data available',))
        
        exit_table.pack(fill='both', expand=True)
    def add_employee(self):
        root = tk.Tk()
        app = EmployeeFormApp(root)
        
if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
