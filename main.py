from classes import Database
import os
from tabulate import tabulate
import logging 
import function
from art import tprint

if not os.path.exists("files"):
    os.mkdir("files")

logging.basicConfig(filename='logs/program_logs.log', filemode='a', format='%(levelname)s -> %(asctime)s: %(message)s', level=logging.DEBUG)
os.system('cls' if os.name == 'nt' else 'clear')
tprint("SQL-Viewer")

print("\nWelcome to SQL-Viewer!\n\nFor help type 'help'")

db = None

commands = ["edit", "rename", "create", "get", "del", "help", "select ", "showdbs", "delete_db", "create_db", "clear", "exit"]

while True:

    databases = []
    for f in os.listdir("files"):
        if f.endswith('.db'):
            databases.append(f)
    formatted_databases = ', '.join(databases)

    try:
        
        if db is not None:
            command = input(f"\n{db.nameDB} >>> ")
        else:
            command = input("\n>>> ")

        if not function.is_valid_command(command, commands):
            print("Command not found! or wrong command. Try again.")

        if command.lower() == "help":
            function.show_help()

        elif command.lower() == "get":
            print("\nThis command requires argument.\nFor help type 'help'")

        elif command.lower() == "del":
            print("\nThis command requires argument.\nFor help type 'help'")

        elif command.lower() == "create":
            print("\nThis command requires argument.\nFor help type 'help'")

        elif command.lower() == "rename":
            print("\nThis command requires argument.\nFor help type 'help'")

        elif command.lower() == "edit":
            print("\nThis command requires argument.\nFor help type 'help'")

        elif command.lower() == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            tprint("SQL-Viewer")
            print("\nWelcome to SQL-Viewer!\n\nFor help type 'help'")
        
        elif "select " in command.lower():
            db = function.select_command(command)

        elif "get " in command.lower():
            function.command_get(db, command)

        elif "del " in command.lower():
            function.command_del(db, command)

        elif "create " in command.lower():
            function.command_create(db, command)
                
        elif "rename " in command.lower():
            function.command_rename(db, command)
          
        elif "edit " in command.lower():
            function.command_edit(db, command)
                
        elif command.lower() == "showdbs":
            function.command_showdbs(databases, formatted_databases)
                
        elif command.lower() == "delete_db":
            name = input("Enter database name: ")
            if name == "cancel":
                print("\nOk. Canceled.")
            else:
                function.delete_database(db, name)

        elif command.lower() == "create_db":
            if db is None:
                name = input("Enter database name: ")
                if name == "cancel":
                    print("\nOk. Canceled.")
                else:
                    function.create_database(name)
            else:
                logging.info(f"User try to create database, but he selected another database.")
                print("You already have a database. Plese run `select cancel` to exit from selected database.")

        elif command.lower() == "exit":
            os.system('cls' if os.name == 'nt' else 'clear')
            logging.debug("Goodbye!")
            tprint("\nGoodbye!")
            break

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"\nError: {str(e)}")

    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        logging.debug("Goodbye!")
        tprint("\nGoodbye!")
        break
