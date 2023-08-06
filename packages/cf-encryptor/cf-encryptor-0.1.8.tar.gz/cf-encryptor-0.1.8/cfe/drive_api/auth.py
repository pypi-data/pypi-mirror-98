import os

import requests
from pydrive2.auth import GoogleAuth

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
REVOKE = "https://accounts.google.com/o/oauth2/revoke"
SETTINGS_FILE = os.path.join(DIR_PATH, 'settings.yaml')


def drive_login() -> GoogleAuth:
    cwd = change_dir()  # temp solution until we know what will be the working directory

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    os.chdir(cwd)

    return gauth


def drive_logout() -> None:
    cwd = change_dir()

    gauth = GoogleAuth()
    cred_file = gauth.settings.get("save_credentials_file")
    token = os.path.join(DIR_PATH, cred_file)
    gauth.LoadCredentials()
    if not gauth.access_token_expired:
        print('logging out from the gDrive...')
        requests.post(url=REVOKE, params={'token': gauth.credentials.access_token},
                      headers={'Content-type': 'application/x-www-form-urlencoded'})
    os.remove(token)

    os.chdir(cwd)


def change_dir() -> str:
    cwd = os.getcwd()
    os.chdir(DIR_PATH)
    return cwd
