import csv
from pathlib import Path


class Dataset:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def shape(self):
        """Return (number of rows, number of columns)."""
        return (len(self.data), len(self.columns))

    def get_column(self, column_name):
        """Return all values from a specified column."""
        if column_name not in self.columns:
            raise ValueError(
                f"Column '{column_name}' does not exist."
            )

        index = self.columns.index(column_name)

        return [row[index] for row in self.data]

    def __repr__(self):
        return (
            f"Dataset(rows={len(self.data)}, "
            f"columns={len(self.columns)})"
        )

    def to_csv(self, filepath):
        """Export the dataset to a CSV file."""
        path = Path(filepath)

        try:
            with path.open(
                mode="w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                # Write column names
                writer.writerow(self.columns)

                # Write records
                writer.writerows(self.data)

        except OSError as e:
            raise OSError(
                f"Could not write CSV file '{path}': {e}"
            ) from e


def convert_value(value):
    """
    Convert string values into appropriate Python types.

    Empty values become None.
    Integers become int.
    Decimal numbers become float.
    Other values remain strings.
    """

    value = value.strip()

    if value == "":
        return None

    # Try integer conversion
    try:
        return int(value)
    except ValueError:
        pass

    # Try floating-point conversion
    try:
        return float(value)
    except ValueError:
        pass

    # Preserve textual values
    return value


def load_csv(filepath: str) -> Dataset:
    """
    Load a CSV file and return a Dataset object.

    Handles:
    - File-not-found errors
    - Empty files
    - Missing values
    - Malformed rows
    - Numerical type conversion
    """

    path = Path(filepath)

    # Check whether file exists
    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: '{path}'"
        )

    try:
        with path.open(
            mode="r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.reader(file)

            # Read column names
            try:
                columns = next(reader)
            except StopIteration:
                # Empty file
                return Dataset([], [])

            columns = [column.strip() for column in columns]

            if not columns or any(column == "" for column in columns):
                raise ValueError(
                    "CSV header contains empty column names."
                )

            if len(set(columns)) != len(columns):
                raise ValueError(
                    "CSV contains duplicate column names."
                )

            data = []

            # Process individual records
            for line_number, row in enumerate(reader, start=2):

                # Ignore completely empty rows
                if not row:
                    continue

                # Validate row length
                if len(row) != len(columns):
                    raise ValueError(
                        f"Malformed CSV at line {line_number}: "
                        f"Expected {len(columns)} values, "
                        f"but found {len(row)}."
                    )

                # Convert values
                converted_row = [
                    convert_value(value)
                    for value in row
                ]

                data.append(converted_row)

            return Dataset(columns, data)

    except FileNotFoundError:
        raise

    except UnicodeDecodeError as e:
        raise ValueError(
            f"Unable to decode CSV file '{path}'. "
            "Ensure it uses UTF-8 encoding."
        ) from e

    except csv.Error as e:
        raise ValueError(
            f"Error parsing CSV file '{path}': {e}"
        ) from e

    except OSError as e:
        raise OSError(
            f"Could not read CSV file '{path}': {e}"
        ) from e

