import json
import sqlite3

conn = sqlite3.connect('My-Network-Automation.db')
newegg_json = json.load(open('Device_Details.json'))

queries = []
queries.append("CREATE TABLE IF NOT EXISTS Network_Device_Inventory02 ( SlNo")
queries.append("INSERT INTO Network_Device_Inventory02 VALUES (?")

value = []
values = []

columns = []
column = []
slno = 1

print("Starting...")

for data in newegg_json:
    column = list(data.keys())
    value.append(str(slno))
    # print("Column:... \n")
    for col in column:
        if col not in columns:
            columns.append(col)
            # print(col)
            queries[0] = queries[0] + ", " + str(col)
            queries[1] = queries[1] + ", ?"
        value.append(str(dict(data).get(col)))
        values.append(list(value))
        # print(value)
        value.clear()
        slno = slno + 1


queries[0] = queries[0] + ")"
print(queries[0])
queries[1] = queries[1] + ")"
print(queries[1])

# create_query = 'create table if not exists table_newegg (model, item, price)'
# insert_query = 'insert into table_newegg values (?,?,?)'
c = conn.cursor()
c.execute(str(queries[0]))
# print("values:...\n",values)
c.executemany(str(queries[1]), values)
conn.commit()
c.close()

