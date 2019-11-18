import json
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "config/secrets.json"), encoding="utf-8") as f:
    secrets_dict = json.loads(f.read())


class ImproperlyConfigured(Exception):
    pass


def get_secret(setting: str, secrets: dict = secrets_dict) -> str:
    """
    returns parameter from dict config file

    :param setting: name of parameter
    :type setting: str
    :param secrets: dict file with params
    :type secrets: dict
    :return:
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


def create_dir(path: str) -> None:
    """
    This function receives path and creates a new directory if it wasn`t created earlier

    :param path: dirname with path
    :type path: str
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)

def process_is_running(process_name):
    """
    Checks if there is running process with given name

    :param process_name: process name
    :type process_name: str
    :return:
    """
    p = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    already_running = False

    for line in out.decode('utf-8').splitlines():
        # Find tesseract process
        if process_name in line:
            already_running = True

    return already_running