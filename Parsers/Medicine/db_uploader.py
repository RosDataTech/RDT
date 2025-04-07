import psycopg2
from urllib.parse import urlparse

url = urlparse('db_url')

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:], 
    user=url.username,
    password=url.password
)
cur= conn.cursor()

rows = []

with open('medicine.csv') as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        rows.append(line)

database_lst = []

for row in rows[:rows.index([';;;'])]:
    lst_row = [i for i in "".join(row).split(';')]
    if lst_row[0] == 'ROSTGMU' or lst_row[0]=='ROSUNIMED': continue
    lst_row[1]=lst_row[1][:8]
    database_lst.append(lst_row)
database_lst[0][0]='SECH'


for row in database_lst:
    cur.execute(f'''INSERT INTO Medicine (university,code,url,type)
                    VALUES ('{row[0]}','{row[1]}','{row[2]}','{row[3]}')''')
    print(row)
    
conn.commit()
cur.close()  
conn.close()
