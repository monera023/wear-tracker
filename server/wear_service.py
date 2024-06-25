from typing import List

from server.Constants import WearItem, DbConstants, WearItemTrackingEntry
from server.database_handler import DatabaseHandler
from server.utils import convert_bool, convert_to_wear_item, convert_to_wear_item_tracking, \
    convert_to_wear_item_tracking_sum


class WearService:
    def __init__(self, db_name):
        self.database_conn = DatabaseHandler(db_name)

    def add_wear_items(self, items: List[WearItem]):
        insert_data = [(item.name, item.type.name, item.color, item.comment, convert_bool(item.active)) for item in items]
        print(f"IN {__name__}.add_wear_item {insert_data}")
        self.database_conn.insert_wear_items(insert_data)

    def fetch_wear_items(self):
        output = self.database_conn.fetch_all(DbConstants.WEAR_ITEM)
        formatted_output = convert_to_wear_item(output)
        return formatted_output

    def add_wear_items_tracking(self, items: List[WearItemTrackingEntry]):
        insert_data = [(item.item_id, item.counter, item.date) for item in items]
        print(f"In {__name__}.add_wear_items_tracking for {insert_data}")
        self.database_conn.insert_wear_item_tracking(insert_data)

    def fetch_wear_item_tracking(self, item: int):
        output = self.database_conn.fetch_wear_item_tracking(item)
        formatted_output = convert_to_wear_item_tracking(output)
        return formatted_output

    def fetch_wear_items_with_tracking(self):
        output = self.database_conn.fetch_wear_items_with_tracking()
        formatted_output = convert_to_wear_item_tracking_sum(output)
        return formatted_output

    def search_wear_items(self, query_param_dict):
        output = self.database_conn.search_wear_items(query_param_dict)
        formatted_output = convert_to_wear_item(output)
        return formatted_output



