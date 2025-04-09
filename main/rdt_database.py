import psycopg2
from urllib.parse import urlparse
import rdt_db_viewer as dv
import sys

def dataToDict(db_url) -> dict:
    spec_names = ['IT','Jurisprudence','Pedagogy','Geology','Medicine']
    url = urlparse(db_url)
    
    conn = psycopg2.connect(
        host=url.hostname,
        port=url.port,
        database=url.path[1:], 
        user=url.username,
        password=url.password
    )
    cur= conn.cursor()

    data_dict = dict()
    for spec_name in spec_names:
        cur.execute(f'''SELECT university, url FROM {spec_name}''')
        links = list()
        for uni_url in cur.fetchall():
            links.append([uni_url[0],uni_url[1]])
        data_dict[spec_name]=links



    conn.commit()
    cur.close()  
    conn.close()

    return data_dict

    
def view(db_url):
    app = dv.QApplication(sys.argv)
    window = dv.DatabaseViewer(db_url)  
    window.show()
    sys.exit(app.exec_())
