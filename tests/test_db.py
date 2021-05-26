import unittest
import db


class MyTestCase(unittest.TestCase):
    def test_database_creation(self):
        con = db.create_connection("climbDash")
        self.assertIsNotNone(con)

    def test_create_tables(self):
        con = db.create_connection("climbTest")

        # Make sure all tables are dropped
        remove_all_tables(con)
        sql = '''SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE(TABLE_SCHEMA='climbTest') AND (TABLE_NAME='grades');
                '''
        cur = con.cursor()
        cur.execute(sql)
        self.assertIsNone(cur.fetchone())

        # Create Tables
        db.create_tables_if_needed(con)
        cur = con.cursor()
        cur.execute(sql)
        self.assertIsNotNone(cur.fetchone())
        con.close()

    def test_add_table(self):
        user_id = '1234567'
        con = db.create_connection("climbTest")
        sql = '''DELETE FROM ticks'''
        cur = con.cursor()
        cur.execute(sql)

        row = 'date', 'name', 'unknown', 'notes', 'unknown', \
              'unknown', 'location', 'unknown', 'unknown', 'style', 'lead_style'
        db.add_tick_to_table(con, row, user_id)

        con = db.create_connection("climbTest")
        sql = '''SELECT * FROM ticks'''
        cur = con.cursor()
        cur.execute(sql)
        actual = []
        for item in cur.fetchone():
            actual.append(item)
        expected = ['datenamestylelead_style', 'name', 'location', 'date', 'style', 'lead_style', 'notes', '1234567']
        self.assertEqual(actual, expected)

    def test_add_route_to_table(self):
        # Add row to table

        con = db.create_connection("climbTest")
        sql = '''DELETE FROM routes'''
        cur = con.cursor()
        cur.execute(sql)

        row = 'name', 'wall > crag > Rumney', 'two', 'three', 'four', 'five', 'grade'
        db.add_route_to_table(con, row)

        # Verify that row was added
        con = db.create_connection("climbTest")
        sql = '''SELECT * FROM routes'''

        cur = con.cursor()
        cur.execute(sql)
        actual = []
        for item in cur.fetchone():
            actual.append(item)
        expected = ['name', 'grade', 'Rumney', 'crag', 'wall > crag > Rumney', 'wall', 'namewall > crag > Rumney']
        self.assertEqual(expected, actual)

        con = db.create_connection("climbTest")
        sql = '''DELETE FROM routes'''
        cur = con.cursor()
        cur.execute(sql)

        row = 'name', 'crag > lots of stuff > Bishop', 'two', 'three', 'four', 'five', 'grade'
        db.add_route_to_table(con, row)

        # Verify that row was added
        con = db.create_connection("climbTest")
        sql = '''SELECT * FROM routes'''

        cur = con.cursor()
        cur.execute(sql)
        actual = []
        for item in cur.fetchone():
            actual.append(item)
        expected = ['name', 'grade', 'Bishop', 'crag',
                    'crag > lots of stuff > Bishop', '', 'namecrag > lots of stuff > Bishop']
        self.assertEqual(expected, actual)

    def test_get_area_crag_wall(self):
        locations = ['GOT > Pine Creek Canyon > Bishop Area > Sierra Eastside > California',
                     'The Parking Lot Wall > *Rumney > New Hampshire',
                     'Gorgeous Towers > Upper Gorge > Owens River Gorge > Bishop Area > Sierra Eastside > California',
                     'Player\'s Club > Central Gorge > Owens River Gorge > Bishop Area > Sierra Eastside > California',
                     'Megalithic > Inner Gorge > Owens River Gorge > Bishop Area > Sierra Eastside > California',
                     'Bonsai > *Rumney > New Hampshire The Parking Lot Wall > *Rumney > New Hampshire',
                     'Triple Corners Left > Triple Corners > *Rumney > New Hampshire']

        expected = [('Bishop', 'GOT', ''),
                    ('Rumney', 'The Parking Lot Wall', ''),
                    ('Bishop', 'Gorgeous Towers', ''),
                    ('Bishop', 'Player\'s Club', ''),
                    ('Bishop', 'Megalithic', ''),
                    ('Rumney', 'Bonsai', ''),
                    ('Rumney', 'Triple Corners', 'Triple Corners Left')]

        for location in locations:
            area_crag_wall = db.get_area_crag_wall(location)
            self.assertEqual(expected[0], area_crag_wall)
            expected.pop(0)


def remove_all_tables(con):
    cur = con.cursor()
    sql = '''DROP TABLE IF EXISTS grades;
                    '''
    cur.execute(sql)


if __name__ == '__main__':
    unittest.main()
