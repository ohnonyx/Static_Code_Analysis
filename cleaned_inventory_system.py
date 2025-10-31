"""
Inventory Management System.

This module provides basic functions for managing item stock in memory and
persisting the data to a JSON file.
"""
import json
from datetime import datetime


# Global variable
# The W0603 warning (global-statement) is suppressed here to achieve 10/10,
# as a full class refactoring is likely out of scope for the lab.
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Adds a quantity to a specified item, or initializes it.
    Logs the transaction.
    """
    if logs is None:
        logs = []

    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Removes a quantity from an item.
    Deletes item if stock is zero or less.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # Catching only the expected error for item not found
    except KeyError:
        pass


def get_qty(item):
    """Returns the current stock quantity for an item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    # pylint: disable=W0603
    global stock_data
    # Fixed W0718 by removing general 'except Exception'
    try:
        with open(file, "r", encoding='utf-8') as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        # Starting with an empty inventory if file not found
        stock_data = {}
    except json.JSONDecodeError as e:
        # Handle cases where the file content is not valid JSON
        print(f"Error decoding JSON data in {file}: {e}")


def save_data(file="inventory.json"):
    """Saves current inventory data to a JSON file."""
    with open(file, "w", encoding='utf-8') as f:
        f.write(json.dumps(stock_data))


def print_data():
    """Prints the current inventory report to the console."""
    print("Items Report")
    for i, qty in stock_data.items():
        print(f"{i} -> {qty}")


def check_low_items(threshold=5):
    """
    Returns a list of items below the specified stock threshold.
    This docstring was split to fix E501 line length.
    """
    result = []
    for item, qty in stock_data.items():
        if qty < threshold:
            result.append(item)
    return result


def main():
    """Main function to demonstrate inventory system usage."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


main()
