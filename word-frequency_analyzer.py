def analyze_text(text: str) -> dict:

    # Step 1: Convert text to lowercase
    text = text.lower()

    # Step 2: Replace punctuation with spaces
    punctuation = ".,!?:;'\"()"

    for char in punctuation:
        text = text.replace(char, " ")

    # Step 3: Split text into individual words
    words = text.split()

    # Step 4: Count word frequencies
    frequencies = {}

    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    # Step 5: Sort words by frequency and alphabetically
    sorted_words = sorted(
        frequencies.items(),
        key=lambda item: (-item[1], item[0])
    )

    # Step 6: Get the five most frequent words
    top_words = sorted_words[:5]

    # Step 7: Return the analysis
    return {
        "total_words": len(words),
        "unique_words": len(frequencies),
        "frequencies": frequencies,
        "top_words": top_words
    }

if __name__ == "__main__":

    text = "Python is great! Python is useful, and Python is popular."

    result = analyze_text(text)

    print(result)