import os
import sqlite3


class Database:
    """
    Represents a SQLite database.

    Attributes:
        nameDB (str): The name of the database file.
        conn (sqlite3.Connection): The database connection object.
        cur (sqlite3.Cursor): The cursor object for executing SQL queries.
    """

    def __init__(self, nameDB: str):
        """
        Initializes a new instance of the Database class.

        Args:
            nameDB (str): The name of the database file.
        """
        if not os.path.exists("files/"+nameDB):
            print("File not found")
        else:
            self.nameDB = nameDB
            self.conn = sqlite3.connect("files/"+self.nameDB)
            self.cur = self.conn.cursor()

    def get_all_tabels(self):
        """
        Returns all tables in the database.

        Returns:
            list: A list of tuples containing the names of all tables in the database.
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cur.fetchall()

    def get_all_columns(self, table: str):
        """
        Returns all columns in a table.

        Args:
            table (str): The name of the table.

        Returns:
            list: A list of tuples containing the names and types of all columns in the table.
        """
        try:
            self.cur.execute(f"PRAGMA table_info({table})")
            return self.cur.fetchall()

        except Exception as e:
            return print(f"Error | Method - get_all_columns: {str(e)}")

    def get_all_data(self, table: str):
        """
        Returns all data in a table.

        Args:
            table (str): The name of the table.

        Returns:
            list: A list of tuples containing all data in the table.
        """
        self.cur.execute(f"SELECT * FROM {table}")
        return self.cur.fetchall()

    def del_table(self, table: str):
        """
        Deletes a table from the database.

        Args:
            table (str): The name of the table to be deleted.
        """
        try:
            self.cur.execute(f"DROP TABLE {table}")
            self.conn.commit()

        except Exception as e:
            return print(f"Error | Method - del_table: {str(e)}")
        
        else:
            return print("Successful!")
        
    def del_column(self, column: str, table: str):
        """
        Deletes a column from a table.

        Args:
            column (str): The name of the column to be deleted.
            table (str): The name of the table from which the column is to be deleted.
        """
        try:
            self.cur.execute(f"ALTER TABLE {table} DROP COLUMN {column}")
            self.conn.commit()

        except Exception as e:
            return print(f"Error | Method - del_column: {str(e)}")
        
        else:
            return print("Successful!")
        
    def del_record(self, table: str, column: str, value: str):
        """
        Deletes a record from a table.

        Args:
            table (str): The name of the table from which the record is to be deleted.
            column (str): The name of the column used to identify the record.
            value (str): The value of the column used to identify the record.
        """
        try:
            self.cur.execute(f"DELETE FROM {table} WHERE {column} = ?", (value,))
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - del_record: {str(e)}")
        else:
            print("Successful!")


print("| SQL-Viewer |")

while True:

    databases = os.listdir("files")
    formatted_databases = ', '.join(databases)

    try:
        command = input("\n>>> ")

        if "select " in command.lower():
            print("\nSelecting database...")
            select = command.split(" ")[1]
            if select in databases:
                db = Database(select)
                print(f"\nSelected database: {select}")
            else:
                print("\nDatabase not found.")

        elif command.lower() == "exit":
            print("\nGoodbye!")
            break

        elif command.lower() in ["help", "commands"]:
            print("""Available commands:
                  
                  help - show this help
                  select - select database
                  databases - show available databases
                  tables - show tables in selected database
                  columns - show columns in selected table
                  data - show data in selected table
                  del_table - delete table in selected database
                  del_column - delete column in selected table
                  del_record - delete record in selected table
                  exit - exit the program""")

        elif command.lower() == "databases":
            print(f"\nAvailable databases: {formatted_databases}")

        elif command.lower() == "tables":
            if db is not None:
                print(f"\nTables in {select}: {db.get_all_tabels()}")
            else:
                print("\nNo database selected.")

        elif command.lower() == "columns":
            if db is not None:
                table = input("Table name: ")
                print(f"\nColumns in {table}: {db.get_all_columns(table)}")
            else:
                print("\nNo database selected.")

        elif command.lower() == "data":
            if db is not None:
                table = input("Table name: ")
                print(f"\nData in {table}: {db.get_all_data(table)}")
            else:
                print("\nNo database selected.")

        elif command.lower() == "del_table":
            if db is not None:
                table = input("\nTable name: ")
                db.del_table(table)
            else:
                print("\nNo database selected.")

        elif command.lower() == "del_column":
            if db is not None:
                table = input("\nTable name: ")
                column = input("\nColumn name: ")
                db.del_column(column, table)
            else:
                print("\nNo database selected.")

        elif command.lower() == "del_record":
            if db is not None:
                table = input("\nTable name: ")
                column = input("\nColumn name: ")
                value = input("\nValue: ")
                db.del_record(table, column, value)
            else:
                print("\nNo database selected.")

    except Exception as e:
        print(f"\nError: {str(e)}")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break

