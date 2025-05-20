from flask import Flask, render_template, request, jsonify, redirect
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import os
from config import store_command_in_db, connect_to_db
import subprocess #for opening vs code

app = Flask(__name__)

# Function to give voice response using pyttsx3
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")    

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/commands')
def commands_page():
    return render_template('commands.html')      

@app.route('/search-history')
def search_history():
    connection = connect_to_db()
    if connection is None:
        return "Failed to connect to database."
    
    cursor = connection.cursor()

    try:
        # query to fetch the search history
        cursor.execute("SELECT created_at, command FROM users ORDER BY created_at DESC")
        search_data = cursor.fetchall() # get all records

        # pass data to the template
        return render_template('search_history.html', search_data=search_data)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Error fetching data"

    finally:
        cursor.close()
        connection.close()            

@app.route('/clear_history', methods=['POST'])
def clear_history():
    connection = connect_to_db()
    if connection is None:
        return "Failed to connect to database."
    
    cursor = connection.cursor()

    try:
        # query to clear history
        cursor.execute("DELETE FROM users")
        connection.commit()  # Commit the transaction

        return redirect('/search-history')  # Redirect back to the search history page

    except Exception as e:
        print(f"Error clearing data: {e}")
        return "Error clearing data"

    finally:
        cursor.close()
        connection.close()  

# Route to handle voice command
@app.route('/process_voice', methods=['POST'])
def process_voice():
    data = request.get_json()
    command = data.get('command')
    
    if command:
        processCommand(command)  # Process the command
        return jsonify({"status": "success", "command": command})
    return jsonify({"status": "error", "message": "No command received"})


def processCommand(command):
    # Store the command in the database
    store_command_in_db(command)

    if "open google" in command.lower():
        speak("Sure! I am openning google for you")
        webbrowser.open("https://www.google.co.in/") 
    elif "open email" in command.lower():
        speak("Sure! I am openning your emails for you")
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")   
    elif "open facebook" in command.lower():
        speak("Sure! I am openning facebook for you")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command.lower():
        speak("Sure! I am openning youtube for you")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command.lower():
        speak("Sure! I am openning linkedin for you")
        webbrowser.open("https://linkedin.com")
    elif "open github" in command.lower():
        speak("Sure! I am openning Github for you")
        webbrowser.open("https://github.com/")
    elif "initiate coding" in command.lower():
        speak("Initiating Coding mode. Let’s build something awesome!")
        subprocess.run([r'C:\Users\sohai\AppData\Local\Programs\Microsoft VS Code\Code.exe'], check=True)
        webbrowser.open("https://docs.python.org/3.12/")
        webbrowser.open("https://youtube.com")
        webbrowser.open("https://github.com/AamirSohail07000")
        webbrowser.open("https://google.com")
        webbrowser.open("https://www.w3schools.com/python/default.asp")
        webbrowser.open("https://linkedin.com")
    elif "how are you" in command.lower():
        speak("Hey,I'm doing great!,How can I help ?")       
    else:
        speak("Sorry, I did not understand the command.")



if __name__ == '__main__':
    app.run(debug=True)
