import configparser
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DEFAULT_CONFIG_FILE = BASE_DIR / 'config.ini'
DEFAULT_WRITE_KEY = ''
DEFUALT_VIEW_KEY = ''
CONFIG = {}


def get_path(s):
    s = s.strip('"\'')
    return Path(s).expanduser()


config = configparser.ConfigParser()
with open(DEFAULT_CONFIG_FILE) as f:
    config.read_file(f)
config_file = os.environ.get('TW5_CONFIG_FILE')
if config_file:
    with open(config_file) as f:
        config.read_file(f)
CONFIG['TW5_TEMPLATE_URL'] = config['server']['template_url']
CONFIG['TW5_TEMPLATE_FILE'] = get_path(config['server']['template_file'])
CONFIG['TW5_WIKI_ROOT'] = get_path(config['server']['wiki_root'])
authentication = {}
for section in config.sections():
    if not section.startswith('wiki.'):
        continue
    view_key = config.get(section, 'view_key', fallback='')
    write_key = config.get(section, 'write_key', fallback='')
    section = section[len('wiki.'):]
    authentication[section] = {
        'view_key': view_key,
        'write_key': write_key,
    }
CONFIG['TW5_AUTHENTICATION'] = authentication
