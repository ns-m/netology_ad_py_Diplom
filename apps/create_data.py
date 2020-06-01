class DataMaker:

    def __init__(self, user, user_list):
        self.user = user
        self.user_list = user_list

    def take_photo(self, people):
        photo_list = self.user.vk_api.photos.get(owner_id=people['id'], album_id='profile', extended=1)
        top_photo = []
        if photo_list['count'] > 2:
            photo_list['items'].sort(key=lambda dictionary: dictionary['likes'].get('count'), reverse=True)
            for item in photo_list['items'][0:3]:
                url = item['sizes'][len(item['sizes']) - 1]['url']
                top_photo.append(url)
            people.update({'photo': {
                                     '1': top_photo[0],
                                     '2': top_photo[1],
                                     '3': top_photo[2]
                                    }
                          })
        else:
            people.update({'photo': None})

    def take_ten_json(self):
        json_file = []
        for user in self.user_list:
            self.take_photo(user)
            if user.get('photo'):
                json_file.append({
                    'id': user['id'],
                    'photo': user['photo'],
                    'link': 'https://vk.com/id{}'.format(user['id'])
                })
                if len(json_file) == 10:
                    break
        return json_file
