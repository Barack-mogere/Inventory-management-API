from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# Temporary inventory database
inventory = [
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
]


# Generate the next available ID
def get_next_id():
    if not inventory:
        return 1

    return max(item["id"] for item in inventory) + 1


# Home route
@app.route("/")
def home():
    return {"message": "Inventory Management API is running!"}


# Get all inventory items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


# Get one inventory item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


# Add a new inventory item
@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "product_name",
        "brand",
        "barcode",
        "price",
        "stock",
        "ingredients"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    new_item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brand": data["brand"],
        "barcode": data["barcode"],
        "price": data["price"],
        "stock": data["stock"],
        "ingredients": data["ingredients"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# Update an inventory item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    for item in inventory:
        if item["id"] == item_id:

            if "product_name" in data:
                item["product_name"] = data["product_name"]

            if "brand" in data:
                item["brand"] = data["brand"]

            if "barcode" in data:
                item["barcode"] = data["barcode"]

            if "price" in data:
                item["price"] = data["price"]

            if "stock" in data:
                item["stock"] = data["stock"]

            if "ingredients" in data:
                item["ingredients"] = data["ingredients"]

            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


# Delete an inventory item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Item deleted successfully"
            })

    return jsonify({"error": "Item not found"}), 404


# Search OpenFoodFacts by barcode
def get_product_from_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "barcode": barcode,
            "ingredients": product.get("ingredients_text"),
            "image_url": product.get("image_url")
        }

    except requests.RequestException:
        return None


# Find a product using OpenFoodFacts barcode
@app.route("/products/<barcode>", methods=["GET"])
def find_product(barcode):
    product = get_product_from_openfoodfacts(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found or OpenFoodFacts is unavailable"
        }), 404

    return jsonify(product)


# Search OpenFoodFacts by product name
def search_openfoodfacts_by_name(name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 10
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        products = []

        for product in data.get("products", []):
            products.append({
                "product_name": product.get("product_name"),
                "brand": product.get("brands"),
                "barcode": product.get("code"),
                "ingredients": product.get("ingredients_text"),
                "image_url": product.get("image_url")
            })

        return products

    except requests.RequestException:
        return None


# Find products using OpenFoodFacts name search
@app.route("/products/search", methods=["GET"])
def search_products():
    name = request.args.get("name")

    if not name:
        return jsonify({
            "error": "Please provide a product name"
        }), 400

    products = search_openfoodfacts_by_name(name)

    if products is None:
        return jsonify({
            "error": "OpenFoodFacts is unavailable"
        }), 503

    if len(products) == 0:
        return jsonify({
            "message": "No products found"
        }), 404

    return jsonify(products)


# Add a product from OpenFoodFacts to inventory
@app.route("/inventory/from-api/<barcode>", methods=["POST"])
def add_product_from_api(barcode):
    product = get_product_from_openfoodfacts(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found on OpenFoodFacts"
        }), 404

    data = request.get_json() or {}

    new_item = {
        "id": get_next_id(),
        "product_name": product["product_name"],
        "brand": product["brand"],
        "barcode": product["barcode"],
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
        "ingredients": product["ingredients"],
        "image_url": product["image_url"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)