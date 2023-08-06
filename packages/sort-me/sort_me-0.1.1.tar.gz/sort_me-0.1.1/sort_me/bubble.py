def bubble(lst, status = True):
    lst_func = list(lst)
    for j in range(len(lst_func)):
        for i in range(len(lst_func) - 1 - j):
            if lst_func[i] <= lst_func[i + 1]:
                pass

            elif lst_func[i] > lst_func[i + 1]:
                lst_func[i], lst_func[i + 1] = lst_func[i + 1], lst_func[i]

    return lst_func