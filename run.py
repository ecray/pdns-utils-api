import os

from app import pdns_utils

config_name = os.getenv('APP_SETTINGS')
app = pdns_utils(config_name)

if __name__ == '__main__':
        app.run()
