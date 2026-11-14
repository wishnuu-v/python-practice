
import csv


def read_csv_batches(filepath, batch_size=1000):
    """
    Read a CSV file incrementally and yield batches.

    Each batch contains dictionaries with column names
    as keys.
    """

    if isinstance(batch_size, bool) or not isinstance(batch_size, int):
        raise TypeError("batch_size must be an integer")

    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    with open(filepath, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file, strict=True)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing headers")

        batch = []

        try:
            for row in reader:

                # Skip records with missing or extra fields.
                if None in row or any(
                    value is None for value in row.values()
                ):
                    continue

                batch.append(row)

                if len(batch) == batch_size:
                    yield batch
                    batch = []

            if batch:
                yield batch

        except csv.Error as error:
            print(f"Malformed CSV record near line {reader.line_num}: {error}")


def process_csv(filepath, column, batch_size=1000):
    """
    Calculate statistics for a numerical CSV column
    without loading the entire dataset into memory.
    """

    total_records = 0
    missing_values = 0
    valid_count = 0

    total_sum = 0.0
    minimum = None
    maximum = None

    for batch in read_csv_batches(filepath, batch_size):

        for row in batch:

            total_records += 1

            value = row.get(column)

            if value is None or value.strip() == "":
                missing_values += 1
                continue

            try:
                number = float(value)

            except (ValueError, TypeError):
                missing_values += 1
                continue

            total_sum += number
            valid_count += 1

            if minimum is None or number < minimum:
                minimum = number

            if maximum is None or number > maximum:
                maximum = number

    return {
        "total_records": total_records,
        "mean": total_sum / valid_count if valid_count else None,
        "minimum": minimum,
        "maximum": maximum,
        "missing_values": missing_values
    }


if __name__ == "__main__":

    filepath = "large_dataset.csv"
    column = "salary"

    print("CSV STREAMING PROCESSOR")
    print("-" * 40)

    try:
        results = process_csv(
            filepath=filepath,
            column=column,
            batch_size=1000
        )

        for key, value in results.items():
            print(f"{key}: {value}")

    except FileNotFoundError:
        print(f"File not found: {filepath}")
