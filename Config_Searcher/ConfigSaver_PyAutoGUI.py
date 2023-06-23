# Note:
#     Please place the Pycharm, Notepad++, and Config Searcher windows
#     in below appropriate places before start executing the file.
#     1.  Config Searcher (Top Right Corner)
#             Full screen -> W + Left -> W+Right -> W + Up
#     2.  Notepad++ (Bottom Right Corner)
#             Full screen -> W + Left -> W+Right -> W + Down
#     3.  Pycharm (Left side)
#             It will automatically ask you to select the place.

# ****** Documentations ******
# https://pyautogui.readthedocs.io/en/latest/
# https://www.youtube.com/watch?v=3PekU8OGBCA

import os
import time
from os.path import exists

import pyautogui

devices = ["NJ-BIGIP-FDSG-DMZ-1", "NJ-BIGIP-FDSG-DMZ-2"]

path = "C:\\Users\\dnarala\\PycharmProjects\\My-Network-Automation"

for device in devices:
    print(f"{path}\\{device}.txt")
    # Clears The Device Section And Replaces The New Device Name
    pyautogui.click(1236, 75, 1)  # Position for Device Text Box
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')

    pyautogui.write(device)

    # Clears The Search String Section -- Removed.

    #
    pyautogui.click(1894, 71, 1)   # Position GO Button.
    time.sleep(10)                 # It waits for 10 secs

    pyautogui.click(1111, 142, 1)  # Click on Results Section

    pyautogui.click(1411, 492, 1)  # Click On Config Section

    pyautogui.hotkey('ctrl', 'a')  # Selects all the config.

    pyautogui.hotkey('ctrl', 'c')  # Copy the config.

    pyautogui.click(1432, 756, 1)  # Notepad Edit Section.
    pyautogui.hotkey('ctrl', 'n')  # Creates a new text file.
    pyautogui.click(1432, 756, 1)  # Notepad Edit Section.
    pyautogui.hotkey('ctrl', 'a')  # Select all the content if any.
    pyautogui.hotkey('ctrl', 'v')  # Paste the config.
    pyautogui.hotkey('ctrl', 's')  # Saves the config.
    time.sleep(2)

    # File Validation - Checks if the device config is available already.
    # If config file is already available, it removes the file.
    file_exists = exists(f"{path}\\{device}.txt")
    if file_exists:
        print(file_exists)
        os.remove(f"{path}\\{device}.txt")

    pyautogui.click(1506, 554, 1)  # File Location Section.
    time.sleep(1)
    pyautogui.write(path)          # Replace The Path.
    time.sleep(1)
    pyautogui.press('enter')

    pyautogui.click(1249, 947, 2)  # File Name Section.
    pyautogui.hotkey('ctrl', 'a')  # Removes the file name if any.
    pyautogui.write(device)        # Name the file as Device name.
    pyautogui.click(1725, 1013, 1)  # Click on Save.

    pyautogui.click(1432, 756, 1)  # Notepad Edit Section.
    pyautogui.hotkey('ctrl', 'w')  # Close The File.

