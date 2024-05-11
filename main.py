from classes import Database
import os
from tabulate import tabulate

print("| SQL-Viewer |")

db = None

while True:

    databases = []
    for f in os.listdir("files"):
        if f.endswith('.db'):
            databases.append(f)
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
                if ".db" not in select:
                    select += ".db"
                    db = Database(select)
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
                tables = db.get_all_tabels()
                if not tables:
                    print("\nNo tables in selected Database.")
                else:
                    print(f"\nTables in {db.nameDB}:")
            
                headers = ["№", "Table"]
                table_data = []
                for index, table in enumerate(tables, start=1):
                    table_data.append([index, table[0]])
            
                table = tabulate(table_data, headers=headers, tablefmt="heavy_outline")
                print(table)


        elif command.lower() == "get_columns":
            if db is None:
                print("\nNo database selected.")
                

            table = input("Table name: ")
            if table not in [t[0] for t in db.get_all_tabels()]:
                print("\nTable not found. Try again.")
                

            try:
                columns = db.get_all_columns(table)
                if not columns:
                    raise ValueError("No columns in selected table.")
            except Exception as e:
                print(f"\nError: {str(e)}")
                

            headers = ["№", "Position", "Name", "Type", "NULL", "Default_value", "Primary_Key"]
            table_data = [[index, *column] for index, column in enumerate(columns, 1)]
            
            for row in table_data:
                for index, value in enumerate(row):
                    if value is None:
                        row[index] = "None"
            
            table = tabulate(table_data, headers=headers, tablefmt="heavy_outline")
            print(table)


        elif command.lower() == "get_data":
            if db is None:
                print("\nNo database selected.")

            table = input("Table name: ")
            try:
                if table not in [t[0] for t in db.get_all_tabels()]:
                    raise ValueError("Table not found. Try again.")
                
                data = db.get_all_data(table)
                if not data:
                    raise ValueError("No data in selected table.")
            except Exception as e:
                print(f"\nError: {str(e)}")
            else:
                columns = [column[1] for column in db.get_all_columns(table)]
                table_data = [dict(zip(columns, row)) for row in data]
                
                t = tabulate(table_data, headers="keys", tablefmt="heavy_outline")
                print(f"Table: {table}")
                print(t)

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
            if db is None:
                print("\nNo database selected.")
            else:
                table = input("\nTable name: ")
                if table not in [t[0] for t in db.get_all_tabels()]:
                    print("\nTable not found. Try again.")
                else:
                    column = input("\nColumn name: ")
                    if not column:
                        print("\nColumn name cannot be empty")
                    else:
                        db.create_column(column, table)

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


