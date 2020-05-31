import re
from collections import Counter
from datetime import datetime
from apps.user import take_config, calculate_age
from apps.config import cfg_db


class Criteria:

    def __init__(self, user, user_list):
        self.user = user
        self.user_list = user_list
        self.without_close = []
        self.with_groups = []
        self.criteria = take_config(cfg_db)

    def users_with_common_groups(self):
        user_ids = [i['id'] for i in self.user_list]
        if not self.user.groups:
            result = []
            return result
        else:
            common_groups = []
            for i in self.user.groups:
                res = self.user.is_member(i, user_ids)
                for user in res:
                    if user['member'] == 1:
                        common_groups.append(user['user_id'])
            count_list = Counter(common_groups)

            for user in self.user_list:
                if user['id'] in count_list:
                    user['weight'] += count_list[user['id']]

    def user_weight_all(self):
        for people in self.user_list:
            if people.get('interests'):
                for item in self.user.interests:
                    regex = re.compile(f'{item}')
                    match = re.search(regex, people['interests'])
                    if match:
                        people['weight'] += self.criteria.get('interests')

            if people.get('books'):
                for item in self.user.books:
                    regex = re.compile(f'({item})')
                    match = re.search(regex, people['books'])
                    if match:
                        people['weight'] += self.criteria.get('books')

            if people.get('music'):
                for item in self.user.music:
                    regex = re.compile(f'({item})')
                    match = re.search(regex, people['music'])
                    if match:
                        people['weight'] += self.criteria.get('music')

            try:
                day, month, year = people.get('bdate').split('.')
                age = calculate_age(datetime(year=int(year), month=int(month), day=int(day)))
                if age == self.user.age:
                    people['weight'] += self.criteria.get('age')
            except Exception:
                continue

    def create_list_with_weight(self):
        new_list = []
        for user in self.user_list:
            if user['weight']:
                new_list.append(user)
        self.user_list = new_list

    def sort_list(self):
        self.user_list.sort(key=lambda couple: couple['weight'], reverse=True)


if __name__ == '__main__':
    pass
