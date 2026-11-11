
class Dataset:
    def __init__(self, data):
        self.data = [row.copy() for row in data]

    # Validate column names
    def _validate_column(self, column):
        if not self.data:
            return

        if column not in self.data[0]:
            raise ValueError(f"Invalid column name: {column}")

    # Create a new Dataset
    def _new_dataset(self, data):
        return Dataset(data)

    # 1. Filtering
    def filter(self, condition):
        filtered_data = [
            row for row in self.data
            if condition(row)
        ]

        return self._new_dataset(filtered_data)

    # 2. Sorting
    def sort_by(self, column, descending=False):
        self._validate_column(column)

        sorted_data = sorted(
            self.data,
            key=lambda row: row[column],
            reverse=descending
        )

        return self._new_dataset(sorted_data)

    # 3. Grouping
    def group_by(self, column):
        self._validate_column(column)

        groups = {}

        for row in self.data:
            key = row[column]

            if key not in groups:
                groups[key] = []

            groups[key].append(row.copy())

        return groups

    # 4. Counting
    def value_counts(self, column):
        groups = self.group_by(column)

        return {
            key: len(rows)
            for key, rows in groups.items()
        }

    # Shared aggregation helper
    def _calculate(self, values, operation):

        if operation == "mean":
            return sum(values) / len(values) if values else None

        elif operation == "min":
            return min(values) if values else None

        elif operation == "max":
            return max(values) if values else None

        elif operation == "sum":
            return sum(values)

        elif operation == "count":
            return len(values)

        else:
            raise ValueError(
                f"Unsupported aggregation: {operation}"
            )

    # 5. Aggregation
    def aggregate(self, group_column, target_column, operations):

        self._validate_column(group_column)
        self._validate_column(target_column)

        groups = self.group_by(group_column)

        # Support both single and multiple operations
        if isinstance(operations, str):
            operations = [operations]

        results = {}

        for group, rows in groups.items():

            values = [
                row[target_column]
                for row in rows
                if row[target_column] is not None
            ]

            if len(operations) == 1:
                results[group] = self._calculate(
                    values, operations[0]
                )
            else:
                results[group] = {
                    operation: self._calculate(values, operation)
                    for operation in operations
                }

        return results

    # Display dataset
    def show(self):
        for row in self.data:
            print(row)

    # Dataset length
    def __len__(self):
        return len(self.data)


employees = [
    {"name": "Alice", "age": 28, "department": "Engineering", "salary": 50000},
    {"name": "Bob", "age": 32, "department": "Marketing", "salary": 60000},
    {"name": "Charlie", "age": 24, "department": "Engineering", "salary": 55000},
    {"name": "David", "age": 35, "department": "Finance", "salary": 75000},
    {"name": "Eva", "age": 29, "department": "Engineering", "salary": 52000},
    {"name": "Frank", "age": 26, "department": "Marketing", "salary": 60000},
]

dataset = Dataset(employees)


result = dataset.filter(lambda row: row["age"] > 25)

result.show()


result = dataset.sort_by("salary", descending=True)

result.show()


result = dataset.group_by("department")

print(result)


result = dataset.value_counts("department")

print(result)


result = dataset.aggregate(
    "department",
    "salary",
    "mean"
)

print(result)