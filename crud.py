import csv
import sys
from utils import get_csv_path, get_next_id

class ResourceNotFoundError(Exception):
    pass


def get_entry(resource, id):
    path = get_csv_path(resource)
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == id:
                return row
    raise ResourceNotFoundError(f"{resource} {id} not found")


def delete_entry(resource, id):
    path = get_csv_path(resource)
    rows = []
    found = False
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        for row in rows:
            if row['id'] == id:
                found = True
                rows.remove(row)
    if not found:
        raise ResourceNotFoundError(f"{resource} {id} not found")
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return f"Deleted {resource} {id}"


def add_entry(resource, fields):
    path = get_csv_path(resource)
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        rows = list(reader)
    if len(fields) != len(headers) - 1:
        raise ValueError("Invalid number of fields")
    new_id = get_next_id(rows)
    new_entry = {'id': str(new_id)}
    for i, key in enumerate(headers[1:]):
        new_entry[key] = fields[i]
    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writerow(new_entry)
    return new_entry


def update_entry(resource, id, fields):
    path = get_csv_path(resource)
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        rows = list(reader)
    updated = False
    for row in rows:
        if row['id'] == id:
            for i, key in enumerate(headers[1:]):
                row[key] = fields[i]
            updated = True
    if not updated:
        raise ResourceNotFoundError(f"{resource} {id} not found")
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return f"Updated {resource} {id}"
