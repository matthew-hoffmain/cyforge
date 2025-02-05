import sqlite3
import queue
import threading
import time
from typing import List, Any


class DBConnector:
    def __init__(self,
                 database: str,
                 log: bool
                 ) -> None:
        self.database = database
        self.query_queue = queue.Queue()
        self.db_connection = None
        self.log = log

    def run_query(self,
                  query: str
                  ) -> list[Any]:
        if self.log:
            print(f"SERVER_QUERY_LOG#Q:{query}")

        # Use connection as a context manager, attempt query execution and close connection upon exiting context
        db_connection = sqlite3.connect(self.database, check_same_thread=False)
        try:
            # Commit called automatically upon exiting context
            with db_connection:
                res = db_connection.execute(query).fetchall()
        # Rollback called upon exception
        except sqlite3.IntegrityError:
            print(f"SERVER_QUERY_LOG#E:Exception triggered, rolling back previous query:{query}")
            raise

        if self.log:
            print(f"SERVER_QUERY_LOG#R:{res}")
        return res
