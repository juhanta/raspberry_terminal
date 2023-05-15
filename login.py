
import PySimpleGUI as sg
import mysql.connector
import subprocess
import config
import time
import asyncio

#DB Connectin
mydb = mysql.connector.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.database
    )

#Open ErrorLayout if user is not found
def openError():
    errorWindow = sg.Window('Viga!', [  [sg.Text("Viga! Ei leia sellist kasutajat!")],[sg.OK()]], modal=True)   
    print("pole sellist kasutajat")
    event, values = errorWindow.read()
    errorWindow.close()

#Find user based on keycard ID
async def findUser(user):
    mycursor = mydb.cursor()
    mycursor.execute("""SELECT username FROM tbl_users WHERE keyID = %s""", (user,))
    result = mycursor.fetchall()
    mycursor.close()
    return result

async def isAdmin(user):
    mycursor = mydb.cursor()
    mycursor.execute("""SELECT * FROM synergyweb.tbl_ugmembers where GroupID = -1 AND UserName = %s""", (user))
    result = mycursor.fetchall()
    if len(result) > 0:
        return 1
    mycursor.close()

#1429692851

#Manage users window, add or remove Keys. 
def manageWindow():
    def getAllUsers():
        mycursor = mydb.cursor()
        mycursor.execute("""SELECT username, IFNULL(keyID,"") FROM synergyweb.tbl_users WHERE Comp_ID LIKE '%BNT%'""")
        result = mycursor.fetchall()
        mycursor.close()
        return result
    #Get names from list
    result = getAllUsers()
    name = [item[0] for item in result]

    layout = [
            [sg.Listbox(values = name, size=(20, 4), key='-LIST-', enable_events=True)],
            [sg.Text('KEY:'), sg.Input(key='-KEY-')],
            [sg.Button('Salvesta'), sg.Button('Tagasi')]
            ]
    manageWindow = sg.Window("Manage Window", layout)

    def update_input_field(values):
        person = result[name.index(values['-LIST-'][0])]
        keyId = person[1]
        manageWindow['-KEY-'].update(keyId)


    currentKey = manageWindow['-KEY-'].get()
    while True:
        event, values = manageWindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'Salvesta':
            if len(values['-KEY-']) <= 10:
                mycursor = mydb.cursor()
                newKey = currentKey if currentKey != '' else values['-KEY-']
                sql = """UPDATE synergyweb.tbl_users SET keyID = %s WHERE username = %s"""
                keys = (newKey, values['-LIST-'][0])
                mycursor.execute(sql, keys)
                mydb.commit()
                result = getAllUsers()
                manageWindow['-LIST-'].update(values=[item[0] for item in result])
                if mycursor.rowcount > 0:
                    sg.popup(f"Salvestatud")
                mycursor.close()
            else:
                sg.popup(f"Uksekaardi kood peab olema kuni 10 tähemärki")

        elif event == '-LIST-':
            update_input_field(values)
        elif event == '-KEY-':
            currentKey = values['-KEY-']
        elif event == 'Tagasi':
            manageWindow.close()


        
    
    
#Proceed to terminal or open manager window
def adminWindow():
    layout = [[sg.Button("Admin", size= (15,5)),sg.Button("Terminal", size= (15,5))]
             ]
    adminWindow = sg.Window("Admin Window", layout, modal=True, size=(300,200),  element_justification='c')
    while True:
        event, values = adminWindow.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Terminal":
            print("TERMINALI")
            adminWindow.close()
            time.sleep(5)
            window.close()
            break
        elif event == "Admin":
            print("admin")
            adminWindow.close()
            manageWindow()
            
    adminWindow.close()

# Main window content
layout = [  [sg.Text("Piiksuta kiipi")],     
            [sg.Input(do_not_clear=False)],
            [sg.OK()]]

# Create the window
window = sg.Window('Logi Sisse', layout)     
              



#Main function
async def main():
    # While loop to read the key values
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        else:    
            user =  await findUser(values[0])
            if len(user) > 0:   #If user found then 
                admin = await isAdmin(user[0])
                if admin == 1:
                    adminWindow()
                    
                else:
                    print('Hello', values[0], "! ")
                    print('Andmebaasist:', user)
                    # subprocess.run(["/home/user/Desktop/kiosk.sh"])
                    time.sleep(5)
                    window.close()
                    break

            else:
                openError()

asyncio.run(main())