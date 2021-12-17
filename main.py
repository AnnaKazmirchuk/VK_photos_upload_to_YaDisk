import requests
from pprint import pprint
import time
from tqdm import tqdm
import json

with open('VK_TOKEN.txt', 'r') as file_object:
    VK_TOKEN = file_object.read().strip()

class VKUser:

    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {'access_token': token,
                       'v': version}

    def get_photos(self, user_id, count=50):
        profile_photos = dict()
        profile_photo_url = self.url + 'photos.get'
        profile_photo_params = {'owner_id': user_id,
                                'album_id': 'profile',
                                'extended': 1,
                                'photo_sizes': 1,
                                'count': count
                                }

        response = requests.get(profile_photo_url,
                                params={**self.params, **profile_photo_params}).json()['response']['items']
        for photo in response:
            photo_name = photo['likes']['count']
            photo_size = photo['sizes'][-1]['type']
            photo_date = photo['date']
            url_download = photo['sizes'][-1]['url']
            if photo_name not in profile_photos:
                profile_photos[photo_name] = [url_download, photo_size]
            else:
                profile_photos[f'{photo_name}_{photo_date}'] = [url_download, photo_size]
        # pprint(profile_photos)
        return profile_photos

with open('YaDisk_TOKEN.txt', 'r') as file_object:
    YaDisk_TOKEN = file_object.read().strip()

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': folder_name}
        requests.put(url, headers=headers, params=params)
        return folder_name

    def upload_photos_to_disk(self, path_to_file, files_to_upload):
        download_photos_data = []
        self.create_folder(path_to_file)
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for photo_name, photo_url in tqdm(files_to_upload.items()):
            download_photos_data.append({'file_name': f'{photo_name}.jpg',
                                          'size': photo_url[1]}
                                         )
            time.sleep(0.33)
            params = {'path': f'{path_to_file}/{photo_name}',
                      'url': photo_url[0]}
            requests.post(url=url, params=params, headers=headers)
        print('Success')
        return get_photos_info_json(download_photos_data)

def get_photos_info_json(photos_file):
    with open('photo_request.json', 'w', encoding='utf-8') as file:
        json.dump(photos_file, file, indent=2)




if __name__ == '__main__':
    user1 = VKUser(VK_TOKEN, '5.131')
    photos = user1.get_photos(390905222, 5)
    ya1 = YandexDisk(YaDisk_TOKEN)
    folder = ya1.create_folder('Photos_from_VK')

    ya1.upload_photos_to_disk(folder, photos)
