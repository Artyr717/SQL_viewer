# The class `Database` represents a SQLite database and provides methods for interacting with tables,
# columns, data, and database operations.
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
            fail = input("Database not found. Create a new database? (y/n): ")
            if fail in ["y", "Y", "yes", "Yes"]:
                self.nameDB = nameDB
                if ".db" not in self.nameDB:
                    self.conn = sqlite3.connect("files/"+self.nameDB+".db")
                else:
                    self.conn = sqlite3.connect("files/"+self.nameDB)
                self.cur = self.conn.cursor()

            elif fail in ["n", "N", "no", "No"]:
                print("Exiting...")
                exit()

            else:
                print("Invalid input. Exiting...")
                exit()

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

    def create_table(self, table: str):
        """
        Creates a new table in the database.

        Args:
            table (str): The name of the table to be created.
        """
        try:
            self.cur.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY)")
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - create_table: {str(e)}")

    def create_column(self, column: str, table: str):
        """
        Creates a new column in a table.

        Args:
            column (str): The name of the column to be created.
            table (str): The name of the table in which the column is to be created.
        """
        type = input("Enter the type: ")
        if type == "INTEGER":
            patametr = input("Make primary key? (y/n): ")
            if patametr == "y":
                type = "INTEGER PRIMARY KEY"
            else:
                type = "INTEGER"

        if type == "TEXT":
            pass

        else:
            print("Invalid type")
            return
        try:
            self.cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type.upper()}")
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - create_column: {str(e)}")

    def create_record(self, table: str, column: str, value: str):
        """
        Creates a new record in a table.

        Args:
            table (str): The name of the table in which the record is to be created.
            column (str): The name of the column in which the record is to be created.
            value (str): The value of the record to be created.
        """
        try:
            self.cur.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - create_record: {str(e)}")

    def DeleteDatabase(self):
        """
        Deletes the database.
        """
        try:
            self.conn.close()
            os.remove(f"files/{self.nameDB}")
            print("Successful!")
        except Exception as e:
            print(f"Error | Method - DeleteDatabase: {str(e)}")


print("| SQL-Viewer |")

db = None

while True:

    databases = os.listdir("files")
    formatted_databases = ', '.join(databases)

    try:
        
        command = input("\n>>> ")

        if command.lower() in ["help", "commands"]:
            print("""Available commands:
                  
                  help - show this help
                  select - select database
                  showdbs - show available databases
                  get_tables - show tables in selected database
                  get_columns - show columns in selected table
                  get_data - show data in selected table
                  del_table - delete table in selected database
                  del_column - delete column in selected table
                  del_record - delete record in selected table
                  create_table - create new table in selected database
                  create_column - create new column in selected table
                  create_record - create new record in selected table
                  delete_database - delete selected database
                  exit - exit the program""")

        elif "select " in command.lower():
            print("\nSelecting database...")
            select = command.split(" ")[1]
            if select == "" or select == " ":
                print("\nNo database selected. Try again.")
            else:
                db = Database(select)
                print(f"\nSelected database: {select}")

        elif command.lower() == "exit":
            print("\nGoodbye!")
            break

        elif command.lower() == "showdbs":
            if not databases:
                print("\nNo databases found. Try again.")
            else:
                print(f"\nAvailable databases: {formatted_databases}")

        elif command.lower() == "get_tables":
            if db is not None:
                if db.get_all_tabels() == []:
                    print("\nNo tables in selected Database.")
                else:
                    print(f"\nTables in {select}:")
                    
                    print("""╔════════════════╗""")
                    for table in db.get_all_tabels():
                        print(" "*8 +table[0])
                    print("""╚════════════════╝""")
            else:
                print("\nNo database selected.")

        elif command.lower() == "get_columns":
            if db is not None:
                table = input("Table name: ")
                for column in db.get_all_columns(table):
                    print(column)
            else:
                print("\nNo database selected.")

        elif command.lower() == "get_data":
            if db is not None:
                table = input("Table name: ")
                print(f"\nData in {table}:")
                for row in db.get_all_data(table):
                    print(row)
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

        elif command.lower() == "create_table":
            if db is not None:
                table = input("\nTable name: ")
                db.create_table(table)
            else:
                print("\nNo database selected.")

        elif command.lower() == "create_column":
            if db is not None:
                table = input("\nTable name: ")
                column = input("\nColumn name: ")
                db.create_column(column, table)
            else:
                print("\nNo database selected.")

        elif command.lower() == "create_record":
            if db is not None:
                table = input("\nTable name: ")
                column = input("\nColumn name: ")
                value = input("\nValue: ")
                db.create_record(table, column, value)
            else:
                print("\nNo database selected.")

        elif command.lower() == "delete_database":
            if db is not None:
                db.DeleteDatabase()
            else:
                print("\nNo database selected.")

    except Exception as e:
        print(f"\nError: {str(e)}")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break


