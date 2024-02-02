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


    def close_connection(self):
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    # Create an instance of the DatabaseManager
    db_manager = DatabaseManager(
        host='localhost',
        username='root',
        password='Madan@333',
        database='automated_entry_system'
    )

    try:
        # Execute the SELECT query
        query = "SELECT * FROM employees"
        results = db_manager.execute_query(query)

        # Print the results
        for row in results:
            print(row)
        res = db_manager.check_user("johndoe", "securepassword")
        print(res)
    finally:
        # Close the database connection
        db_manager.close_connection()