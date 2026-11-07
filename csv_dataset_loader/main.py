from dataset import Dataset, load_csv


# Load CSV
dataset = load_csv("employees.csv")

# Display dataset information
print(dataset)

# Display shape
print("Shape:", dataset.shape())

# Retrieve individual columns
print("Names:", dataset.get_column("name"))
print("Ages:", dataset.get_column("age"))
print("Salaries:", dataset.get_column("salary"))

# Export dataset
dataset.to_csv("output.csv")

print("CSV exported successfully!")