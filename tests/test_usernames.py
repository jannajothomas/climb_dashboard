import unittest

import web_requests


class MyTestCase(unittest.TestCase):
    def test_get_usernames_janna(self):
        actual_names = web_requests.get_user_data('janna thomas')
        expected_names = [('janna thomas', '7027871'), ('janna thomas', '200907314')]
        self.assertEqual(expected_names, actual_names)

    def test_get_usernames_susan(self):
        actual_names = web_requests.get_user_data('susan jensen')
        expected_names = [('susan jensen', '7027752')]
        self.assertEqual(expected_names, actual_names)


if __name__ == '__main__':
    unittest.main()
