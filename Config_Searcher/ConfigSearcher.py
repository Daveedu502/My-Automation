import os
import sys
import time

from pywinauto.application import Application

# Start() helps when config searcher is not opened.
# app = Application(backend="uia").start(
#     r"C:\Users\dnarala\AppData\Local\Apps\2.0\97QCDNCC.V31\K1GM5J53.V4L\devi..tion_0000000000000000_0001.0005_53d2604abdf32823\Device_Configuration_Searcher.exe")

# Connect() helps when config searcher is already opened.
app = Application(backend="uia").connect(title_re=".*Searcher", class_name="Window")

# describe the window inside Notepad.exe process
dlg_spec = app.MonsterDeviceConfigurationSearcher
# wait till the window is really open
# time.sleep(10)
actionable_dlg = dlg_spec.wait('visible')

dlg_spec = app.window(title='Monster Device Configuration Searcher')
# print(dlg_spec)
# <pywinauto.application.WindowSpecification object at 0x0568B790>
dlg_spec.wrapper_object()
# print(dlg_spec.wrapper_object())
# <pywinauto.controls.win32_controls.DialogWrapper object at 0x05639B70>

# dlg_spec.print_control_identifiers()
# dlg_spec.Settings.click()


# devices = ["FRA-BIGIP-FDSG-DMZ-2", "NJ-BIGIP-FDSG-DMZ-1", "VA-BIGIP-FDSG-DMZ-1", "NJ-BIGIP-DMZ-2", "VA-BIGIP-DMZ-2",
#            "NJ-BIGIP-2", "VA-BIGIP-2", "NJ-BIGIP-3", "VA-BIGIP-3", "NJ-BIGIP-NP-1", "NS2 NJ-BIGIP-GSLB1",
#            "NJ-GSLB-FDSG-DMZ1", "NJ-BIGIP-FDSG-1", "VA-BIGIP-FDSG-1", "FRA-BIGIP-FDSG-1"]
# devices = ["NJ-BIGIP-FDSG-DMZ-1", "NJ-BIGIP-FDSG-DMZ-2", "VA-BIGIP-2"]

devices = ["VA-BIGIP-DMZ-2"]
# devices = ["NJ-BIGIP-3","VA-BIGIP-3","NRT-BIGIP-2","LHR-BIGIP-1","FRA-BIGIP-1","HKG-BIGIP-1","SYD-BIGIP-2","NJ-BIGIP-DMZ-2","VA-BIGIP-DMZ-2"]
path = "C:\\Users\\dnarala\\PycharmProjects\\My-Network-Automation\\Devices_Backup"

devices_names = ""
devices_count = 0
for device in devices:
    if devices_names == "":
        devices_names = device
    else:
        devices_names = devices_names + " " + device
    devices_count = devices_count + 1
print(f"Total Devices: {devices_count}")

# dlg_spec['Edit0'].set_text("Testing00")  # Working for Search String
# dlg_spec['Edit1'].set_text("Testing01")  # Working for Search String
# dlg_spec['Edit3'].set_text("Testing03")  # Working for Device
dlg_spec['Edit0'].set_text("")
dlg_spec['Edit3'].set_text("")
dlg_spec.Go.click()
dlg_spec['Edit3'].set_text(devices_names)
dlg_spec.Go.click()
# time.sleep(120)

today = time.strftime('%Y%m%d')
if not os.path.exists(str(today)):
    os.mkdir(str(today))
    print("Folder Created.!")
today = path



i = 0
print(dlg_spec['ListBox'].items())
while dlg_spec['ListBox'].items() == [] :
    time.sleep(3)
    if i >= 5*devices_count :
        break
    i = i +1
print(f"Timer Exited After Waiting For {i*3} seconds.!")

i = 0
for item in dlg_spec.ListBox.items():
    print(item)
    item.select()
    # print(item.is_selected())
    count = dlg_spec['Edit2'].line_count()
    print(f"Device: {devices[i]} \nLines Count: {count}")
    # print(dlg_spec['Edit2'].text_block())
    # If config file is already available, it removes the file.
    file_exists = os.path.exists(f"{today}\\{devices[i]}.txt")
    if file_exists:
        print(file_exists)
        os.remove(f"{today}\\{devices[i]}.txt")
    handler = open(f"{today}\\{devices[i]}.txt", "w")
    handler.write(dlg_spec['Edit2'].text_block())
    handler.close()
    i = i + 1


# Pinding Tasks.!!
    # File name should be the respective device name which should be pulled from the results section.
    # Failing after 8 devices though more than 8 devices exists in results section.
