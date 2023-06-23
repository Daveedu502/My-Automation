import Library
import os
import time
import xlsxwriter

from pywinauto.application import Application
from os.path import exists

device_list = ["NJ-BIGIP-DMZ-2"]
path = "C:\\Users\\dnarala\\PycharmProjects\\My-Network-Automation\\Devices_Backup"

destination_and_service = ""
destination = ""
service = ""
stakeholder = ""

# Library.get_device_config(device_list)

file_exists = exists('VIPs_Details.xlsx')
if file_exists:
    # print(file_exists)
    os.remove('VIPs_Details.xlsx')
workbook = xlsxwriter.Workbook('VIPs_Details.xlsx')
worksheet = workbook.add_worksheet()

heading_format = workbook.add_format({
    'bold':     True,
    'border':   2,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#D7E4BC'})

normal_format = workbook.add_format({
    'bold':     False,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter'})

col = 1
row = 1

# worksheet.write(row + 1, col + 0, 'VIP Name', heading_format)
# worksheet.write(row + 1, col + 1, 'VIP IP', heading_format)
# worksheet.write(row + 1, col + 2, 'VIP Service', heading_format)
# worksheet.write(row + 1, col + 3, 'Stakeholder Name', heading_format)
# worksheet.write(row + 1, col + 4, 'Remarks', heading_format)
# worksheet.write(row + 1, col + 5, 'Device', heading_format)
row = 2

for device in device_list:
    # worksheet = workbook.add_worksheet(device)
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
                    k = j+1
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
    worksheet.add_table(2, 1, row, col + 5, {'columns': [{'header': 'VIP Name'},{'header': 'VIP IP'},{'header': 'VIP Service'},{'header': 'Stakeholders'},{'header': 'Remarks'},{'header': 'Device'}],'style': 'Table Style Medium 4'})
    worksheet.autofit()

workbook.close()
