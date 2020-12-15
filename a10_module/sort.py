def smaller(x, y):
    return x <= y


def larger(x, y):
    return x >= y


def odd_even_sort(list_for_sorting, comparison_function):
    """
    Use Odd-even algorithm to sort a given list by a given comparison function
    :param list_for_sorting:
    :param comparison_function:
    :return: nothing, the list is modified in the memory
    """
    is_sorted = False
    length = len(list_for_sorting)
    while not is_sorted:
        is_sorted = True
        for odd_index in range(1, length - 1, 2):
            first = list_for_sorting[odd_index]
            second = list_for_sorting[odd_index + 1]
            if comparison_function(first, second):
                continue
            else:
                list_for_sorting[odd_index] = second
                list_for_sorting[odd_index + 1] = first
                is_sorted = False
        for even_index in range(0, length - 1, 2):
            first = list_for_sorting[even_index]
            second = list_for_sorting[even_index + 1]
            if comparison_function(first, second):
                continue
            else:
                list_for_sorting[even_index] = second
                list_for_sorting[even_index + 1] = first
                is_sorted = False


def sort_dictionary(dictionary, function):
    """
    Sort a dictionary by converting it into a list of tuples and then using the odd-even sort
    algorithm implemented to sort the converted dictionary
    After sorting, the list of tuples is converted back into a dictionary
    :param dictionary: a dictionary
    :param function: a boolean value function used for comparison between elements
    :return: the sorted dictionary
    """
    converted_to_list = list(dictionary.items())
    odd_even_sort(converted_to_list, function)
    sorted_list = converted_to_list
    return {item[0]: item[1] for item in sorted_list}


'''
def test():
    my_list = [5, 6, 2, 9, 1, 7, 3, 2]
    my_list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    odd_even_sort(my_list, smaller)
    print(my_list)

test()
'''

