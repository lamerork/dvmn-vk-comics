import os
from random import randint
from urllib.parse import unquote, urlsplit
import requests
from dotenv import load_dotenv


def check_vk_response(response):
    try:
        error = response['error']
        raise Exception(f'Код ошибки "{error["error_code"]}"\nСообщение: "{error["error_msg"]}"')
    except KeyError:
        return


def upload_vk_picture(access_token, group_id, filename):

    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': group_id,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vk_api_response = response.json()
    upload_url = vk_api_response['response']['upload_url']

    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    return response.json()


def save_vk_picture(access_token, group_id, vk_photo, vk_server, vk_hash):

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': group_id,
        'photo': vk_photo,
        'server': vk_server,
        'hash': vk_hash,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def post_vk_picture(access_token, group_id, picture_id, owner_id, comment):

    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': group_id,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{picture_id}',
        'message': comment,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_picture_extension(image_url):

    link_split = urlsplit(image_url)
    file_name = unquote(link_split[2])
    file_extension = os.path.splitext(file_name)
    return file_extension[1]


def get_random_comic():

    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    total_comics = response.json()['num']

    comic_number = randint(0, total_comics)
    response = requests.get(f'https://xkcd.com/{comic_number}/info.0.json')
    response.raise_for_status()
    random_comic = response.json()
    image_url = random_comic['img']
    comment = random_comic['alt']

    picture_extension = get_picture_extension(image_url)
    filename = f'temp_picture{picture_extension}'

    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename, comment


def main():

    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    filename, comment = get_random_comic()

    try:
        upload_response = upload_vk_picture(vk_access_token, vk_group_id, filename)
        check_vk_response(upload_response)
        vk_photo = upload_response['photo']
        vk_server = upload_response['server']
        vk_hash = upload_response['hash']
        save_response = save_vk_picture(vk_access_token, vk_group_id, vk_photo, vk_server, vk_hash)
        check_vk_response(save_response)
        picture_id = save_response["response"][0]["id"]
        owner_id = save_response["response"][0]["owner_id"]
        post_response = post_vk_picture(vk_access_token, vk_group_id, picture_id, owner_id, comment)
        check_vk_response(post_response)

    finally:
        os.remove(filename)


if __name__ == '__main__':
    main()
