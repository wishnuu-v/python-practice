def validate_operation(operation, inventory):
    operation_type = operation.get("type")
    product = operation.get("product")
    quantity = operation.get("quantity")

    if operation_type not in ("purchase", "restock"):
        return "Unknown operation type"

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return "Invalid quantity"

    if product not in inventory:
        return f"Unknown product: {product}"

    if operation_type == "purchase" and inventory[product] < quantity:
        return f"Insufficient stock for {product}"

    return None


def process_purchase(inventory, product, quantity):
    inventory[product] -= quantity


def process_restock(inventory, product, quantity):
    inventory[product] += quantity


def process_inventory(inventory: dict, operations: list[dict]) -> dict:
    updated_inventory = inventory.copy()

    successful_operations = 0
    failed_operations = 0
    errors = []

    for operation in operations:
        product = operation.get("product")
        quantity = operation.get("quantity")
        operation_type = operation.get("type")

        error = validate_operation(operation, updated_inventory)

        if error:
            failed_operations += 1
            errors.append(error)
            continue

        if operation_type == "purchase":
            process_purchase(updated_inventory, product, quantity)

        elif operation_type == "restock":
            process_restock(updated_inventory, product, quantity)

        successful_operations += 1

    return {
        "inventory": updated_inventory,
        "successful_operations": successful_operations,
        "failed_operations": failed_operations,
        "errors": errors
    }

inventory = {
    "laptop": 10,
    "mouse": 25,
    "keyboard": 15
}

operations = [
    {"type": "purchase", "product": "laptop", "quantity": 2},
    {"type": "purchase", "product": "mouse", "quantity": 30},
    {"type": "restock", "product": "keyboard", "quantity": 10},
    {"type": "purchase", "product": "monitor", "quantity": 1},
    {"type": "purchase", "product": "laptop", "quantity": 3}
]

result = process_inventory(inventory, operations)

print(result)
print("Original inventory:", inventory)