def first_non_repeating(numbers):
    count = {}

    # Step 1: Count the frequency of each number
    for number in numbers:
        if number in count:
            count[number] += 1
        else:
            count[number] = 1

    # Step 2: Find the first number that appears exactly once
    for number in numbers:
        if count[number] == 1:
            return number

    # Step 3: No non-repeating number was found
    return None


n = int(input("How many numbers? "))

numbers = []

for i in range(n):
    number = int(input("Enter a number: "))
    numbers.append(number)

result = first_non_repeating(numbers)
print("First non-repeating element:", result)