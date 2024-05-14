import sqlite3
import os
import logging
from tabulate import tabulate

from classes import Database

logging.basicConfig(filename='logs/function_logs.log', filemode='a', format='%(levelname)s -> %(asctime)s: %(message)s', level=logging.DEBUG)

def is_valid_command(command: str, commands: list) -> bool:
    """
    Checks if a given command is valid.
    """
    return command.lower() in commands or command.lower().startswith(("edit ", "rename ", "create ", "del ", "get ", "select "))

def create_database(name: str):
    if ".db" not in name:
        name = name + ".db"
        print(f"Creating database {name}...")
        database_files = os.listdir("files")
        if name not in database_files:
            try:
                conn = sqlite3.connect(f"files/{name}")
                cur = conn.cursor()
                logging.info(f"Successful! Created Database: {name}")
            except Exception as e:
                logging.error(f"Error | Method - create_database: {str(e)}")
        else:
            logging.error(f"Error | Method - create_database: Database {name} already exists.")
            print(f"Database {name} already exists.")

def delete_database(db: Database, name: str):
    if db is not None:
        print("Ops, you can't delete the database while you are using it.\nPlease, enter the command `select cancel` to close up the database.")

    else:
        if ".db" not in name:
            name = name + ".db"
            if name in os.listdir("files"):
                question = input(f"Are you sure you want to delete database {name}? (y/n): ")
                if question.lower() in ["y", "yes"]:
                    try:
                        os.remove(f"files/{name}")
                        logging.info(f"Successful! Deleted database: {name}.")
                    except Exception as e:
                        logging.error(f"Error | Method - DeleteDatabase: {str(e)}.")
                    else:
                        print("Deleted.")
                else:
                    print("Canceled.")

            else:
                logging.error(f"Error | Method - DeleteDatabase: Database {name} not found.")
                print(f"Database {name} not found.")

def show_help():
    headers = ["Command", "Description", "Parameters"]
    table_data = [
                ["help", "show this help", ""],
                ["select", "select database", "database name"],
                ["showdbs", "show available databases", ""],
                ["get", "show tables, columns and data in selected database", "table_name"],
                ["get tables", "show tables in selected database", ""],
                ["get columns", "show columns in selected table", "table_name"],
                ["get data", "show data in selected table", "table_name, column_name"],
                ["del", "delete table, column, record from selected database", "table_name, column_name, record_id"],
                ["del table", "delete table from selected database", "table_name"],
                ["del column", "delete column from selected table", "table_name, column_name"],
                ["del record", "delete record from selected table", "table_name, column_name, value"],
                ["create", "create new table, column, record in selected database", "table_name, column_name, value"],
                ["create table", "create new table in selected database", "table_name"],
                ["create column", "create new column in selected table", "table_name, column_name, data_type"],
                ["create record", "create new record in selected table", "table_name, column_name=value"],
                ["edit", "edit database, table, column, record", "table_name, column_name=value, record_id"],
                ["edit column", "edit column in selected table", "table_name, column_name, data_type"],
                ["edit record", "edit record in selected table", "table_name, column_name=value"],
                ["rename", "rename table, column", "database_name, table_name, column_name"],
                ["rename table", "rename table in selected database", "table_name"],
                ["rename column", "rename column in selected table", "table_name, column_name, new_column_name"],
                ["delete_db", "delete selected database", "database_name"],
                ["create_db", "create new database", "database_name"],
                ["clear", "clear the screen", ""],
                ["exit", "exit the program", ""]]
    table = tabulate(table_data, headers=headers, tablefmt="heavy_grid")
    print(f"\n{table}")

def select_command(command: str):
    logging.debug(f"Selecting database... {command}")
    print("\nSelecting database...")
    select = command.split(" ")[1]
    if select == "" or select == " ":
        logging.error(f"No database selected.")
        print("\nNo database selected. Try again.")
    elif select =="cancel":
        db = None
        logging.info(f"Database selection cancelled.")
        print("\nDatabase selection cancelled.")
    else:
        if ".db" not in select:
            select += ".db"
            db = Database(select)
        else:
            db = Database(select)
        logging.info(f"Selected database: {select}")
        print(f"\nSelected database: {select}")
    return db

def command_showdbs(databases, formatted_databases):
    if not databases:
        logging.info(f"No databases found.")
        print("\nNo databases found. Try again.")
    else:
        logging.info(f"Available databases: {formatted_databases}")
        print(f"\nAvailable databases: {formatted_databases}")

