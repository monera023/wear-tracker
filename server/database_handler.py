import sqlite3
from typing import List, Tuple

from server.Constants import DbConstants


class DatabaseHandler:
    TABLES = []
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.setup_done = False
        self.do_setup()

    def do_setup(self):
        print(f"Setting up db..")
        if not self.setup_done:
            tables = [DbConstants.WEAR_ITEM, DbConstants.WEAR_ITEM_TRACKING]
            tables_in_query = ", ".join('?' for _ in tables)
            check_table_query = f"select name from sqlite_master where type='table' and name in ({tables_in_query})"
            print(f"Query:: {check_table_query}")
            cursor = self.conn.cursor()
            cursor.execute(check_table_query, tables)

            tables_exist = cursor.fetchall()
            if len(tables_exist) == len(tables):
                print(f"Tables present..")
            else:
                print(f"Creating tables..")
                self.create_tables()
        else:
            print(f"DB Setup already done..")

    def create_tables(self):
        print(f"In create_tables..")
        cursor = self.conn.cursor()
        create_table_wear_item_query = '''
         CREATE TABLE IF NOT EXISTS wear_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          type TEXT,
          color TEXT,
          comment TEXT,
          active INTEGER
         )
        '''
        cursor.execute(create_table_wear_item_query)
        self.conn.commit()

        create_table_wear_item_tracking_query = '''
         CREATE TABLE IF NOT EXISTS wear_item_tracking (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          item_id INTEGER,
          counter INTEGER,
          created_at datetime DEFAULT CURRENT_DATE
         )
        '''
        cursor.execute(create_table_wear_item_tracking_query)
        self.conn.commit()
        cursor.close()

    def insert_wear_items(self, items: List[Tuple]):

        print(f"In insert_wear_item")
        cursor = self.conn.cursor()
        insert_item_query = f"INSERT INTO {DbConstants.WEAR_ITEM} (name, type, color, comment, active) VALUES (?, ?, ?, ?, ?)"
        cursor.executemany(insert_item_query, items)
        self.conn.commit()
        cursor.close()

    def insert_wear_item_tracking(self, items_tracker: List[Tuple]):
        print(f"In insert_wear_item_tracking for :: {len(items_tracker)}")
        cursor = self.conn.cursor()
        insert_item_tracking_query = f"INSERT INTO {DbConstants.WEAR_ITEM_TRACKING} (item_id, counter, created_at) VALUES (?, ?, ?)"
        cursor.executemany(insert_item_tracking_query, items_tracker)
        self.conn.commit()
        cursor.close()

    def fetch_all(self, table_name):
        select_all_query = f"SELECT * FROM {table_name} limit 100"
        cursor = self.conn.cursor()
        cursor.execute(select_all_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def flush_table(self, table_name):
        cursor = self.conn.cursor()
        flush_table_query = f"DELETE FROM {table_name}"
        cursor.execute(flush_table_query)

        reset_autoincre_query = f"DELETE FROM sqlite_sequence WHERE name = '{table_name}'"
        cursor.execute(reset_autoincre_query)

        self.conn.commit()
        cursor.close()
        print("Done flush for table..")

    def drop_table(self, table_name):
        cursor = self.conn.cursor()
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_table_query)
        self.conn.commit()
        cursor.close()
        print(f"Dropped table..{table_name} from db")

    def fetch_wear_item_tracking(self, item: int):
        cursor = self.conn.cursor()
        select_query = f"SELECT * from {DbConstants.WEAR_ITEM_TRACKING} WHERE item_id = {item}"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_wear_items_with_tracking(self):
        select_query = (f"select wi.id, wi.name, wi.type, wi.active, sum(wit.counter) as count from {DbConstants.WEAR_ITEM_TRACKING} as wit right join {DbConstants.WEAR_ITEM} as wi"
                        f" on wi.id == wit.item_id group by wi.id, wi.name, wi.type, wi.active")
        cursor = self.conn.cursor()
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
