import xlsxwriter
import os

from os.path import exists

file_exists = exists('Table.xlsx')
if file_exists == True :
    print(file_exists)
    os.remove('Table.xlsx')
workbook = xlsxwriter.Workbook('Table.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Profile')
worksheet.write('B1', 'VIP Name')
worksheet.write('C1', 'VIP IP')
worksheet.write('D1', 'Remarks')
row = 2


print("\n\nStarting............\n\n")
with open('FRA-BIGIP-FDSG-DMZ-2.txt', 'r') as f:
#with open('NJ-BIGIP-FDSG-DMZ-2.txt', 'r') as f:
    lines = f.read().split('\n')

count = 0
i = 0
j = 0
k = 0
l = 0
profiles = []
vips = []
vipnames = []
vipips = []

for line in lines:
    #if line.__contains__("    cert /Common/wildcard.ppe.factsetdigitalsolutions.com_2023") == True :
    if line.__contains__("    cert /Common/investments.uat.targobank.de_2023") == True:
    #if line.__contains__("    cert /Common/WILDCARD.PPE.FACTSETDIGITALSOLUTIONS.COM_2023") == True:
        while j > 0 :
            j = j - 1
            backline = lines[j]
            if backline.__contains__("ltm profile client-ssl") == True :
                backline = backline.replace("ltm profile client-ssl /Common/", "").replace("{", "")
                if backline not in profiles :
                    profiles.append(backline)
                # j = 0
                break
    i = i + 1
    j = i
# print(profiles)
for profile in profiles:
    print(profile)
print("\n\nEND...... Finding Profiles.....\n\n")

print("Starting...... Finding VIPs Associated to Respective Profile.....\n\n")

i = 0
j = 0
table = ["","",""]
innertable = []

for profile in profiles :
    # print(profile)
    # print("\nVIPs Associated to Profile: " + f"{profile}\n\n")
    for line in lines :
        if line.__contains__(f"       /Common/{profile}") == True :
            while j > 0:
                j = j - 1
                if profile not in innertable :
                    innertable.append(profile)
                backline = lines[j]
                if backline.__contains__("ltm virtual /Common/") == True :
                    backline = backline.replace("ltm virtual /Common/","").replace("{","")
                    # print(f"VIP Name: {backline}")
                    # if backline not in vipnames :
                    vipnames.append(backline)
                    #print(len(innertable))
                    if len(innertable) == 2:
                        innertable.append(backline)
                        innertable[2] = innertable[1]
                        innertable[1] = backline

                        worksheet.write(f'A{row}', f'{innertable[0]}')
                        worksheet.write(f'B{row}', f'{innertable[1]}')
                        worksheet.write(f'C{row}', f'{innertable[2]}')
                        row = row + 1

                if backline.__contains__("    destination /Common/") == True :
                    backline = backline.replace("    destination /Common/","")
                    # print(f"VIP IP: {backline}")
                    vipips.append(backline)
                    #print(len(innertable))
                    if len(innertable) == 1 :
                        innertable.append(backline)
                    # break

                #print(len(innertable))
                if len(innertable) == 3 :
                    table.append(innertable)
                    print(innertable)
                    innertable.clear()
                    break
        innertable.clear()
        i = i + 1
        j = i
        # print("i value: ")
        # print(i)
    i = 0
    j = 0

workbook.close()


