import os


def get_csv_path(resource):
    return os.path.join("data", f"{resource}s.csv")


def get_next_id(rows):
    if not rows:
        return 0
    return max(int(row["id"]) for row in rows) + 1
