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
                content TEXT NOT NULL,
                type TEXT NOT NULL
            );
            """)
    def link(pod_name, file_path, type="folder",content="na"):
        fullpath = ""
        for i in file_path.split("/"):
            fullpath += i 
            with dbman() as (conn, cursor):
                cursor.execute("""
                INSERT INTO pod_filesystem (pod_name, file_path, content, type)
                VALUES (?, ?, ?, ?)
                """, (i, fullpath, "na", type))
            fullpath += "/"


Internal()  # initialize internal db structure

    
            

