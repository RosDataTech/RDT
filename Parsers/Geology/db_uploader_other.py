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
cur = conn.cursor()
cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                                VALUES ('MISIS','21.05.04','https://drive.google.com/file/d/1ML9V5rVa8w74Z3LHNetdqdK-_U9o8BnZ/view?usp=drive_link','.pdf')''')
cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                                VALUES ('RUDN','21.05.02','https://drive.google.com/file/d/1WVLJmO_z_Ae1BSdnsPziNGtnhOQ40icn/view?usp=drive_link','.pdf')''')
cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                                VALUES ('RUDN','21.05.02','https://drive.google.com/file/d/1QG8Pytukj4fhlYcMesbLv-U7Tvj_IjcV/view?usp=drive_link','.pdf')''')
cur.execute(f'''INSERT INTO Geology (university,code,url,type)
                                                VALUES ('MIREA','05.03.03','https://drive.google.com/file/d/1Q3WzpLjXi_Lu0C4DXDqNIuZ7G7WTFQmI/view?usp=drive_link','.pdf')''')
conn.commit()
cur.close()
conn.close()
