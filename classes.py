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

    def get_all_tables(self):
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
            self.cur.execute(f"CREATE TABLE {table} (IgnoreOrDelete TEXT)")
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - create_table: {str(e)}")
        else:
            print(f"Successful! Created table: {table} in Database: {self.nameDB}")

    def create_column(self, column, table):
        # Check if the input is not empty
        if not column:
            print("Column name cannot be empty")
            return
        if not table:
            print("Table name cannot be empty")
            return
    
        type = input("Enter the type: ")
        if type.upper() in ["INTEGER", "TEXT", "REAL"]:
            parameters = [type.upper()]
            p_k = "PRIMARY KEY"
            d_v = "DEFAULT "
            parametr = input("Make primary key? (y/n): ")
            if parametr.lower() in ["y", "yes"]:
                parameters.append(p_k)
    
            parametr = input("Make default value? (y/n): ")
            if parametr.lower() in ["y", "yes"]:
                default = input("Enter default value: ")
                if default:
                    parameters.append(d_v+default)
                else:
                    print("Default value cannot be empty")
                    return
            parameters = " ".join(parameters)
    
        else:
            print("Invalid type. Please enter 'integer' or 'text'.")
            return
    
        try:
            if type.upper() in ["INTEGER", "TEXT", "REAL"]:
                self.cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {parameters};")
            # elif type.upper() == "TEXT":
            #     self.cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type.upper()};")
            self.conn.commit()
            print(f"Column '{column}' added to table '{table}'.")
        except sqlite3.OperationalError as e:
            print(f"Error | Method - create_column: {str(e)}")

    def create_record(self, table: str):
        """
        Создает новую запись в таблице.
    
        Args:
            table (str): Название таблицы, в которой нужно создать запись.
        """
        try:
            columns = self.get_all_columns(table)
            if not columns:
                raise ValueError(f"Table {table} not found.")
    
            non_primary_columns = [column[1] for column in columns if column[5] != 1]
            values = []
            for column in non_primary_columns:
                value = input(f"Enter value for {column}: ")
                values.append(value)
    
            if len(values) != len(non_primary_columns):
                raise ValueError("The number of provided values does not correspond to the number of columns, excluding the first and second columns.")
    
            sql = f"INSERT INTO {table} ({', '.join(non_primary_columns)}) VALUES ({', '.join('?' for _ in values)})"
            self.cur.execute(sql, values)
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - create_record: {str(e)}")
        else:
            values = ", ".join(values)
            print(f"\nSuccessful!\nTable: {table}\nDatabase: {self.nameDB}\nRecord: {values}")

    def rename_table(self, old_name: str, new_name: str):
        """
        Renames a table.

        Args:
            old_name (str): The name of the table to be renamed.
            new_name (str): The new name for the table.
        """
        try:
            self.cur.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - rename_table: {str(e)}")
        else:
            print(f"Successful!\nTable: {old_name}\nDatabase: {self.nameDB}\nNew name: {new_name}")

    def rename_column(self, table: str, old_name: str, new_name: str):
        """
        Renames a column in a table.

        Args:
            table (str): The name of the table in which the column is to be renamed.
            old_name (str): The name of the column to be renamed.
            new_name (str): The new name for the column.
        """
        try:
            self.cur.execute(f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name}")
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - rename_column: {str(e)}")
        else:
            print(f"Successful!\nTable: {table}\nDatabase: {self.nameDB}\nColumn: {old_name}\nNew name: {new_name}")

    def edit_column(self, table: str, column: str, new_type: str):
        """
        Edits the type of a column in a table.

        Args:
            table (str): The name of the table in which the column is to be edited.
            column (str): The name of the column to be edited.
            new_type (str): The new type for the column.
        """
        try:
            self.cur.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE {new_type}")
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - edit_column: {str(e)}")
        else:
            print(f"Successful!\nTable: {table}\nDatabase: {self.nameDB}\nColumn: {column}\nNew type: {new_type}")

    def edit_record(self, table: str, column: str, value: str, new_value: str):
        """
        Edits a record in a table.

        Args:
            table (str): The name of the table in which the record is to be edited.
            column (str): The name of the column in which the record is to be edited.
            value (str): The value of the record to be edited.
            new_value (str): The new value for the record.
        """
        try:
            self.cur.execute(f"UPDATE {table} SET {column} = ? WHERE {column} = ?", (new_value, value))
            self.conn.commit()
        except Exception as e:
            print(f"Error | Method - edit_record: {str(e)}")
        else:
            print(f"Successful!\nTable: {table}\nDatabase: {self.nameDB}\nColumn: {column}\nValue: {value}\nNew value: {new_value}")