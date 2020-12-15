from unittest import TestCase

from a10_module.filter import positive, filtering_function
from a10_module.sort import smaller, odd_even_sort, larger


class TestSort(TestCase):
    def setUp(self):
        self.my_list = []

    def test_smaller_empty(self):
        sorted_list = sorted(self.my_list)
        odd_even_sort(self.my_list, smaller)
        self.assertEqual(self.my_list, sorted_list)

    def test_larger_empty(self):
        sorted_list = sorted(self.my_list)
        odd_even_sort(self.my_list, larger)
        self.assertEqual(self.my_list, sorted_list)

    def test_smaller(self):
        self.my_list = [5, 6, 1, 2, 3, 7, 4, 9]
        sorted_list = sorted(self.my_list)
        odd_even_sort(self.my_list, smaller)
        self.assertEqual(self.my_list, sorted_list)

    def test_larger(self):
        self.my_list = [5, 6, 1, 2, 3, 7, 4, 9]
        sorted_list = sorted(self.my_list, reverse=True)
        odd_even_sort(self.my_list, larger)
        self.assertEqual(self.my_list, sorted_list)

    def tearDown(self):
        print("TORE DOWN")


class TestFilter(TestCase):
    def setUp(self):
        self.my_list = []
        self.my_function = positive

    def test_empty_list(self):
        self.assertEqual(self.my_list, filtering_function(self.my_list, self.my_function))

    def test_no_valid_item(self):
        self.my_list = [-2, -4, 0]
        self.assertEqual([], filtering_function(self.my_list, self.my_function))

    def test_one_valid_item(self):
        self.my_list = [-5, 0, -7, 99, -1, -2]
        self.assertEqual([99], filtering_function(self.my_list, self.my_function))

    def test_random(self):
        self.my_list = [20, 69, 16, 5, 1, 0, 73, 81, 3]
        self.assertEqual([16, 1, 0, 81], filtering_function(self.my_list, lambda x: x ** (1/2) == int(x ** (1/2))))

    def tearDown(self):
        print("TORE DOWN")

