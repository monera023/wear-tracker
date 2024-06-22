from server.Constants import DbConstants
from server.database_handler import DatabaseHandler


class OperationsManager:
    def __init__(self):
        self.database = DatabaseHandler("wear-tracker.db")

    def fetch_data_for_table(self, table_name):
        output = self.database.fetch_all(table_name)
        for row in output:
            print(row)

    def drop_tables(self, table_name):
        self.database.drop_table(table_name)


if __name__ == "__main__":
    ops_manager = OperationsManager()
    # ops_manager.fetch_data_for_table(DbConstants.WEAR_ITEM_TRACKING)
    data = ops_manager.database.fetch_wear_items_with_tracking()
    for row in data:
        print(row)
