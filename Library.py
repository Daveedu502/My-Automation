import os
import time
import xlsxwriter

from pywinauto.application import Application
from os.path import exists

# *********** Global Variables Starts ************

path = "C:\\Users\\dnarala\\PycharmProjects\\My-Network-Automation\\Devices_Backup"


# *********** Global Variables Ends ************

# *********** Getting Devices Backup Starts **********

def get_device_config(device_list):
    """
    :param device_list:
    """
    app = Application(backend="uia").connect(title_re=".*Searcher", class_name="Window")
    dlg_spec = app.MonsterDeviceConfigurationSearcher
    # actionable_dlg = dlg_spec.wait('visible')
    # dlg_spec = app.window(title='Monster Device Configuration Searcher')
    dlg_spec.wrapper_object()
    dlg_spec.minimize()

    devices_names = ""
    devices_count = 0
    for device in device_list:
        if devices_names == "":
            devices_names = device
        else:
            devices_names = devices_names + " " + device
        devices_count = devices_count + 1
    print(f"Total Devices: {devices_count}")

    dlg_spec['Edit0'].set_text("")
    dlg_spec['Edit3'].set_text("")
    dlg_spec.Go.click()
    dlg_spec['Edit3'].set_text(devices_names)
    dlg_spec.Go.click()

    i = 0
    print(dlg_spec['ListBox'].items())
    while not dlg_spec['ListBox'].items():
        time.sleep(3)
        if i >= 5 * devices_count:
            break
        i = i + 1
    print(f"Timer Exited After Waiting For {i * 3} seconds.!")

    i = 0
    for item in dlg_spec.ListBox.items():
        print(item)
        item.select()
        count = dlg_spec['Edit2'].line_count()
        print(f"Device: {device_list[i]} \nLines Count: {count}")
        file_exists = os.path.exists(f"{path}\\{device_list[i]}.txt")
        if file_exists:
            print(file_exists)
            os.remove(f"{path}\\{device_list[i]}.txt")
        handler = open(f"{path}\\{device_list[i]}.txt", "w")
        handler.write(dlg_spec['Edit2'].text_block())
        handler.close()
        i = i + 1


# *********** Getting Devices Backup Ends ************

# *********** Getting VIP Details of an SSL Cert Starts **********

def get_vips_of_ssl_cert(device_list, cert_list):
    """
    :param device_list:
    :param cert_list:
    """
    get_device_config(device_list)

    file_exists = exists('Table.xlsx')
    if file_exists:
        print(file_exists)
        os.remove('Table.xlsx')
    workbook = xlsxwriter.Workbook('Table.xlsx')
    worksheet = workbook.add_worksheet()
    col = 1
    row = 1
    for device in device_list:
        # worksheet = workbook.add_worksheet(device)
        with open(f'{path}\\{device}.txt', 'r') as f:
            lines = f.read().split('\n')
        # row = 1

        for cert in cert_list:
            i = 0
            j = 0
            profiles = []
            vipnames = []
            vipips = []

            for line in lines:
                if line.__contains__(f"    cert /Common/{cert}"):
                    while j > 0:
                        j = j - 1
                        backline = lines[j]
                        if backline.__contains__("ltm profile client-ssl"):
                            profile = backline.replace("ltm profile client-ssl /Common/", "").replace("{", "")
                            if profile not in profiles:
                                profiles.append(profile)
                            break
                i = i + 1
                j = i

            print(f"\n\nAvailable SSL Profiles in {device} Associated to {cert}:")
            for profile in profiles:
                print(profile)
            print("\nEND...... Finding Profiles.....\n\n")

            print("\n\nStarting...... Finding VIPs Associated to Respective Profile.....\n\n")

            i = 0
            j = 0
            table = ["", "", ""]
            innertable = []
            for profile in profiles:
                for line in lines:
                    if line.__contains__(f"       /Common/{profile}"):
                        while j > 0:
                            j = j - 1
                            if profile not in innertable:
                                innertable.append(profile)
                            backline = lines[j]
                            if backline.__contains__("ltm virtual /Common/"):
                                vipname = backline.replace("ltm virtual /Common/", "").replace("{", "")
                                vipnames.append(vipname)
                                if len(innertable) == 2:
                                    innertable.append(vipname)
                                    innertable[2] = innertable[1]
                                    innertable[1] = vipname

                                    if row == 1:
                                        # worksheet.write('A1', 'Profile')
                                        # worksheet.write('B1', 'VIP Name')
                                        # worksheet.write('C1', 'VIP IP')
                                        # worksheet.write('D1', 'Remarks')
                                        worksheet.write(row + 1, col + 0, 'Profile')
                                        worksheet.write(row + 1, col + 1, 'VIP Name')
                                        worksheet.write(row + 1, col + 2, 'VIP IP')
                                        worksheet.write(row + 1, col + 3, 'Remarks')
                                        row = 2
                                    if row > 1:
                                        # worksheet.write(f'A{row}', f'{innertable[0]}')
                                        # worksheet.write(f'B{row}', f'{innertable[1]}')
                                        # worksheet.write(f'C{row}', f'{innertable[2]}')
                                        # worksheet.write(f'D{row}', f'{device}')
                                        worksheet.write(row + 1, col + 0, f'{innertable[0]}')
                                        worksheet.write(row + 1, col + 1, f'{innertable[1]}')
                                        worksheet.write(row + 1, col + 2, f'{innertable[2]}')
                                        worksheet.write(row + 1, col + 3, f'{device}')
                                        row = row + 1

                            if backline.__contains__("    destination /Common/"):
                                destination = backline.replace("    destination /Common/", "")
                                vipips.append(destination)
                                if len(innertable) == 1:
                                    innertable.append(destination)

                            if len(innertable) == 3:
                                table.append(innertable)
                                print(innertable)
                                innertable.clear()
                                break
                    innertable.clear()
                    i = i + 1
                    j = i
                i = 0
                j = 0

    workbook.close()


