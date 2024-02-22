import tkinter as tk
from tkinter import messagebox
import re 
from databasemanager import DatabaseManager

class EmployeeFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Form")
        self.manager = DatabaseManager(
            host='localhost',
            username='root',
            password='Madan@333',
            database='automated_entry_system'
        )
        self.create_widgets()

    def create_widgets(self):
        self.labels = ["Employee ID:", "Name:", "Phone Number:", "Email:", "Username:", "Password:", "Job Title:", "Salary:"]
        self.entries = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self.root, text=label_text)
            label.grid(row=i, column=0, sticky="e")

            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        submit_button = tk.Button(self.root, text="Submit", command=self.submit_form)
        submit_button.grid(row=len(self.labels), columnspan=2, pady=10)

    def submit_form(self):
        employee_data = [entry.get() for entry in self.entries]
        self.root.destroy()
        if self.validate_employee_data(employee_data):
            self.manager.add_employee(employee_data)
            for label, data in zip(self.labels, employee_data):
                print(label, data)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
        

 # Import regular expression module for email validation

    def validate_employee_data(self, data):
        # Check if any field is empty
        if not all(data):
            return False
        
        # Check password length
        if len(data[5]) < 8:  # Assuming password is at index 5 in the data list
            return False
        
        # Validate employee ID (assuming it should be an integer)
        if not data[0].isdigit():  # Assuming employee ID is at index 0
            return False
        
        # Validate phone number (assuming it should be 10 digits)
        if not data[2].isdigit() or len(data[2]) != 10:  # Assuming phone number is at index 2
            return False
        
        # Validate email using regular expression
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', data[3]):  # Assuming email is at index 3
            return False
        
        # Additional validation rules for other fields
        # For example, checking if username, job title, and name are not empty
        if not data[4] or not data[6] or not data[1]:  # Assuming username, job title, and name are at indexes 4, 6, and 1 respectively
            return False
        
        
        try:
            salary = float(data[7])
            if salary <= 0:
                return False
        except ValueError:
            return False
        
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeFormApp(root)
    root.mainloop()

