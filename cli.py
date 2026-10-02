import requests


BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory")

        if response.status_code == 200:
            products = response.json()

            print("\n===== INVENTORY =====")

            for product in products:
                print(f"""
ID: {product["id"]}
Product: {product["product_name"]}
Brand: {product["brand"]}
Barcode: {product["barcode"]}
Price: Ksh {product["price"]}
Stock: {product["stock"]}
Ingredients: {product["ingredients"]}
-------------------------
""")
        else:
            print("Error getting inventory.")

    except requests.RequestException:
        print("Unable to connect to the API.")


def view_product():
    item_id = input("Enter product ID: ")

    try:
        response = requests.get(
            f"{BASE_URL}/inventory/{item_id}"
        )

        if response.status_code == 200:
            product = response.json()

            print("\n===== PRODUCT =====")
            print(f"ID: {product['id']}")
            print(f"Product: {product['product_name']}")
            print(f"Brand: {product['brand']}")
            print(f"Barcode: {product['barcode']}")
            print(f"Price: Ksh {product['price']}")
            print(f"Stock: {product['stock']}")
            print(f"Ingredients: {product['ingredients']}")

        else:
            print("Product not found.")

    except requests.RequestException:
        print("Unable to connect to the API.")


def add_product():
    print("\n===== ADD PRODUCT =====")

    product_name = input("Product name: ")
    brand = input("Brand: ")
    barcode = input("Barcode: ")
    ingredients = input("Ingredients: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Price must be a number and stock must be a whole number.")
        return

    product = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "price": price,
        "stock": stock,
        "ingredients": ingredients
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=product
        )

        if response.status_code == 201:
            print("\nProduct added successfully!")
            print(response.json())
        else:
            print("Failed to add product.")

    except requests.RequestException:
        print("Unable to connect to the API.")


def update_product():
    print("\n===== UPDATE PRODUCT =====")

    item_id = input("Enter product ID: ")

    print("\nLeave a field empty if you don't want to change it.")

    price = input("New price: ")
    stock = input("New stock: ")

    update_data = {}

    if price:
        try:
            update_data["price"] = float(price)
        except ValueError:
            print("Price must be a number.")
            return

    if stock:
        try:
            update_data["stock"] = int(stock)
        except ValueError:
            print("Stock must be a whole number.")
            return

    if not update_data:
        print("No changes were entered.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=update_data
        )

        if response.status_code == 200:
            print("\nProduct updated successfully!")
            print(response.json())
        else:
            print("Product not found.")

    except requests.RequestException:
        print("Unable to connect to the API.")


def delete_product():
    print("\n===== DELETE PRODUCT =====")

    item_id = input("Enter product ID: ")

    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{item_id}"
        )

        if response.status_code == 200:
            print("\nProduct deleted successfully!")
        else:
            print("Product not found.")

    except requests.RequestException:
        print("Unable to connect to the API.")


def search_openfoodfacts():
    print("\n===== OPENFOODFACTS SEARCH =====")

    name = input("Enter product name: ")

    try:
        response = requests.get(
            f"{BASE_URL}/products/search",
            params={"name": name}
        )

        if response.status_code == 200:
            products = response.json()

            print("\n===== SEARCH RESULTS =====")

            for product in products:
                print(f"""
Product: {product["product_name"]}
Brand: {product["brand"]}
Barcode: {product["barcode"]}
Ingredients: {product["ingredients"]}
-------------------------
""")

        elif response.status_code == 404:
            print("No products found.")

        else:
            print("OpenFoodFacts is unavailable.")

    except requests.RequestException:
        print("Unable to connect to the API.")


def main():
    while True:

        print("""
=================================
     INVENTORY MANAGEMENT
=================================

1. View all inventory
2. View one product
3. Add product
4. Update product
5. Delete product
6. Search OpenFoodFacts
7. Exit
""")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_product()

        elif choice == "3":
            add_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            search_openfoodfacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()