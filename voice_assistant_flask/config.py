import mysql.connector
from mysql.connector import Error
# music = {
#     "stealth": "https://www.youtube.com/watch?v=U47Tr9BB_wE",
#     "march": "https://www.youtube.com/watch?v=Xqeq4b5u_Xw",
#     "skyfall": "https://www.youtube.com/watch?v=DeumyOzKqgI&pp=ygUHc2t5ZmFsbA%3D%3D",
#     "wolf": "https://www.youtube.com/watch?v=ThCH0U6aJpU&list=PLnrGi_-oOR6wm0Vi-1OsiLiV5ePSPs9oF&index=21"
# }

import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",     # Change if you're using a remote server
            user="root", # Your MySQL username
            password="786123@Ms", # Your MySQL password
            database="voice_assistant_db"  # The database you created
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL DB: {e}")
        return None

def store_command_in_db(command):
    connection = connect_to_db()
    if connection is None:
        print("Failed to connect to database.")
        return

    cursor = connection.cursor()
    sql = "INSERT INTO users (command) VALUES (%s)"
    try:
        cursor.execute(sql, (command,))
        connection.commit()
        print("Command stored successfully.")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()

def processCommand(command):
    store_command_in_db(command)  # Store command in database
    # Additional command processing logic...
