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


def save_vk_picture(access_token, group_id, upload_reponse):

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'v': 5.131,
        'group_id': group_id,
        'photo': upload_reponse['photo'],
        'server': upload_reponse['server'],
        'hash': upload_reponse['hash'],
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def post_vk_picture(access_token, group_id, save_response, comment):
    picture_id = save_response["response"][0]['id']
    owner_id = save_response["response"][0]['owner_id']

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


def get_randon_comic():

    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    total_comic = response.json()['num']

    number_comic = randint(0, total_comic)
    response = requests.get(f'https://xkcd.com/{number_comic}/info.0.json')
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
    access_token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    filename, comment = get_randon_comic()

    try:
        upload_response = upload_vk_picture(access_token, group_id, filename)
        check_vk_response(upload_response)
        save_reponse = save_vk_picture(access_token, group_id, upload_response)
        check_vk_response(save_reponse)
        post_respons = post_vk_picture(access_token, group_id, save_reponse, comment)
        check_vk_response(post_respons)

    finally:
        os.remove(filename)


if __name__ == '__main__':
    main()
