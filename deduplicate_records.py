def deduplicate_records(records: list[dict]) -> list[dict]:

    latest_records = {}

    for record in records:

        record_id = record['id']

        # First time encountering this ID
        if record_id not in latest_records:
            latest_records[record_id] = record.copy()

        # A newer record for an existing ID    
        elif record['updated_at'] > latest_records[record_id]['updated_at']:
            latest_records[record_id] = record.copy()
    
    return list(latest_records.values())

records = [
    {"id":1, "name":"Alice", "updated_at":10},
    {"id":2, "name":"Bob", "updated_at":15},
    {"id":1, "name":"Alice Smith", "updated_at":20},
    {"id":3, "name":"Charlie", "updated_at":12},
    {"id":2, "name":"Robert", "updated_at":18}
]


print(deduplicate_records(records))
