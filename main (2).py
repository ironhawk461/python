from typing import Any
import psycopg2  # import the psycopg2 library to your python environment to do Postgres Database operations
from psycopg2 import sql
import logging
import getpass  # if you are using pycharm then remember to go to edit configuration and enable emulate terminal in

# output console to get the getpass library to work

# How the logging configuration of the logging library
logging.basicConfig(filename="output.log", level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
# A while loop for the connection of the SQL database
connecting = True
while connecting is True:
    logging.debug("Obtaining the username, password, hostname, and database from the user ")
    dbuser = str(input("What is your username? "))
    dbpass = getpass.getpass(prompt="What is your password? ")
    dbhost = str(input("What is the hostname for your server? "))
    dbdata = str(input("What is the database name for your server? "))
    try:
        logging.debug("Trying to connect with the SQL server")
        connection = psycopg2.connect(  # This is the connection string for your Postgres Database server
            host=dbhost,  # The connecting Database host, which means the location of you DB
            database=dbdata,  # The database name in your host
            user=dbuser,  # The user name of your database
            password=dbpass,
        )
        connection.set_session(autocommit=True)
        logging.debug("Connection into " + dbdata + " by the user " + dbuser + " was successful")
        print("Connection into", dbdata, "was successful")
        connecting = False
    except psycopg2.OperationalError:
        logging.debug("Connection into " + dbdata + " by the user " + dbuser + " was unsuccessful")
        print("Could not connect to the database, please re-input information")


def count_rows(table_name: str, limit: int) -> str | Any:
    try:
        logging.debug("Attempting to check the tables that were specified by the user")
        with connection.cursor() as cursor:
            stmt = sql.SQL("""
            SELECT
                COUNT(*)
            FROM (
                SELECT
                    1
                FROM
                    {table_name}
                LIMIT
                    {limit}
            ) AS limit_query
        """).format(
                table_name=sql.Identifier(table_name),
                limit=sql.Literal(limit),
            )
            cursor.execute(stmt)
            result = cursor.fetchone()

        rowcount, = result
        logging.debug("Table was found")
        return rowcount
    except:
        logging.debug("Table not found")
        print("Table not found. You have have inputted an incorrect an table name")


def is_admin(username: str) -> bool:
    logging.debug("Checking the username if it is admin")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                admin
            FROM
                users
            WHERE
                username = %(username)s
        """, {
            'username': username
        })
        result = cursor.fetchone()

    if result is None:
        # User does not exist
        return False
    else:
        admin, = result
        return admin


admin_name_quit_count = True
while admin_name_quit_count is True:
    choice = str(input("Please enter either 'admin' to input a username with admin account, 'count rows' to display the"
                       " rows for a table, or 'Q' to quit the operation: "))
    if choice == "admin":
        adname = str(input("Please input the username for the admin account: "))
        if is_admin(adname) is True:
            logging.debug("The username that the user inputted has administrative rights")
            print(is_admin(adname))
        else:
            logging.debug("The username that the user inputted does not have administrative rights")
            print(is_admin(adname))
    elif choice == "count rows":
        logging.debug("user is checking the the rows of a desired table ")
        flag = True
        rows = str(input("Please enter the table name: "))
        limit = input("Please input a limit for the table: ")
        logging.debug("Checking if the limit that was inputted was an integer")
        try:
            int(limit)
            logging.debug("The limit that was inputted was an integer")
        except ValueError:
            flag = False
            logging.debug("The limit that was inputted was not an integer")
        if flag:
            logging.debug("Printing the rows of the desired table")
            print(count_rows(rows, limit))
        else:
            print("Please input a number value into the limit")
    elif choice == "Q":
        logging.debug("Quitting system")
        break
    else:
        print("Invalid input, please try again: ")
