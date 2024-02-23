import mysql.connector

class DatabaseManager:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            username=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, values=None):
        if not self.connection or not self.cursor:
            self.connect()

        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)

        result = self.cursor.fetchall()
        return result

    def check_user(self, username, password):
        query = "SELECT * FROM employees WHERE username = %s AND password = %s"
        values = (username, password)
        result = self.execute_query(query, values)
        
        if result:
            return result
        else:
            return False
        
    def check_ticket(self,ticket_id):
        nop = 0
        tk,nop = self.check_if_exit(ticket_id)
        if (nop):
            query = "DELETE FROM exit_tickets WHERE ticket_id = %s"
            values = (ticket_id,)
            self.execute_query(query, values)
            self.connection.commit()
            return 200,nop
        
        elif(self.check_if_entered(ticket_id)):
            return 500,nop
        else:   
            query = "SELECT * FROM tickets WHERE ticket_id = %s"
            values = (ticket_id,)
            result = self.execute_query(query, values)
            if result:
                self.add_to_entered(ticket_id)
                return result,nop
            else:
                return 400,nop
            

    def check_if_entered(self,ticket_id):
        query = "SELECT * FROM entered_tickets" 
        result = self.execute_query(query)
        for row in result:
            if row[0] == ticket_id:
                return True
        return False
    
    def check_if_exit(self,ticket_id):
        query = "SELECT * FROM exit_tickets" 
        nop = 0
        result = self.execute_query(query)
        for row in result:
            if row[0] == ticket_id:
                nop = row[1]
                return ticket_id,nop
        return ticket_id,nop
    
    def add_to_entered(self,ticket_id):
        query = "INSERT INTO entered_tickets (ticket_id) VALUES (%s)"
        values = (ticket_id,)
        self.execute_query(query, values)
        self.connection.commit()


    def close_connection(self):
        if self.connection:
            self.connection.close()

    def add_to_exit(self,ticket_id,no_of_persons):
        if self.exit_check(ticket_id) is not None:
            query = "UPDATE exit_tickets SET number_of_persons_left = number_of_persons_left + %s WHERE ticket_id = %s"
            values = (no_of_persons,ticket_id)
            self.execute_query(query, values)
            self.connection.commit()
            return
        else:
            query = "INSERT INTO exit_tickets (ticket_id,number_of_persons_left) VALUES (%s,%s)"
            values = (ticket_id,no_of_persons)
            self.execute_query(query, values)
            self.connection.commit()

    def all_employees(self):
        query = "SELECT * FROM employees"
        result = self.execute_query(query)
        return result
    
    def all_tickets(self):
        query = "SELECT * FROM tickets"
        result = self.execute_query(query)
        return result
    
    def all_entered_tickets(self):
        query = "SELECT * FROM entered_tickets"
        result = self.execute_query(query)
        return result
    
    def all_exit_tickets(self):
        query = "SELECT * FROM exit_tickets"
        result = self.execute_query(query)
        return result
    
    def exit_check(self,ticket_id):
        query = "SELECT * FROM exit_tickets where ticket_id = %s"
        result = self.execute_query(query, (ticket_id,))
        if result:
            return result
        else:
            return None
        
    def add_employee(self, employee_data):
        query = "INSERT INTO employees (employee_id, name, phone_number, email, username, password, job_title, salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.execute_query(query, employee_data)
        self.connection.commit()
