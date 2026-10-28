def compress_string(s: str) -> str:
    if not s:
        return ""

    current_char = s[0]
    count = 1
    result = []

    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            result.append(f"{current_char}{count}")
            current_char = s[i]
            count = 1

    # Add the final group
    result.append(f"{current_char}{count}")

    return "".join(result)


text = input("Enter a string: ")
print(compress_string(text))