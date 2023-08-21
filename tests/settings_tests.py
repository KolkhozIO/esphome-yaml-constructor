import json
from uuid import uuid4

config_data = {
    'esphome': {
        'name': 'edfhgkd'
    },
    'esp32': {
        'board': 'esp32doit-devkit-v1',
        'framework': {
            'type': 'arduino'
        }
    },
    'api': {
        'password': 'password'
    },
    'ota': {
        'password': 'password'
    },
    'wifi': {
        'password': 'password',
        'ap': {
            'password': 'password',
            'ssid': 'sdfg'
        },
        'ssid': '23dc'
    },
    'logger': {
        'level': 'debug',
        'baud_rate': 1024
    },
    'i2c': {
        'sda': 21,
        'scl': 22,
        'scan': True
    }
}


config_failed_data = {
    'esphome': {
        'name': ''
    },
    'esp32': {
        'board': 'esp32doit-devkit-v1',
        'framework': {
            'type': 'arduino'
        }
    },
    'api': {
        'password': ''
    },
    'ota': {
        'password': ''
    },
    'wifi': {
        'password': '',
        'ap': {
            'password': '',
            'ssid': ''
        },
        'ssid': ''
    },
    'logger': {
        'level': 'debug'
    },
    'i2c': {
        'sda': 21,
        'scl': 22,
        'scan': True
    }
}

config_data_two = {
    'esphome': {
        'name': 'test2'
    },
    'esp32': {
        'board': 'esp32doit-devkit-v1',
        'framework': {
            'type': 'arduino'
        }
    },
    'api': {
        'password': 'password'
    },
    'ota': {
        'password': 'password'
    },
    'wifi': {
        'password': 'password',
        'ap': {
            'password': 'password',
            'ssid': 'sdfg'
        },
        'ssid': '23dc'
    },
    'logger': {
        'level': 'debug',
        'baud_rate': 1024
    },
    'i2c': {
        'sda': 21,
        'scl': 22,
        'scan': True
    }
}


user_data = {
        'user_id': '105383501433443125091',
        'name': 'Петр',
        'surname': 'Петров',
        'email': 'petr@gmail.com',
        'is_active': True,
    }


test_config_data = {
        'name_config': uuid4(),
        'hash_yaml': '205d5758d4cc066603a617faf6ad7c29',
        'name_esphome': 'edfhgkd',
        'platform': 'ESP32',
        'compile_test': False,
        'config_json': json.dumps(config_data),
    }


test_config_two_data = {
        'name_config': uuid4(),
        'hash_yaml': 'dc574c778c684d8e375fd8a2ace364e9',
        'name_esphome': 'test2',
        'platform': 'ESP32',
        'compile_test': False,
        'config_json': json.dumps(config_data_two),
    }


google_profile_one = {
        'googleId': '105383501433443125091',
        'imageUrl': 'https://lh3.googleusercontent.com/a/Aasdetdvp_AKqaxgAaouTOHTeYbmoG48KMbTwo-KlLxuBks3_GM=s96-c',
        'email': 'petr@gmail.com',
        'name': 'Петров Петр',
        'givenName': 'Петров',
        'familyName': 'Петр'
    }


google_profile_two = {
        'imageUrl': 'https://lh3.googleusercontent.com/a/AAcsdfdp_AKqaxgAaouTOHTeYbmoG48KMbTwo-KlLxuBks3_GM=s96-c',
        'email': 'petr@gmail.com',
        'name': 'Петров Петр',
        'givenName': 'Петров',
        'familyName': 'Петр'
    }
