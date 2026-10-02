# Inventory Management System API

## Overview

This project is a Python REST API built with Flask for managing inventory items. The system allows users to create, view, update, and delete inventory products through API endpoints.

The application also connects to the OpenFoodFacts API to retrieve product information using a barcode or product name.

A command-line interface (CLI) is included so that employees can interact with the inventory system without manually entering API URLs.

## Features

- View all inventory items
- View a single inventory item
- Add a new inventory item
- Update an existing inventory item
- Delete an inventory item
- Search OpenFoodFacts by barcode
- Search OpenFoodFacts by product name
- Add OpenFoodFacts products to the local inventory
- CLI interface for interacting with the API
- Input validation
- Error handling
- Automated tests using pytest
- Mocking external API requests using unittest.mock

## Technologies Used

- Python
- Flask
- Requests
- Pytest
- unittest.mock
- OpenFoodFacts API

## Project Structure

```text
inventory-management-api/
│
├── app.py
├── cli.py
├── README.md
├── requirements.txt
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_cli.py
    └── test_external_api.py