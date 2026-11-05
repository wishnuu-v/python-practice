from copy import deepcopy
from typing import Any


class Dataset:

    def __init__(self, data: list[dict[str, Any]]) -> None:

        if not isinstance(data, list):
            raise TypeError("Dataset must be initialized with a list.")

        if not data:
            self._data = []
            self._columns = []
            return

        if not all(isinstance(record, dict) for record in data):
            raise TypeError("Every record must be a dictionary.")

        # Get column names from the first record
        self._columns = list(data[0].keys())

        if not self._columns:
            raise ValueError("Records must contain at least one column.")

        # Validate that all records follow the same schema
        for index, record in enumerate(data):
            if list(record.keys()) != self._columns:
                raise ValueError(
                    f"Record at index {index} does not match the dataset schema."
                )

        # Store a deep copy to protect internal data
        self._data = deepcopy(data)

    def columns(self) -> list[str]:
        """Return column names."""
        return self._columns.copy()

    def shape(self) -> tuple[int, int]:
        """Return number of records and columns."""
        return (len(self._data), len(self._columns))

    def get_column(self, column_name: str) -> list[Any]:
        """Retrieve values from a specific column."""
        if column_name not in self._columns:
            raise KeyError(f"Column '{column_name}' does not exist.")

        return deepcopy([
            record[column_name] for record in self._data
        ])

    def get_record(self, index: int) -> dict[str, Any]:
        """Retrieve an individual record."""
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Record index must be an integer.")

        try:
            return deepcopy(self._data[index])
        except IndexError:
            raise IndexError(
                f"Record index {index} is out of range."
            ) from None

    def add_record(self, record: dict[str, Any]) -> None:
        """Add a new record after validating its schema."""
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary.")

        if list(record.keys()) != self._columns:
            raise ValueError(
                "New record must contain exactly the existing columns "
                "in the same order."
            )

        self._data.append(deepcopy(record))

    def select_columns(self, selected_columns: list[str]) -> "Dataset":
        """Return a new Dataset containing selected columns."""
        if not isinstance(selected_columns, list):
            raise TypeError("Selected columns must be provided as a list.")

        if not selected_columns:
            raise ValueError("At least one column must be selected.")

        if len(selected_columns) != len(set(selected_columns)):
            raise ValueError("Duplicate column names are not allowed.")

        for column in selected_columns:
            if column not in self._columns:
                raise KeyError(f"Column '{column}' does not exist.")

        new_data = [
            {
                column: deepcopy(record[column])
                for column in selected_columns
            }
            for record in self._data
        ]

        return Dataset(new_data)

    def __len__(self) -> int:
        """Return the number of records."""
        return len(self._data)

    def __repr__(self) -> str:
        """Return a meaningful string representation."""
        return (
            f"Dataset(shape={self.shape()}, "
            f"columns={self._columns})"
        )

data = [
    {"name": "Alice", "age": 25, "salary": 50000},
    {"name": "Bob", "age": 30, "salary": 60000},
    {"name": "Charlie", "age": 28, "salary": 55000}
]

dataset = Dataset(data)

print("Columns:", dataset.columns())

print("Shape:", dataset.shape())

print("Number of records:", len(dataset))

print("Number of columns:", len(dataset.columns()))

print("Age column:", dataset.get_column("age"))

print("First record:", dataset.get_record(0))

dataset.add_record({
    "name": "David",
    "age": 35,
    "salary": 70000
})

print("After adding record:", dataset.shape())

subset = dataset.select_columns(["name", "salary"])

print("Selected columns:", subset.columns())
print("Selected dataset:", subset.shape())

print(dataset)

record = dataset.get_record(0)
record["name"] = "Modified"

print("Original record:", dataset.get_record(0))