import requests

BASE_URL = "http://localhost:8081"
RESOURCE = "items"
TEST_ID = "3"

create_data = {"name": "TestItem", "value": "42"}
update_data = {"name": "UpdatedItem", "value": "100"}

def test_post():
    response = requests.post(f"{BASE_URL}/{RESOURCE}", data=create_data)
    assert response.status_code == 201, f"POST failed: {response.text}"
    print("✅ POST passed")

def test_get():
    response = requests.get(f"{BASE_URL}/{RESOURCE}/{TEST_ID}")
    assert response.status_code == 200, f"GET failed: {response.text}"
    print("✅ GET passed")

def test_put():
    response = requests.put(f"{BASE_URL}/{RESOURCE}/{TEST_ID}", data=update_data)
    assert response.status_code == 200, f"PUT failed: {response.text}"
    print("✅ PUT passed")

def test_delete():
    response = requests.delete(f"{BASE_URL}/{RESOURCE}/{TEST_ID}")
    assert response.status_code == 200, f"DELETE failed: {response.text}"
    print("✅ DELETE passed")

if __name__ == "__main__":
    print("🔁 Running E2E tests...")
    test_post()
    test_get()
    test_put()
    test_delete()
    print("🎉 All tests passed.")
