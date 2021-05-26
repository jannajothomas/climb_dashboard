from unittest import TestCase

import constants
import utilities


class Test(TestCase):

    def test_update_args_contained_dictionary(self):
        my_dict = {'view': 'all',
                   'grade': '9',
                   'exact_match': 'true',
                   'name_to_search': ''}

        new_dict = utilities.update_args(sample_args(), my_dict)
        expected_form_values = {'view': 'all',
                                'grade': '7',
                                'exact_match': 'false',
                                'name_to_search': ''}

        self.assertDictEqual(expected_form_values, new_dict)

    def test_update_args_ext_dictionary(self):
        # Setup
        my_dict = constants.default_param_dict
        # Test
        new_dict = utilities.update_args(sample_args(), my_dict)
        expected_form_values = {
            'name_selected': '',
            'crag': 'all',
            'view': 'all',
            'exact_match': 'false',
            'name_to_search': '',
            'user': '',
            'grade': '7',
            'all_grades': constants.display_grade,
            'area': 'Rumney'
        }
        # Assertion
        self.assertDictEqual(expected_form_values, new_dict)


def sample_args():
    data = {'view': 'all',
            'grade': '7',
            'exact_match': 'false',
            'name_to_search': ''}
    return data
