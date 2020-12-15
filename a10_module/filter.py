def positive(x):
    if x > 0:
        return True
    return False


def filtering_function(list_for_filtering, filter_function):
    filtered_list = []
    for item in list_for_filtering:
        if filter_function(item):
            filtered_list.append(item)
    return filtered_list


'''
def test():
    my_list = [-1, 1, -2, 2, -3, 3, 0, 7, -9, 4]
    function = positive
    print(filtering_function(my_list, function))

test()
'''
