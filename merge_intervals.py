def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # Sort intervals by their starting point
    sorted_intervals = sorted(intervals)

    #Start with the first interval
    result = [sorted_intervals[0][:]]

    for current in sorted_intervals[1:]:
        #Get the last merged interval
        last = result[-1]

        #Check whether the intervals overlap or touch
        if current[0] <= last[1]:
            #Extend the ending point if necessary
            last[1] = max(last[1], current[1])
        else:
            #No overlap: add a new interval
            result.append(current[:])
        
    return result



print(merge_intervals([[1,3],[2,6],[9,12],[8,10]]))

print(merge_intervals([[1,4],[4,5]]))

print(merge_intervals([[1,10], [3,4]]))