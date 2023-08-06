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