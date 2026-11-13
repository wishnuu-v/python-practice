
from copy import deepcopy
from numbers import Real


class Dataset:
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Dataset must be a list of dictionaries.")

        if not all(isinstance(row, dict) for row in data):
            raise TypeError("Every record must be a dictionary.")

        # Keep an independent copy of the original data
        self.data = deepcopy(data)

    # 1. Missing-value detection

    def is_missing(self, column):
        """
        Return information about missing values in a column.
        Missing values are represented by None.
        """

        missing_records = []

        for index, row in enumerate(self.data):
            if column not in row:
                raise KeyError(f"Column '{column}' does not exist.")

            if row[column] is None:
                missing_records.append({
                    "index": index,
                    "record": deepcopy(row)
                })

        return {
            "column": column,
            "missing_count": len(missing_records),
            "missing_indices": [
                item["index"] for item in missing_records
            ],
            "missing_records": missing_records
        }

    # 2. Missing-value counts

    def missing_counts(self):
        """
        Return the number of missing values in each column.
        """

        counts = {}

        for row in self.data:
            for column in row:
                if column not in counts:
                    counts[column] = 0

                if row[column] is None:
                    counts[column] += 1

        return counts

    # 3. Remove incomplete records

    def drop_missing(self):
        """
        Return a new Dataset without records containing
        missing values.
        """

        clean_data = [
            deepcopy(row)
            for row in self.data
            if all(value is not None for value in row.values())
        ]

        return Dataset(clean_data)

    # 4 and 5. Fill missing values

    def fill_missing(self, column, value=None, strategy=None):
        """
        Fill missing values using:
        1. A constant value.
        2. The numerical mean.

        Returns a new Dataset.
        """

        if strategy not in (None, "mean"):
            raise ValueError(
                "Supported strategies: None or 'mean'."
            )

        if strategy == "mean" and value is not None:
            raise ValueError(
                "Provide either a value or a strategy, not both."
            )

        # Validate column existence
        for row in self.data:
            if column not in row:
                raise KeyError(f"Column '{column}' does not exist.")

        if strategy == "mean":

            # Collect non-missing values
            values = [
                row[column]
                for row in self.data
                if row[column] is not None
            ]

            # Ensure all existing values are numerical
            if not all(
                isinstance(v, Real) and not isinstance(v, bool)
                for v in values
            ):
                raise TypeError(
                    f"Column '{column}' must contain numerical values."
                )

            # Handle columns containing only None
            if not values:
                raise ValueError(
                    f"Cannot calculate mean: column '{column}' "
                    "contains only missing values."
                )

            fill_value = sum(values) / len(values)

        else:
            if value is None:
                raise ValueError(
                    "Provide a replacement value or strategy='mean'."
                )

            fill_value = value

        # Create a new independent dataset
        new_data = deepcopy(self.data)

        for row in new_data:
            if row[column] is None:
                row[column] = fill_value

        return Dataset(new_data)

    # 6. Apply transformations

    def apply(self, column, function):
        """
        Apply a transformation function to every non-missing
        value in the specified column.

        Returns a new Dataset.
        """

        if not callable(function):
            raise TypeError("Transformation must be callable.")

        new_data = deepcopy(self.data)

        for row in new_data:
            if column not in row:
                raise KeyError(f"Column '{column}' does not exist.")

            value = row[column]

            # Preserve missing values
            if value is not None:
                transformed_value = function(value)

                # Do not silently turn valid data into None
                if transformed_value is None:
                    raise ValueError(
                        "Transformation cannot return None."
                    )

                row[column] = transformed_value

        return Dataset(new_data)

    # Remove duplicate records

    def drop_duplicates(self, subset=None):
        """
        Remove duplicate records.

        If subset is provided, compare only those columns.
        Otherwise, compare entire records.

        Keeps the first occurrence.
        """

        if subset is not None and not isinstance(subset, (list, tuple)):
            raise TypeError("Subset must be a list or tuple of columns.")

        if subset is not None:
            for row in self.data:
                for column in subset:
                    if column not in row:
                        raise KeyError(
                            f"Column '{column}' does not exist."
                        )

        seen = set()
        unique_data = []

        for row in self.data:

            if subset is None:
                key_columns = tuple(sorted(row.keys()))
                key = (
                    key_columns,
                    tuple(
                        (column, self._make_hashable(row[column]))
                        for column in key_columns
                    )
                )

            else:
                key = tuple(
                    self._make_hashable(row[column])
                    for column in subset
                )

            if key not in seen:
                seen.add(key)
                unique_data.append(deepcopy(row))

        return Dataset(unique_data)

    # Helper: Convert values into hashable representations

    @staticmethod
    def _make_hashable(value):
        if isinstance(value, dict):
            return tuple(
                sorted(
                    (k, Dataset._make_hashable(v))
                    for k, v in value.items()
                )
            )

        if isinstance(value, (list, tuple)):
            return tuple(
                Dataset._make_hashable(v) for v in value
            )

        if isinstance(value, set):
            return frozenset(
                Dataset._make_hashable(v) for v in value
            )

        try:
            hash(value)
            return value
        except TypeError:
            raise TypeError(
                f"Unsupported unhashable value: {type(value).__name__}"
            )

    # Display dataset

    def __repr__(self):
        return f"Dataset({self.data})"

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


# TESTING THE IMPLEMENTATION

data = [
    {"name": "Alice", "age": 25, "salary": 50000},
    {"name": "Bob", "age": None, "salary": 60000},
    {"name": "Charlie", "age": 28, "salary": None},
    {"name": "David", "age": None, "salary": 75000}
]

dataset = Dataset(data)


# 1. Missing-value detection
print("\n1. Missing values in age:")
print(dataset.is_missing("age"))


# 2. Missing-value counts
print("\n2. Missing counts:")
print(dataset.missing_counts())


# 3. Remove incomplete records
print("\n3. Drop missing:")
clean_dataset = dataset.drop_missing()
print(clean_dataset)


# 4. Fill missing values with a constant
print("\n4. Fill missing age with 25:")
filled_dataset = dataset.fill_missing("age", 25)
print(filled_dataset)


# 5. Fill missing values using mean
print("\n5. Fill missing salary using mean:")
mean_dataset = dataset.fill_missing(
    "salary",
    strategy="mean"
)
print(mean_dataset)


# 6. Apply transformations
print("\n6. Increase salary by 10%:")
transformed_dataset = dataset.apply(
    "salary",
    lambda value: value * 1.1
)
print(transformed_dataset)


# Remove duplicates
duplicate_data = [
    {"name": "Alice", "age": 25, "salary": 50000},
    {"name": "Bob", "age": 30, "salary": 60000},
    {"name": "Alice", "age": 25, "salary": 70000},
    {"name": "David", "age": 35, "salary": 75000}
]

duplicate_dataset = Dataset(duplicate_data)

print("\n7. Drop duplicates:")
unique_dataset = duplicate_dataset.drop_duplicates(
    subset=["name", "age"]
)
print(unique_dataset)


# 8. Verify original dataset remains unchanged
print("\n8. Original dataset:")
print(dataset)
