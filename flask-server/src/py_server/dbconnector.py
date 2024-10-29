import sqlite3
import queue
import threading
import time


class DBConnector:
    def __init__(self, database: str, log: bool):
        self.database = database
        self.query_queue = queue.Queue()
        self.db_connection = None
        self.log = log

    def run_query(self, query):
        if self.log:
            print(f"SERVER_QUERY_LOG#Q:{query}")
        db_connection = sqlite3.connect(self.database, check_same_thread=False)
        # Initialize DB connection and cursor
        try:
            cur = db_connection.cursor()
            res = cur.execute(query).fetchall()
            db_connection.commit()
        finally:
            db_connection.close()
        if self.log:
            print(f"SERVER_QUERY_LOG#R:{res}")
        return res

    def work_on_queue(self):
        while True:
            if not self.query_queue.empty():
                query = self.query_queue.get()
                print(query)

    def queue_query(self, query):
        pass

    def start_workers(self, num_workers=3):
        thread = threading.Thread(target=self.work_on_queue)
        thread.start()