def command_get_tables(db: Database):
    if db is None:
        print("\nNo database selected.")
        return
    
    try:
        tables = db.get_all_tables()
    except Exception as e:
        print(f"\nError: {str(e)}")
        return
    
    if not tables:
        print("\nNo tables in selected database.")
    else:
        print(f"\nTables in {db.nameDB}:")
        headers = ["№", "Table"]
        table_data = [[index, table[0]] for index, table in enumerate(tables, start=1)]
        table = tabulate(table_data, headers=headers, tablefmt="heavy_outline")
        print(table)

def command_get_columns(db: Database, table_name: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")
        

    if table_name not in [t[0] for t in db.get_all_tables()]:
        logging.info(f"Table not found. Try again.")
        print("\nTable not found. Try again .")
        
    else:
        try:
            columns = db.get_all_columns(table_name)
            headers = ["№", "Position", "Name", "Type", "NULL", "Default_value", "Primary_Key"]
            table_data = [[index, *column] for index, column in enumerate(columns, 1)]
        
            for row in table_data:
                for index, value in enumerate(row):
                    if value is None:
                        row[index] = "None"
                
            table = tabulate(table_data, headers=headers, tablefmt="heavy_outline")
            print(table)
            if not columns:
                raise ValueError("No columns in selected table.")
        
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"\nError: {str(e)}")
        
