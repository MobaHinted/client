import os
from dotenv import load_dotenv

import cassiopeia
import cassiopeia_diskstore  # Required for building to executable

import hinter.settings
import hinter.users

import hinter.struct.user

# Set up settings
settings = hinter.settings.Settings()
settings.load_settings()

# Get ready for Cassiopeia
cassiopeia_path = os.getcwd() + '\\data\\cassiopeia'
if not os.path.exists(cassiopeia_path):
    os.mkdir(cassiopeia_path)
cassiopeia_settings = {
    'pipeline': {
        'Cache': {},
        'SimpleKVDiskStore': {
            'package': 'cassiopeia_diskstore',
            'path': cassiopeia_path,
        },
        'DDragon': {},
    },
}

# Set up Cassiopeia, either with local key or proxy kernel
try:
    if not os.path.exists('.env'):
        raise Exception('No .env file found')

    load_dotenv('.env')
    cassiopeia.set_riot_api_key(os.getenv('RIOT_API_KEY'))
    cassiopeia_settings['pipeline']['RiotAPI'] = {
        'api_key': os.getenv('RIOT_API_KEY'),
    }
    print('USING: Development Key (RIOT\'s servers)')
except Exception:
    cassiopeia_settings['pipeline']['Kernel'] = {
            'server_url': 'https://mhk-api.zbee.dev',
            'port': '443',
        }
    print('USING: Kernel with key (zbee\'s servers)')

# Load basic settings for Cassiopeia
cassiopeia.apply_settings(cassiopeia_settings)
cassiopeia.set_default_region(settings.region)

# Set up user control
users = hinter.users.Users()
