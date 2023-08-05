# HK, 15.12.20

import warnings
from pathlib import Path
import configparser

import requests


def get_config_path() -> Path:
    """Get the config path."""

    config_path = Path('~/.config/norby_config.ini').expanduser()
    assert config_path.exists(), f'Config file not found under {config_path}. ' \
                                 f'Please fill the example under config and move it to {config_path}.'

    return config_path


def get_config():
    config_path = get_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def send_msg(message: str):
    """
    Send message to telegram chat bot.

    message str: text message to be sent to the chat bot.
    """
    config = get_config()
    token = config['telegram_bot']['token']
    chat_id = config['telegram_bot']['chat_id']
    url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    result = requests.get(url_req)
    if result == '<Response [404]>':
        warnings.warn(f'Could not contact Norby, error: {result} \n url_req: {url_req}')
