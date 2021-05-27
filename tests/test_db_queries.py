import unittest

import db


class MyTestCase(unittest.TestCase):
    def setUp(self):
        myCon = db.create_connection("climbTest")
        db.create_tables_if_needed(myCon)
        tick1 = ['friday', 'War and  Peace', 'dc', 'my notes on this',
                 'dc', 'dc', 'Bonsai > *Rumney > New Hampshire', 'dc',
                 'dc', 'lead', 'redpoint']
        tick2 = ['friday', 'Espresso', 'dc', 'my notes on this',
                 'dc', 'dc', 'The Parking Lot Wall > *Rumney > New Hampshire', 'dc',
                 'dc', 'lead', 'redpoint']
        db.add_tick_to_table(myCon, tick1, '7027752')
        db.add_tick_to_table(myCon, tick2, '7027871')
        route1 = ['War and  Peace', 'Bonsai > *Rumney > New Hampshire', 'two', 'three', 'four', 'five', '5.9']
        route2 = ['Espresso', 'The Parking Lot Wall > *Rumney > New Hampshire', 'two', 'three', 'four', 'five', '5.9']
        route3 = ['Giant Man', 'Bonsai > *Rumney > New Hampshire', 'two', 'three', 'four', 'five', '5.10 b/c']
        route4 = ['Flying Hawaiian', 'Waimea > *Rumney > New Hampshire', 'two', 'three', 'four', 'five', '5.10 a']

        db.add_route_to_table(myCon, route1)
        db.add_route_to_table(myCon, route2)
        db.add_route_to_table(myCon, route3)
        db.add_route_to_table(myCon, route4)
        myCon.close()

    def test_query_ticks_only_with_username(self):
        query_results = db.get_rows('Rumney', 'all', 9, 'false', 'all', '7027752', 'climbTest')
        expected_results = [
                ('Bonsai', 'War and  Peace', '5.9', 'friday', 'lead', 'redpoint', 'my notes on this'),
                ('The Parking Lot Wall', 'Espresso', '5.9', None, None, None, None)
        ]
        self.assertEqual(expected_results, query_results)

        query_results = db.get_rows('Rumney', 'all', 9, 'false', 'all', '7027871', 'climbTest')
        expected_results = [
            ('Bonsai', 'War and  Peace', '5.9', None, None, None, None),
            ('The Parking Lot Wall', 'Espresso', '5.9', 'friday', 'lead', 'redpoint', 'my notes on this')
        ]
        self.assertEqual(expected_results, query_results)

    def test_query_ticks_no_username(self):
        query_results = db.get_rows('Rumney', 'all', 9, 'false', 'all', '', 'climbTest')
        expected_results = [
            ('Bonsai', 'War and  Peace', '5.9', None, None, None, None),
            ('The Parking Lot Wall', 'Espresso', '5.9', None, None, None, None)
        ]
        self.assertEqual(expected_results, query_results)

    def test_query_remaining(self):

        query_results = db.get_rows('Rumney', 'all', 9, 'false', 'remaining', '', 'climbTest')
        expected_results = [
            ('Bonsai', 'War and  Peace', '5.9', None, None, None, None),
            ('The Parking Lot Wall', 'Espresso', '5.9', None, None, None, None)
        ]
        self.assertEqual(expected_results, query_results)

    def test_query_view_all_exact_match_true(self):
        query_results = db.get_rows('Rumney', 'all', 10, 'true', 'all', '', 'climbTest')
        expected_results = [
            ('Waimea', 'Flying Hawaiian', '5.10a', None, None, None, None)
        ]
        self.assertEqual(expected_results, query_results)

    def test_query_completed_exact_match_false(self):
        query_results = db.get_rows('Rumney', 'all', 10, 'false', 'completed', '7027752', 'climbTest')
        expected_results = [
            ('Bonsai', 'War and  Peace', '5.9', 'friday', 'lead', 'redpoint', 'my notes on this')
        ]
        self.assertEqual(expected_results, query_results)

    def test_query_completed_exact_match_true(self):
        query_results = db.get_rows('Rumney', 'all', 10, 'true', 'completed', '7027752', 'climbTest')
        expected_results = []
        self.assertEqual(expected_results, query_results)

    def test_query_remaining_exact_match_true(self):
        query_results = db.get_rows('Rumney', 'all', 10, 'true', 'remaining', '', 'climbTest')
        expected_results = [
            ('Waimea', 'Flying Hawaiian', '5.10a', None, None, None, None)
        ]
        self.assertEqual(expected_results, query_results)


if __name__ == '__main__':
    unittest.main()
