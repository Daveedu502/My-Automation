import os
import sys
import time
import xlsxwriter

from pywinauto.application import Application
from os.path import exists

app = Application(backend="uia").connect(title_re=".*Searcher", class_name="Window")
dlg_spec = app.MonsterDeviceConfigurationSearcher
dlg_spec.wrapper_object()
# dlg_spec.minimize()
#
# dlg_spec['Edit0'].set_text("")
# dlg_spec['Edit3'].set_text("")
# dlg_spec.Go.click()
# dlg_spec['Edit3'].set_text("%BIGIP%")
# dlg_spec.Go.click()

i = 1
while True:
    if not dlg_spec['ListBox'].items():
        time.sleep(5)
    else:
        break

count = int(dlg_spec['devices'].texts()[0].replace(" devices", ""))
print(f"{count} Devices there in results section.\nThis may take a few minutes.\nPlease wait...!!")

devices = []
items_list = []
index = 0
i = 0
while True:
    if i == 0:
        for item in dlg_spec['ListBox'].items():
            if item not in items_list:
                name = str(item.texts()[0])
                devices.append(name)
                items_list.append(item)
                item.select()
                i = 1
    if i > 0:
        index = dlg_spec['ListBox'].items().index(items_list[-1])
        for item in dlg_spec['ListBox'].items()[index:]:
            if item not in items_list:
                name = str(item.texts()[0])
                devices.append(name)
                items_list.append(item)
                item.select()

    if len(items_list) == count:
        break
    print(f"sofar items list: {len(items_list)}")
i = 1
strr = ""
devices.sort()
for device in devices:
    print(f"{i}. {device}")
    strr = strr + device + " "
    i += 1

print(strr)