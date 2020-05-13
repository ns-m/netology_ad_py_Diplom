import psycopg2 as pg
from apps.user import take_config


class Database:

    def __init__(self):
        self.data = take_config('config.json')
        self.db = pg.connect(**self.data['data'])

    def create_db(self):
        with self.db as conn:
            with conn.cursor() as curs:
                curs.execute("""CREATE TABLE user_for (
                        id serial PRIMARY KEY NOT NULL,
                        vk_id varchar(100) UNIQUE NOT NULL);
                        """)
                curs.execute("""CREATE TABLE user_couple (
                        id serial PRIMARY KEY,
                        user_id varchar(100) REFERENCES user_for(vk_id),
                        couple_vk_id varchar(100) NOT NULL,
                        link text NOT NULL,
                        photo_link_1 text NOT NULL,
                        photo_link_2 text NOT NULL,
                        photo_link_3 text NOT NULL);
                        """)

    def check_tables(self):
        with self.db as conn:
            with conn.cursor() as curs:
                curs.execute("select * from pg_tables where tablename = 'user_for'")
                user_table = curs.fetchone()
                curs.execute("select * from pg_tables where tablename = 'user_couple'")
                user_couple_table = curs.fetchone()

                if user_table and user_couple_table:
                    return True

    def create_user(self, user_vk_id):
        with self.db as conn:
            with conn.cursor() as curs:
                curs.execute("insert into user_for (vk_id) values (%s) RETURNING id", (user_vk_id,))
                ids = curs.fetchone()
        return ids

    def take_user(self):
        with self.db as conn:
            with conn.cursor() as curs:
                curs.execute("select vk_id from user_for")
                data = curs.fetchall()
        return data

    def insert_json(self, data_list, ids):
        with self.db as conn:
            with conn.cursor() as curs:
                for couple in data_list:
                    curs.execute("insert into user_couple (user_id, couple_vk_id, link, photo_link_1, photo_link_2,"
                                 "photo_link_3) values (%s, %s, %s, %s, %s, %s)", (ids, couple['id'], couple['link'],
                                                                                   couple['photo']['1'],
                                                                                   couple['photo']['2'],
                                                                                   couple['photo']['3']))

    def get_couple(self):
        with self.db as conn:
            with conn.cursor() as curs:
                curs.execute("select couple_vk_id from user_couple")
                data = curs.fetchall()
        return data

if __name__ == '__main__':
    pass
