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