from server.Constants import WearItem, WearType, WearItemTrackingEntry, WearItemTrackingSumEntity


def convert_bool(value):
    return 1 if value else 0


def convert_to_wear_item(items):
    resp = []
    for item in items:
        print(f"HERE {item}")
        resp.append(WearItem(id=item[0], name=item[1], type=WearType[item[2]], color=item[3], comment=item[4], active=bool(item[4])))
    return resp

def convert_to_wear_item_tracking(items):
    resp = []
    for item in items:
        print(f"IN convert_to_wear_item_tracking:: {item}")
        resp.append(WearItemTrackingEntry(item_id=item[1], counter=item[2], date=item[3]))
    return resp

def convert_to_wear_item_tracking_sum(items):
    resp = []
    for item in items:
        print(f"In convert_to_wear_item_tracking_sum:: {item}")
        resp.append(WearItemTrackingSumEntity(item_id=item[0], name=item[1], type=item[2], active=bool(item[3]), total=item[4]))
    return resp