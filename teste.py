import PySimpleGUI as sg
import time
import threading

# Function to perform calculations
def calculate():
    # Replace this with your actual calculations
    result = "Calculation done at " + time.strftime("%H:%M:%S")
    return result

# Main GUI
def main():
    sg.theme('Default')

    layout = [
        [sg.Text("Status: ", size=(15, 1)), sg.Text("Stopped", key="-STATUS-", size=(20, 1))],
        [sg.Multiline(size=(50, 10), key="-OUTPUT-", disabled=True, autoscroll=True)],
        [sg.Button("Start", key="-START-"), sg.Button("Cancel", key="-CANCEL-"), sg.Button("Exit")]
    ]

    window = sg.Window("Periodic Calculation", layout)
    running = False
    start_time = None

    while True:
        event, values = window.read(timeout=1000)  # Check events every second

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "-START-":
            running = True
            start_time = time.time()  # Record the current time
            window["-STATUS-"].update("Running")

        if event == "-CANCEL-":
            running = False
            window["-STATUS-"].update("Stopped")

        if running:
            current_time = time.time()
            if current_time - start_time >= 5:  # Check if 60 seconds have passed
                result = calculate()
                window["-OUTPUT-"].update(f"{result}\n", append=True)
                start_time = current_time  # Reset the timer

    window.close()


if __name__ == "__main__":
    main()
