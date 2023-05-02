
import PySimpleGUI as sg
import mysql.connector
import subprocess
import config
import time

# Define the window's contents

layout = [  [sg.Text("Piiksuta kiipi")],     # Part 2 - The Layout
            [sg.Input(do_not_clear=False)],
            [sg.OK()]]

# Create the window
window = sg.Window('Logi Sisse', layout)      # Part 3 - Window Defintion
                 
# While loop to read the key values
#1429692851
print(config.host)

while True:
    event, values = window.read()
    mydb = mysql.connector.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.database
    )
    mycursor = mydb.cursor()
    mycursor.execute("""SELECT fullname FROM tbl_users WHERE keyID = %s""", (values[0],))
    result = mycursor.fetchall()

    if len(result) > 0:
        print('Hello', values[0], "! ")
        print('Andmebaasist:', result)
        subprocess.run(["/home/user/Desktop/kiosk.sh"])
        time.sleep(5)
        window.close()
        break

    else:
        errorWindow = sg.Window('Viga!', [  [sg.Text("Viga! Ei leia sellist kasutajat!")],[sg.OK()]])
        print("pole sellist kasutajat")
        event, values = errorWindow.read()
        errorWindow.close()

