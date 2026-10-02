import pytest

from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()

    inventory.extend([
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "barcode": "123456789",
            "price": 450,
            "stock": 20,
            "ingredients": "Filtered water, almonds, cane sugar"
        },
        {
            "id": 2,
            "product_name": "Whole Milk",
            "brand": "Brookside",
            "barcode": "987654321",
            "price": 150,
            "stock": 35,
            "ingredients": "Fresh whole milk"
        }
    ])


def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management API is running!"


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["product_name"] == "Organic Almond Milk"


def test_get_single_inventory_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_inventory_item_not_found(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"


def test_add_inventory_item(client):
    new_product = {
        "product_name": "Coca Cola",
        "brand": "Coca Cola",
        "barcode": "5449000000996",
        "price": 100,
        "stock": 25,
        "ingredients": "Carbonated water, sugar"
    }

    response = client.post(
        "/inventory",
        json=new_product
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 3
    assert data["product_name"] == "Coca Cola"
    assert data["brand"] == "Coca Cola"


def test_add_inventory_item_missing_fields(client):
    incomplete_product = {
        "product_name": "Coca Cola",
        "brand": "Coca Cola"
    }

    response = client.post(
        "/inventory",
        json=incomplete_product
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "Missing required fields" in data["error"]


def test_update_inventory_item(client):
    update_data = {
        "price": 200,
        "stock": 50
    }

    response = client.patch(
        "/inventory/1",
        json=update_data
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 200
    assert data["stock"] == 50


def test_update_inventory_item_not_found(client):
    update_data = {
        "price": 200
    }

    response = client.patch(
        "/inventory/999",
        json=update_data
    )

    assert response.status_code == 404


def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Item deleted successfully"

    assert len(inventory) == 1


def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"