# *********** Getting VIP Details of a SSL Cert Ends ************

# *********** Getting Details Of All The VIPs And Associated Stakeholders Names Starts **********

def get_all_vips_details(device_list):
    # destination_and_service = ""
    # destination = ""
    # service = ""
    # stakeholder = ""

    # Library.get_device_config(device_list)

    file_exists = exists('VIPs_Details.xlsx')
    if file_exists:
        # print(file_exists)
        os.remove('VIPs_Details.xlsx')
    workbook = xlsxwriter.Workbook('VIPs_Details.xlsx')
    # worksheet = workbook.add_worksheet()

    heading_format = workbook.add_format({
        'bold': True,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#D7E4BC'})

    normal_format = workbook.add_format({
        'bold': False,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'})

    col = 1
    # row = 1

    # worksheet.write(row + 1, col + 0, 'VIP Name', heading_format)
    # worksheet.write(row + 1, col + 1, 'VIP IP', heading_format)
    # worksheet.write(row + 1, col + 2, 'VIP Service', heading_format)
    # worksheet.write(row + 1, col + 3, 'Stakeholder Name', heading_format)
    # worksheet.write(row + 1, col + 4, 'Remarks', heading_format)
    # worksheet.write(row + 1, col + 5, 'Device', heading_format)

    row = 2

    for device in device_list:
        worksheet = workbook.add_worksheet(device)
        with open(f'{path}\\{device}.txt', 'r') as f:
            lines = f.read().split('\n')

        print(len(lines))
        i = 0
        count = 0
        while True:
            if lines[i].__contains__(f"ltm virtual /Common/"):
                count = count + 1
                vip_name = lines[i].replace("ltm virtual /Common/", "").replace("{", "").strip()
                j = i + 1
                while True:
                    if lines[j].__contains__("    destination /Common/"):
                        destination_and_service = lines[j].replace("    destination /Common/", "").split(":")
                        destination = destination_and_service[0].strip()
                        service = destination_and_service[1].strip()
                        break
                    else:
                        j = j + 1
                with open(f'{path}\\{device}.yml', 'r') as yml:
                    lines_yml = yml.read().split('\n')
                j = 0
                while True:
                    if lines_yml[j].__contains__(vip_name):
                        k = j + 1
                        while True:
                            if lines_yml[k].__contains__("stakeholders:"):
                                stakeholder = lines_yml[k].replace("stakeholders: ", "")
                                break
                            k = k + 1
                        break
                    j = j + 1

                print(f"VIP Name: {vip_name}\tVIP IP: {destination}\tService: {service}\tStakeholder: {stakeholder}")

                worksheet.write(row + 1, col + 0, vip_name, normal_format)
                worksheet.write(row + 1, col + 1, destination, normal_format)
                worksheet.write(row + 1, col + 2, service, normal_format)
                worksheet.write_number(row + 1, col + 2, int(service), normal_format)
                worksheet.write(row + 1, col + 3, stakeholder, normal_format)
                worksheet.write(row + 1, col + 4, "", normal_format)
                worksheet.write(row + 1, col + 5, device, normal_format)
                row = row + 1

            if i == len(lines) - 1:
                break

            i = i + 1
        print(f"Total Number of VIPs: {count}")
        worksheet.add_table(2, 1, row, col + 5, {'columns': [{'header': 'VIP Name'}, {'header': 'VIP IP'},
                                                             {'header': 'VIP Service'}, {'header': 'Stakeholders'},
                                                             {'header': 'Remarks'}, {'header': 'Device'}],
                                                 'style': 'Table Style Medium 4'})
        worksheet.autofit()
        col = 1
        row = 2

    workbook.close()

# *********** Getting Details Of All The VIPs And Associated Stakeholders Names Ends ************

def get_devices_from_results():

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

    i = 1
    for device in devices:
        print(f"{i}. {device}")
        i += 1
