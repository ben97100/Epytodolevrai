import os
import csv
import pytest
from crud import get_entry, add_entry, update_entry, delete_entry, ResourceNotFoundError
from utils import get_csv_path

RESOURCE = "items"
CSV_PATH = get_csv_path(RESOURCE)

@pytest.fixture(autouse=True)
def setup_csv():
    # Crée un fichier CSV temporaire de test avant chaque test
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "value"])
        writer.writeheader()
        writer.writerows([
            {"id": "1", "name": "ItemOne", "value": "10"},
            {"id": "2", "name": "ItemTwo", "value": "20"}
        ])
    yield
    # Nettoyage après chaque test si nécessaire
    # os.remove(CSV_PATH)

def test_get_existing_entry():
    entry = get_entry(RESOURCE, "1")
    assert entry["name"] == "ItemOne"
    assert entry["value"] == "10"

def test_get_non_existing_entry():
    with pytest.raises(ResourceNotFoundError):
        get_entry(RESOURCE, "999")

def test_add_entry():
    result = add_entry(RESOURCE, ["NewItem", "50"])
    assert result["message"] == "Added items 3"
    entry = get_entry(RESOURCE, "3")
    assert entry["name"] == "NewItem"
    assert entry["value"] == "50"

def test_update_entry():
    result = update_entry(RESOURCE, "2", ["UpdatedName", "999"])
    assert result["message"] == "Updated items 2"
    entry = get_entry(RESOURCE, "2")
    assert entry["name"] == "UpdatedName"
    assert entry["value"] == "999"

def test_update_non_existing_entry():
    with pytest.raises(ResourceNotFoundError):
        update_entry(RESOURCE, "999", ["X", "Y"])

def test_delete_entry():
    result = delete_entry(RESOURCE, "1")
    assert result["message"] == "Deleted items 1"
    with pytest.raises(ResourceNotFoundError):
        get_entry(RESOURCE, "1")

def test_delete_non_existing_entry():
    with pytest.raises(ResourceNotFoundError):
        delete_entry(RESOURCE, "999")
