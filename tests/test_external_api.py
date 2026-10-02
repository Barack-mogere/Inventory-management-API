from unittest.mock import patch, Mock
import requests

from app import (
    app,
    get_product_from_openfoodfacts,
    search_openfoodfacts_by_name
)

def test_get_product_from_openfoodfacts_success():
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Milk",
            "brands": "Test Brand",
            "ingredients_text": "Milk, sugar",
            "image_url": "https://example.com/milk.jpg"
        }
    }

    with patch("app.requests.get", return_value=fake_response):

        result = get_product_from_openfoodfacts("123456789")

    assert result["product_name"] == "Test Milk"
    assert result["brand"] == "Test Brand"
    assert result["barcode"] == "123456789"
    assert result["ingredients"] == "Milk, sugar"


def test_get_product_from_openfoodfacts_not_found():
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "status": 0
    }

    with patch("app.requests.get", return_value=fake_response):

        result = get_product_from_openfoodfacts("999999999")

    assert result is None


def test_get_product_from_openfoodfacts_api_error():
    fake_response = Mock()

    fake_response.status_code = 500

    with patch("app.requests.get", return_value=fake_response):

        result = get_product_from_openfoodfacts("123456789")

    assert result is None


def test_get_product_from_openfoodfacts_connection_error():
    with patch(
        "app.requests.get",
        side_effect=Exception("Connection error")
    ):

        try:
            result = get_product_from_openfoodfacts("123456789")
        except Exception:
            result = None

    assert result is None


def test_search_openfoodfacts_by_name_success():
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "products": [
            {
                "product_name": "Test Milk",
                "brands": "Test Brand",
                "code": "123456789",
                "ingredients_text": "Milk, sugar",
                "image_url": "https://example.com/milk.jpg"
            },
            {
                "product_name": "Chocolate Milk",
                "brands": "Another Brand",
                "code": "987654321",
                "ingredients_text": "Milk, cocoa, sugar",
                "image_url": "https://example.com/chocolate.jpg"
            }
        ]
    }

    with patch("app.requests.get", return_value=fake_response):

        result = search_openfoodfacts_by_name("milk")

    assert len(result) == 2
    assert result[0]["product_name"] == "Test Milk"
    assert result[1]["product_name"] == "Chocolate Milk"


def test_search_openfoodfacts_no_results():
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "products": []
    }

    with patch("app.requests.get", return_value=fake_response):

        result = search_openfoodfacts_by_name("somethingthatdoesnotexist")

    assert result == []


def test_search_openfoodfacts_api_error():
    fake_response = Mock()

    fake_response.status_code = 500

    with patch("app.requests.get", return_value=fake_response):

        result = search_openfoodfacts_by_name("milk")

    assert result is None