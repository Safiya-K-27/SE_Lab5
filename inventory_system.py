"""
Inventory Management System.

A simple system to manage item stock levels with logging capabilities.
"""
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variable (consider refactoring to a class in production)
STOCK_DATA: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0,
             logs: Optional[List[str]] = None) -> None:
    """
    Add items to the inventory.

    Args:
        item (str): The name of the item to add.
        qty (int): The quantity to add (must be non-negative).
        logs (Optional[List[str]]): Optional list to store log messages.
    """
    if logs is None:
        logs = []

    if not item or not isinstance(item, str):
        logging.warning("Invalid item name provided")
        return

    if not isinstance(qty, int) or qty < 0:
        logging.warning("Invalid quantity: %s. Must be non-negative", qty)
        return

    STOCK_DATA[item] = STOCK_DATA.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info(log_message)


def remove_item(item: str, qty: int) -> bool:
    """
    Remove items from the inventory.

    Args:
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        if item not in STOCK_DATA:
            logging.warning("Item '%s' not found in inventory", item)
            return False

        if not isinstance(qty, int) or qty < 0:
            logging.warning("Invalid quantity: %s", qty)
            return False

        STOCK_DATA[item] -= qty
        if STOCK_DATA[item] <= 0:
            del STOCK_DATA[item]
            logging.info("Item '%s' removed (quantity depleted)", item)
        else:
            logging.info("Removed %s of '%s'. Remaining: %s",
                        qty, item, STOCK_DATA[item])
        return True
    except KeyError as key_error:
        logging.error("Error accessing item '%s': %s", item, key_error)
        return False


def get_qty(item: str) -> int:
    """
    Get the quantity of an item in inventory.

    Args:
        item (str): The name of the item.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    if item not in STOCK_DATA:
        logging.warning("Item '%s' not found in inventory", item)
        return 0
    return STOCK_DATA[item]


def load_data(file: str = "inventory.json") -> bool:
    """
    Load inventory data from a JSON file.

    Args:
        file (str): The path to the JSON file.

    Returns:
        bool: True if successful, False otherwise.
    """
    global STOCK_DATA  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            STOCK_DATA = json.load(f)
        logging.info("Loaded inventory data from %s", file)
        return True
    except FileNotFoundError:
        logging.warning("File '%s' not found. Starting with empty", file)
        STOCK_DATA = {}
        return False
    except json.JSONDecodeError as json_error:
        logging.error("Error decoding JSON from '%s': %s", file, json_error)
        return False


def save_data(file: str = "inventory.json") -> bool:
    """
    Save inventory data to a JSON file.

    Args:
        file (str): The path to the JSON file.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(STOCK_DATA, f, indent=2)
        logging.info("Saved inventory data to %s", file)
        return True
    except IOError as io_error:
        logging.error("Error writing to '%s': %s", file, io_error)
        return False


def print_data() -> None:
    """Print a formatted report of all items in inventory."""
    print("\n" + "="*40)
    print("INVENTORY REPORT")
    print("="*40)
    if not STOCK_DATA:
        print("No items in inventory")
    else:
        for item, quantity in STOCK_DATA.items():
            print(f"{item:20s} -> {quantity:5d}")
    print("="*40 + "\n")


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Check for items below a certain threshold.

    Args:
        threshold (int): The quantity threshold.

    Returns:
        List[str]: List of item names below the threshold.
    """
    result = []
    for item, quantity in STOCK_DATA.items():
        if quantity < threshold:
            result.append(item)
    return result


def main() -> None:
    """Main function to demonstrate inventory system functionality."""
    logging.info("Starting inventory system")

    # Add valid items
    add_item("apple", 10)
    add_item("banana", 5)
    add_item("orange", 3)

    # Demonstrate validation (these will be rejected)
    add_item("grape", -2)  # Negative quantity - will be rejected
    add_item(123, 10)  # Invalid type - will be rejected

    # Remove items
    remove_item("apple", 3)
    remove_item("orange", 1)

    # Get quantities
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items (threshold=5): {check_low_items()}")

    # Save and load data
    save_data()
    load_data()

    # Print report
    print_data()

    # Replaced dangerous eval() with safe alternative
    logging.info("Inventory system operations completed")


if __name__ == "__main__":
    main()