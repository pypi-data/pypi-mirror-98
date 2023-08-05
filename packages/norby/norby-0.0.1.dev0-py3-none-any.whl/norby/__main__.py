# HK, 15.12.20
import argparse
import subprocess
import sys
import time
from pathlib import Path

import subprocess_tee

from .utils import send_msg, get_config


def main():
    """
    Execute input command and send output to telegram bot.
    """
    config = get_config()

    # parsing the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, help='command to be executed')
    input = parser.parse_args()

    start_time = time.time()
    print(f'executing command {input.command}')
    try:
        output = subprocess_tee.run(input.command, shell=True)
        output = output.stdout
        duration = time.time() - start_time
        message = f'Job {input.command} at {config["other"]["loc_name"]} just finished. ' \
                  f'It took {duration} seconds or {duration // 60} minutes. \n '

        # Telegram limits the message length to 4096 characters
        if len(output) > 4095 and config.getboolean('other', 'ppb'):
            import tempfile
            import os

            with tempfile.TemporaryDirectory() as tmpdirname:
                file_path = Path(tmpdirname) / 'tempfile.txt'
                with open(file_path, mode='w') as f:
                    f.write(output)
                ppb_output = str(subprocess.check_output(f'ppb {file_path}', shell=True).rstrip())
            for substr in ppb_output.split():
                if substr.startswith('http'):
                    break
            message += f'The output can be seen here: {substr}.'
        else:
            message += f'The output is: \n\n {output[:3500]}'
    except:
        e = sys.exc_info()[0]
        duration = time.time() - start_time
        message = f'your job got killed with: \n {e} \n It lived for {duration} seconds. Sorry for your loss.'

    send_msg(message)


if __name__ == '__main__':
    sys.exit(main())
