import math


def validate_data(data):
    """Validate and convert input into a list of finite numbers."""
    values = list(data)

    if not values:
        raise ValueError("Dataset cannot be empty.")

    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Dataset must contain only numerical values.")

        if not math.isfinite(value):
            raise ValueError("Dataset cannot contain NaN or infinity.")

    return values


def mean(data):
    values = validate_data(data)
    return sum(values) / len(values)


def median(data):
    values = sorted(validate_data(data))
    n = len(values)

    middle = n // 2

    if n % 2 == 1:
        return values[middle]

    return (values[middle - 1] + values[middle]) / 2


def variance(data):
    """Calculate population variance."""
    values = validate_data(data)
    avg = mean(values)

    return sum((x - avg) ** 2 for x in values) / len(values)


def standard_deviation(data):
    """Calculate population standard deviation."""
    return math.sqrt(variance(data))


def minimum(data):
    return min(validate_data(data))


def maximum(data):
    return max(validate_data(data))


def data_range(data):
    values = validate_data(data)
    return max(values) - min(values)


def min_max_normalization(data):
    values = validate_data(data)

    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        return [0.0 for _ in values]

    return [
        (x - min_value) / (max_value - min_value)
        for x in values
    ]


def z_score_normalization(data):
    values = validate_data(data)

    avg = mean(values)
    std = standard_deviation(values)

    if std == 0:
        return [0.0 for _ in values]

    return [(x - avg) / std for x in values]


class Dataset:
    """Reusable dataset class with column-wise statistics."""

    def __init__(self, data):
        self.data = data

    def describe(self):
        if not self.data:
            raise ValueError("Dataset cannot be empty.")

        columns = {}

        for row in self.data:
            for column, value in row.items():
                columns.setdefault(column, []).append(value)

        for column, values in columns.items():
            print(f"Column: {column}")
            print(f"Mean: {mean(values):g}")
            print(f"Minimum: {minimum(values):g}")
            print(f"Maximum: {maximum(values):g}")
            print()


# Example usage
if __name__ == "__main__":

    data = [10, 20, 30, 40, 50]

    print("Mean:", mean(data))
    print("Median:", median(data))
    print("Variance:", variance(data))
    print("Standard deviation:", standard_deviation(data))
    print("Minimum:", minimum(data))
    print("Maximum:", maximum(data))
    print("Range:", data_range(data))

    print("Min-max normalization:",
          min_max_normalization(data))

    print("Z-score normalization:",
          z_score_normalization(data))

    # Bonus: Column-wise statistics
    records = [
        {"age": 25, "salary": 50000},
        {"age": 30, "salary": 55000},
        {"age": 35, "salary": 75000}
    ]

    dataset = Dataset(records)
    dataset.describe()