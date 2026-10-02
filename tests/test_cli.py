from unittest.mock import patch, Mock

import cli


def test_view_inventory(capsys):
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Milk",
            "brand": "Brookside",
            "barcode": "123456",
            "price": 150,
            "stock": 20,
            "ingredients": "Fresh milk"
        }
    ]

    with patch("cli.requests.get", return_value=fake_response):
        cli.view_inventory()

    captured = capsys.readouterr()

    assert "Milk" in captured.out
    assert "Brookside" in captured.out
    assert "150" in captured.out


def test_view_product(capsys):
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "barcode": "123456",
        "price": 150,
        "stock": 20,
        "ingredients": "Fresh milk"
    }

    with patch("cli.requests.get", return_value=fake_response):
        with patch("builtins.input", return_value="1"):
            cli.view_product()

    captured = capsys.readouterr()

    assert "Milk" in captured.out
    assert "Brookside" in captured.out


def test_add_product(capsys):
    fake_response = Mock()

    fake_response.status_code = 201

    fake_response.json.return_value = {
        "id": 3,
        "product_name": "Coca Cola",
        "brand": "Coca Cola",
        "barcode": "123456789",
        "price": 100,
        "stock": 20,
        "ingredients": "Carbonated water, sugar"
    }

    user_inputs = [
        "Coca Cola",
        "Coca Cola",
        "123456789",
        "Carbonated water, sugar",
        "100",
        "20"
    ]

    with patch("cli.requests.post", return_value=fake_response):

        with patch(
            "builtins.input",
            side_effect=user_inputs
        ):

            cli.add_product()

    captured = capsys.readouterr()

    assert "Product added successfully!" in captured.out


def test_add_product_invalid_price(capsys):
    user_inputs = [
        "Coca Cola",
        "Coca Cola",
        "123456789",
        "Carbonated water, sugar",
        "invalid",
        "20"
    ]

    with patch(
        "builtins.input",
        side_effect=user_inputs
    ):
        cli.add_product()

    captured = capsys.readouterr()

    assert "Price must be a number" in captured.out


def test_update_product(capsys):
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "barcode": "123456",
        "price": 200,
        "stock": 50,
        "ingredients": "Fresh milk"
    }

    user_inputs = [
        "1",
        "200",
        "50"
    ]

    with patch("cli.requests.patch", return_value=fake_response):

        with patch(
            "builtins.input",
            side_effect=user_inputs
        ):

            cli.update_product()

    captured = capsys.readouterr()

    assert "Product updated successfully!" in captured.out


def test_delete_product(capsys):
    fake_response = Mock()

    fake_response.status_code = 200

    user_inputs = ["1"]

    with patch("cli.requests.delete", return_value=fake_response):

        with patch(
            "builtins.input",
            side_effect=user_inputs
        ):

            cli.delete_product()

    captured = capsys.readouterr()

    assert "Product deleted successfully!" in captured.out


def test_search_openfoodfacts(capsys):
    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = [
        {
            "product_name": "Milk",
            "brand": "Brookside",
            "barcode": "123456",
            "ingredients": "Fresh milk"
        }
    ]

    with patch("cli.requests.get", return_value=fake_response):

        with patch(
            "builtins.input",
            return_value="milk"
        ):

            cli.search_openfoodfacts()

    captured = capsys.readouterr()

    assert "Milk" in captured.out
    assert "Brookside" in captured.out