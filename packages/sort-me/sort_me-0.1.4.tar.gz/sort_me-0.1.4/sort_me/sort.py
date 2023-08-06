#import bubble
#import insertion
#import selection
#import quick
#import merge
def bubble(lst, status = True):
    lst_func = list(lst)
    for j in range(len(lst_func)):
        for i in range(len(lst_func) - 1 - j):
            if lst_func[i] <= lst_func[i + 1]:
                pass

            elif lst_func[i] > lst_func[i + 1]:
                lst_func[i], lst_func[i + 1] = lst_func[i + 1], lst_func[i]

    return lst_func

def insertion(lst):
    lst_func = list(lst)
    for i in range(1, len(lst_func)):
        key = lst_func[i]
        j = i - 1
        while j >= 0 and lst_func[j] > key:
            lst_func[j + 1] = lst_func[j]
            j = j - 1
        lst_func[j + 1] = key

    return lst_func

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

def quick(lst):
    lst_func = list(lst)

    def partition(lst_func, low, high):
        i = (low - 1)
        pivot = lst_func[high]

        for j in range(low, high):
            if lst_func[j] <= pivot:
                i = i + 1
                lst_func[i], lst_func[j] = lst_func[j], lst_func[i]

        lst_func[i + 1], lst_func[high] = lst_func[high], lst_func[i + 1]
        return (i + 1)


    def quickSort(lst_func, low, high):
        if len(lst_func) == 1:
            return lst_func
        if low < high:
            pi = partition(lst_func, low, high)

            quickSort(lst_func, low, pi - 1)
            quickSort(lst_func, pi + 1, high)


    n = len(lst_func)
    quickSort(lst_func, 0, n - 1)
    return lst_func

def selection(lst):
    lst_func = list(lst)
    for i in range(len(lst_func)):
        min_idx = i
        for j in range(i + 1, len(lst_func)):
            if lst_func[min_idx] > lst_func[j]:
                min_idx = j
        lst_func[i], lst_func[min_idx] = lst_func[min_idx], lst_func[i]

    return lst_func


class sort:

    def __init__(self):
        pass

    def bubble(self, lst):
        return bubble.bubble(lst)

    def insertion(self, lst):
        return insertion.insertion(lst)

    def selection(self, lst):
        return selection.selection(lst)

    def quick(self, lst):
        return quick.quick(lst)

    def merge(self, lst):
        return merge.merge(lst)