def smaller(x, y):
    return x <= y


def larger(x, y):
    return x >= y


def odd_even_sort(list_for_sorting, comparison_function):
    is_sorted = False
    length = len(list_for_sorting)
    while not is_sorted:
        is_sorted = True
        for even_index in range(0, length - 1, 2):
            first = list_for_sorting[even_index]
            second = list_for_sorting[even_index + 1]
            if comparison_function(first, second):
                continue
            else:
                list_for_sorting[even_index] = second
                list_for_sorting[even_index + 1] = first
                is_sorted = False
        for odd_index in range(1, length - 1, 2):
            first = list_for_sorting[odd_index]
            second = list_for_sorting[odd_index + 1]
            if comparison_function(first, second):
                continue
            else:
                list_for_sorting[odd_index] = second
                list_for_sorting[odd_index + 1] = first
                is_sorted = False


'''
def test():
    my_list = [5, 6, 2, 9, 1, 7, 3, 2]
    my_list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    odd_even_sort(my_list, smaller)
    print(my_list)

test()
'''

