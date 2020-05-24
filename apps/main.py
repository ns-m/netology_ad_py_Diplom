from apps.user import User, take_config
from apps.sort_couple import Criteria
from apps.create_data import DataMaker
from apps.database import Database
from pprint import pprint
import psycopg2 as pg
from sys import exit
from apps.config import Config


def main():
    try:
        try:
            user_id = Config.id if Config.id else input('Input id: ')
            user = User(user_id)
            user.create_session()
            user.get_main_user_data()
        except ValueError:
            print('Invalid age')
            exit()
        try:
            db = Database()
            if not db.check_tables():
                db.create_db()
            users_ids = db.take_user()
            if not users_ids:
                db.create_user(user.id)
            else:
                users_ids_in_table = []
                for row in users_ids:
                    users_ids_in_table += row
                if str(user.id) not in users_ids_in_table:
                    db.create_user(user.id)
            writen_users = db.get_couple()
        except pg.Error as e:
            print(f'Database problem: {e}.\nCheck the configuration in config.json')
            exit()

        print('***** Got enough user information')

        user.take_groups()
        print('***** Got user groups')

        couple_list = user.search_all()
        writen_users_in_table = []
        new_couple_list = []
        if writen_users:
            for row in writen_users:
                writen_users_in_table += row
            for item in couple_list:
                if str(item['id']) not in writen_users_in_table:
                    new_couple_list.append(item)
            print('***** Got a list of possible pairs\nProcessing...')
            list_for_criteria = Criteria(user, new_couple_list)
        else:
            print('***** Got a list of possible pairs\nProcessing...')
            list_for_criteria = Criteria(user, couple_list)

        list_for_criteria.users_with_common_groups()
        print('***** Added weight to users with shared group')

        list_for_criteria.user_weight_all()
        print('***** Added weight to users with common interests and age')

        list_for_criteria.create_list_with_weight()
        list_for_criteria.sort_list()
        sorted_list = list_for_criteria.user_list
        print('***** Sorted by weight')

        list_to_json = DataMaker(user, sorted_list)
        print('***** We collect photos and form json')

        json_f = list_to_json.take_ten_json()
        print('***** Acquired information')
        pprint(json_f)
        try:
            db.insert_json(json_f, user.id)
            print('***** Information added to the database')
        except pg.Error as e:
            print('***** Failed to write information')

    except KeyboardInterrupt:
        print('***** Program aborted')

if __name__ == '__main__':
    pass
