def selection(lst):
    lst_func = list(lst)
    for i in range(len(lst_func)):
        min_idx = i
        for j in range(i + 1, len(lst_func)):
            if lst_func[min_idx] > lst_func[j]:
                min_idx = j
        lst_func[i], lst_func[min_idx] = lst_func[min_idx], lst_func[i]

    return lst_func