
import csv
import random


def generate_csv(filepath, records):
    """
    Generate a CSV file containing employee records.
    """

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["id", "name", "salary", "department"])

        departments = [
            "Engineering",
            "Finance",
            "Marketing",
            "HR",
            "Sales"
        ]

        for i in range(1, records + 1):

            salary = random.randint(30000, 150000)

            # Introduce missing salary values.
            if random.random() < 0.05:
                salary = ""

            writer.writerow([
                i,
                f"Employee_{i}",
                salary,
                random.choice(departments)
            ])

    print(f"Generated {filepath} with {records} records.")


if __name__ == "__main__":

    generate_csv("large_dataset.csv", 100000)

    generate_csv("dataset_10000.csv", 10000)
    generate_csv("dataset_100000.csv", 100000)
    generate_csv("dataset_500000.csv", 500000)
    generate_csv("dataset_1000000.csv", 1000000)
