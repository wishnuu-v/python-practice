def merge_sorted_lists(a: list[int], b: list[int]) -> list[int]:
    
    result = []

    p1 = 0
    p2 = 0

    #Compare elements while both lists have elements remaining
    while p1 < len(a) and p2 < len(b):

        if a[p1] <= b[p2]:
            result.append(a[p1])
            p1 += 1

        else:
            result.append(b[p2])
            p2 += 1

    #Add any remaining elements
    result.extend(a[p1:])
    result.extend(b[p2:])

    return result


print(merge_sorted_lists([1,4,7],[2,3,8]))