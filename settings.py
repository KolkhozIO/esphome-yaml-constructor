import os

UPLOADED_FILES_PATH = "./uploaded_files/"
COMPILE_DIR = "./compile_files/"

COMPILE_CMD = "esphome compile"

url_front = os.environ.get('REACT_APP_APP_URL')
SHARE_URL = f"{url_front}/config?uuid="
