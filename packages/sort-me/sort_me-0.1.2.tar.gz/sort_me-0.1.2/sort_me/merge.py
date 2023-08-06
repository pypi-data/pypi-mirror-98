def merge(lst_func):
    if len(lst_func) > 1:
        mid = len(lst_func) // 2
        left = lst_func[:mid]
        right = lst_func[mid:]

        # Recursive call on each half
        merge(left)
        merge(right)

        i = 0
        j = 0
        k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                # The value from the left half has been used
                lst_func[k] = left[i]
                # Move the iterator forward
                i += 1
            else:
                lst_func[k] = right[j]
                j += 1
            # Move to the next slot
            k += 1

        while i < len(left):
            lst_func[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            lst_func[k] = right[j]
            j += 1
            k += 1

    return lst_func