import os
import requests
from urllib.parse import urljoin


USER_API_BASE = {}


class UtilsException(Exception): pass


def get_cpu_usage(host, username, token):
    user_part = f'api/v0/user/{username}'
    response = requests.get(
        f'https://{host}/{user_part}/cpu/',
        headers=get_auth(token)
    )
    if response.ok:
        print('CPU quota info:')
        print(response.content)
    else:
        raise UtilsException(response.reason)


def get_api_base(username, token):
    global USER_API_BASE
    if username in USER_API_BASE:
        return USER_API_BASE[username]

    hosts = [
        'www.pythonanywhere.com',
        'eu.pythonanywhere.com'
    ]
    for host in hosts:
        user_part = f'api/v0/user/{username}'
        try:
            get_cpu_usage(host, username, token)
        except UtilsException:
            continue
        else:
            USER_API_BASE[username] = f'https://{host}/{user_part}/'
            return USER_API_BASE[username]

    raise UtilsException(f'There are no suitable hosts: {response.reason}')


def get_auth(token):
    """
    To work with pythonanywhere.com we have to pass auth token for every requset
    """
    return {'Authorization': f'Token {token}'}


def send_file(path, content, username, token):
    """
    Send file using post-method.

    :param str path: Should contain path for the sent file in pythonanywhere filesystem (inside home directory)
        (for example, 'project/templates/projectname/index.html')
    :param str content: content is a string content of the file
    :param str username: name of user on pythonanywhere platform
    :param str token: secret token to use pythonanywhere's API
    """
    url = urljoin(get_api_base(username, token), f'files/path/home/{username}/{path.lstrip("/")}')
    print(url)
    return requests.post(
        url,
        files={'content': content},
        headers=get_auth(token)
    )


def reload_app(username, token):
    """
    Reload pythonanywhere application

    :param str app_name: name of application on pythonanywhere platform
    :param str username: name of user on pythonanywhere platform
    :param str token: secret token to use pythonanywhere's API
    """
    return requests.post(
        urljoin(get_api_base(username, token), f'webapps/{username}.pythonanywhere.com/reload/'),
        headers=get_auth(token)
    )
