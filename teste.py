import json
import os
import PySimpleGUI as sg

# Get the AppData folder path
appdata_path = os.getenv("APPDATA")
if not appdata_path:
    sg.popup_error("AppData folder not found!")
    exit()

# Define the file path in AppData
file_path = os.path.join(appdata_path, "user_data_list.json")

# Load existing data from the JSON file
if os.path.exists(file_path):
    with open(file_path, "r") as json_file:
        data_list = json.load(json_file)
else:
    data_list = []

# Layout for the GUI
layout = [
    [sg.Text("Name:"), sg.InputText(key="name")],
    [sg.Text("Age:"), sg.InputText(key="age")],
    [sg.Text("Email:"), sg.InputText(key="email")],
    [sg.Text("Country:"), sg.InputText(key="country")],
    [sg.Button("Add"), sg.Button("Save"), sg.Button("Cancel")],
    [sg.Multiline(size=(50, 10), key="output", disabled=True, autoscroll=True)]
]

# Create the window
window = sg.Window("JSON File with List of Dictionaries", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Cancel":
        break
    elif event == "Add":
        # Validate and add the new data to the list
        name, age, email, country = values["name"], values["age"], values["email"], values["country"]

        if not all([name, age, email, country]):
            sg.popup_error("All fields must be filled!")
        else:
            try:
                # Add the new dictionary to the list
                new_entry = {"name": name, "age": age, "email": email, "country": country}
                data_list.append(new_entry)

                # Update the output field to show the added entry
                window["output"].update(f"Added: {new_entry}\n", append=True)

                # Clear the input fields
                window["name"].update("")
                window["age"].update("")
                window["email"].update("")
                window["country"].update("")
            except Exception as e:
                sg.popup_error(f"An error occurred: {e}")

    elif event == "Save":
        # Save the updated list to the JSON file
        try:
            with open(file_path, "w") as json_file:
                json.dump(data_list, json_file, indent=4)

            sg.popup(f"Data saved to {file_path} successfully!")
        except Exception as e:
            sg.popup_error(f"An error occurred: {e}")

window.close()
