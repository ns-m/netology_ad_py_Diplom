import unittest
from apps import user, database
import psycopg2 as pg

PATH = '../config.json'


class TestData(unittest.TestCase):
    def setUp(self):
        self.config = user.take_config(PATH)

    def tearDown(self):
        pass

    def test_init(self):
        with self.assertRaises(TypeError):
            self.user = user.User('171691064')
            # self.user = user.User('')

    def test_have_config(self):
        self.assertTrue(type(self.config) == dict)
        self.assertEqual(len(self.config), 3)


class TestDB(unittest.TestCase):
    def setUp(self):
        self.config = user.take_config(PATH)
        self.db = pg.connect(**self.config['data'])
        self.vk_db = database.Database()

    def test_check_table(self):
        self.assertTrue(self.vk_db.check_tables)


if __name__ == '__main__':
    unittest.main()