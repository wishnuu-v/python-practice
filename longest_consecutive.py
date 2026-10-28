def longest_consecutive(nums: list[int]) -> int:
    
    numbers = set(nums)
    longest = 0

    for number in numbers:
        # Start counting only at the beginning of a sequence
        if number - 1 not in numbers:
            current = number
            count = 1

            while current + 1 in numbers:
                current += 1
                count += 1
        
            longest = max(longest, count)
        
    return longest

print(longest_consecutive([100,4,200,1,3,2]))

print(longest_consecutive([1,2,2,3,4]))
















                
    