import kubernetes
import sqlite3  # noqa: F401
from submod.dbman import dbman


class Kubctl:
    def __init__(self, config_file=None):
        kubernetes.config.load_incluster_config() #TODO: add more config options

        self.v1 = kubernetes.client.CoreV1Api()
    

class Internal():
    def __init__(self):
        # pod filesystem init
        with dbman() as (conn, cursor):
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pod_filesystem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pod_name TEXT NOT NULL,
                file_path TEXT NOT NULL UNIQUE,
                content TEXT,
                type TEXT NOT NULL
            );
            """)
    def link(pod_name, file_path, type="folder",content="na"):
        fullpath = ""
        for i in file_path.split("/"):
            fullpath += i 
            try:
                with dbman() as (conn, cursor):
                    cursor.execute("""
                    INSERT INTO pod_filesystem (pod_name, file_path, content, type)
                    VALUES (?, ?, ?, ?)
                    """, (i, fullpath, "na", type))
            except Exception as e:
                a = None
            fullpath += "/"
    def listdir(path):
        with dbman() as (conn, cursor):
            cursor.execute("""
            SELECT * FROM pod_filesystem WHERE file_path LIKE ? AND file_path NOT LIKE ? || '/%/%';
            """, (path + '%',path + "%",))
            out = cursor.fetchall()
            out = [{"path":f[2],"name":f[1]} for f in out]
            try:
                out.remove(path)
            except:  # noqa: E722
                pass
        return out

Internal()  # initialize internal db structure

    
            