def command_get_data(db: Database, table_name: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")

    try:
        if table_name not in [t[0] for t in db.get_all_tables()]:
            raise ValueError("Table not found. Try again.")
        
        data = db.get_all_data(table_name)
        if not data:
            raise ValueError("No data in selected table.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"\nError: {str(e)}")
    else:
        columns = [column[1] for column in db.get_all_columns(table_name)]
        table_data = [dict(zip(columns, row)) for row in data]
                
        t = tabulate(table_data, headers="keys", tablefmt="heavy_outline")
        print(f"Table: {table_name}")
        print(t)

def command_get(db: Database, command: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")

    else:
        tables = db.get_all_tables()
        table_names = [table[0] for table in tables]
        try:
            command = command.split(" ")
            if command[1] == "" or command[1] == " ":
                raise ValueError("No parameter provided. Try again.")
            else:
                if command[1] == "tables":
                    command_get_tables(db)

                elif command[1] == "columns":
                    print("\nTables:", ", ".join(table_names))
                    table_name = input("\nTable name: ")
                    if table_name == "cancel":
                        print("\nOk. Canceled.")
                    else:
                        command_get_columns(db, table_name)

                elif command[1] == "data":
                    print("\nTables:", ", ".join(table_names))
                    table_name = input("\nTable name: ")
                    if table_name == "cancel":
                        print("\nOk. Canceled.")
                    else:
                        command_get_data(db, table_name)

                else:
                    raise ValueError("Invalid parameter. Try again.")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"\nError: {str(e)}")

def command_del(db: Database, command: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")

    else:
        try:
            command = command.split(" ")
            if command[1] == "" or command[1] == " ":
                raise ValueError("No parameter provided. Try again.")
            else:
                tables = db.get_all_tables()
                table_names = [table[0] for table in tables]

                
                if command[1] == "table":
                    print("\nTables:", ", ".join(table_names))
                    table = input("\nTable name: ")
                    if table == "cancel":
                        print("\nOk. Canceled.")
                    else:
                        db.del_table(table)

                elif command[1] == "column":
                    print("\nTables:", ", ".join(table_names))
                    table = input("\nTable name: ")
                    if table == "cancel":
                        print("\nOk. Canceled.")
                    else:
                        columns = db.get_all_columns(table)
                        column_names = [column[1] for column in columns]
                        print("\nColumns:", ", ".join(column_names))
                        column = input("\nColumn name: ")
                        if column == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            db.del_column(column, table)

                elif command[1] == "record":
                    print("\nTables:", ", ".join(table_names))
                    table = input("\nTable name: ")
                    if table == "cancel":
                        print("\nOk. Canceled.")
                    
                    else:
                        print("\nColumns:", ", ".join(column_names))
                        column = input("\nColumn name: ")
                        if column == "cancel":
                            print("\nOk. Canceled.")
                            
                        else:
                            value = input("\nValue: ")
                            if value == "cancel":
                                print("\nOk. Canceled.")
                            else:
                                db.del_record(table, column, value)

                else:
                    raise ValueError("Invalid parameter. Try again.")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"\nError: {str(e)}")
        
def command_create(db: Database, command: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")

    else:
        try:
            command = command.split(" ")
            if command[1] == "" or command[1] == " ":
                raise ValueError("No parameter provided. Try again.")
            else:
                tables = db.get_all_tables()
                table_names = [table[0] for table in tables]

                if command[1] == "table":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        print("\nAvailable tables:", ", ".join(table_names))
                        table = input("\nTable name: ")
                        if table.lower() == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            db.create_table(table)
                        
                elif command[1] == "column":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        tables = [t[0] for t in db.get_all_tables()]
                        print("\nAvailable tables:", ", ".join(tables))
                        table = input("\nTable name: ")
                        if table.lower() == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            column = input("\nColumn name: ")
                            if column.lower() == "cancel":
                                print("\nOk. Canceled.")
                            else:
                                db.create_column(column, table)
                            
                elif command[1] == "record":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        tables = [t[0] for t in db.get_all_tables()]
                        print("\nAvailable tables:", ", ".join(tables))
                        table = input("\nTable name: ")
                        if table == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            db.create_record(table)

                else:
                    raise ValueError("Invalid parameter. Try again.")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"\nError: {str(e)}")
            
def command_rename(db: Database, command: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")

    else:
        try:
            command = command.split(" ")
            if command[1] == "" or command[1] == " ":
                raise ValueError("No parameter provided. Try again.")
            else:

                if command[1] == "table":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        tables = [t[0] for t in db.get_all_tables()]
                        print("\nAvailable tables:", ", ".join(tables))
                        table = input("\nTable name: ")
                        if table == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            new_name = input("\nNew table name: ")
                            if new_name == "cancel":
                                print("\nOk. Canceled.")
                            else:
                                db.rename_table(table, new_name)
                                    
                elif command[1] == "column":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        tables = [t[0] for t in db.get_all_tables()]
                        print("\nAvailable tables:", ", ".join(tables))
                        table = input("\nTable name: ")
                        if table == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            columns = [c[0] for c in db.get_all_columns(table)]
                            column = input("\nColumn name: ")
                            if column == "cancel":
                                print("\nOk. Canceled.")
                            else:
                                new_name = input("\nNew column name: ")
                                if new_name == "cancel":
                                    print("\nOk. Canceled.")
                                else:
                                    db.rename_column(table, column, new_name)

                else:
                    raise ValueError("Invalid parameter. Try again.")
                
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"\nError: {str(e)}")
            
def command_edit(db: Database, command: str):
    if db is None:
        logging.info(f"No database selected.")
        print("\nNo database selected.")

    else:
        try:
            command = command.split(" ")
            if command[1] == "" or command[1] == " ":
                raise ValueError("No parameter provided. Try again.")
            else:
                tables = db.get_all_tables()
                table_names = [table[0] for table in tables]

                if command[1] == "column":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        tables = [t[0] for t in db.get_all_tables()]
                        print("\nAvailable tables:", ", ".join(tables))
                        table = input("\nTable name: ")
                        if table == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            column = input("\nColumn name: ")
                            if column == "cancel":
                                print("\nOk. Canceled.")
                            else:
                                new_column_type = input("\nNew column type: ")
                                if new_column_type == "cancel":
                                    print("\nOk. Canceled.")
                                else:
                                    db.edit_column_type(table, column, new_column_type)

                elif command[1] == "record":
                    if db is None:
                        logging.info(f"No database selected.")
                        print("\nNo database selected.")
                    else:
                        
                        tables = [t[0] for t in db.get_all_tables()]
                        print("\nAvailable tables:", ", ".join(tables))
                        
                        table = input("\nTable name: ")
                        if table == "cancel":
                            print("\nOk. Canceled.")
                        else:
                            columns = db.get_all_columns(table)
                            column_names = [column[1] for column in columns]
                            
                            print("\nAvailable columns:", ", ".join(column_names))
                            
                            column = input("\nColumn name: ")
                            if column == "cancel":
                                print("\nOk. Canceled.")
                            else:
                                
                                id_column = db.get_all_columns(table)
                                id_column_name = id_column[0]
                                
                                values_in_selected_column = db.get_all_data(table)
                                values_in_selected_column = [value[id_column_name] for value in values_in_selected_column] 
                                
                                print("\nAvailable values:", "\n".join(values_in_selected_column))
                                
                                value = input("\nValue: ")
                                if value == "cancel":
                                    print("\nOk. Canceled.")
                                else:
                                    new_value = input("\nNew value: ")
                                    if new_value == "cancel":
                                        print("\nOk. Canceled.")
                                    else:
                                        db.edit_record(table, column, value, new_value)

                else:
                    raise ValueError("Invalid parameter. Try again.")

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"\nError: {str(e)}")