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

with open('ped.csv') as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        rows.append(line)


for row in rows:
    line = "".join(row).split(';')
    print(line)
    cur.execute(f'''INSERT INTO Pedagogy (university,code,url,type)
                    VALUES ('{line[0].upper()}','{line[1]}','{line[2]}','.pdf')''')
    

conn.commit()
cur.close()  
conn.close()
