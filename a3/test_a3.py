"""CSCA08: Fall 2022 -- Assignment 3: Hypertension and Low Income

Starter code for tests to test function get_bigger_neighbourhood in
a3.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith, David Liu, and Anya Tafliovich

"""

import copy
import unittest
from a3 import get_bigger_neighbourhood as gbn
from a3 import SAMPLE_DATA

SAMPLE_DATA2 = {
    'Whitehorse': {
        'id': 1,
        'hypertension': [704, 13294, 3744, 9664, 3954, 5174],
        'total': 33234, 'low_income': 5940},
    'Marsh Lake': {
        'id': 2,
        'hypertension': [785, 12906, 3575, 8815, 2922, 3922],
        'total': 32941, 'low_income': 9694},
    'Dawson': {
        'id': 3,
        'hypertension': [240, 3621, 1147, 2824, 1649, 1867],
        'total': 10365, 'low_income': 2044},
    'Carcross': {
        'id': 4,
        'hypertension': [206, 3662, 1137, 3229, 1395, 1855],
        'total': 10365, 'low_income': 2144},
    'Mayo': {
        'id': 5,
        'hypertension': [172, 3356, 1047, 2872, 949, 1342],
        'total': 9461, 'low_income': 2325}
}


class TestGetBiggerNeighbourhood(unittest.TestCase):
    """Test the function get_bigger_neighbourhood."""

    def test_first_bigger(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when its population is strictly greater than the
        population of the second neighbourhood.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'Elms-Old Rexdale')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_second_bigger(self):
        """Test that get_bigger_neighbourhood correctly returns the second
        neighbourhood when its population is strictly greater than the
        population of the first neighbourhood.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Elms-Old Rexdale', 'Rexdale-Kipling')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_same(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when its population is the same as the population
        of the second neighbourhood.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA2)
        expected = 'Carcross'
        actual = gbn(SAMPLE_DATA2, 'Carcross', 'Dawson')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_first_exclude(self):
        """Test that get_bigger_neighbourhood correctly returns the second
        neighbourhood when the first neighbourhood is not in the data
        city_data.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'West Humber-Clairville'
        actual = gbn(SAMPLE_DATA, 'a', 'West Humber-Clairville')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_both_exclude(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when both neighbourhoods are not in data city_data,
        meaning that both population are 0.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'b'
        actual = gbn(SAMPLE_DATA, 'b', 'a')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_second_exclude(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when the second neighbourhood is not in data
        city_data.

        """

        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'e')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_most_published_authors(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
