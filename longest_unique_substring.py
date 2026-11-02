def longest_unique_substring(s: str) -> int:
    left = 0
    last_seen = {}
    max_length = 0

    for right, ch in enumerate(s):

        if ch in last_seen and last_seen[ch] >= left:
            left = max(left, last_seen[ch] + 1)
        
        last_seen[ch] = right

        current_length = right - left + 1
        max_length = max(max_length, current_length)

    return max_length


print(longest_unique_substring("abcabcbbrtyg"))

