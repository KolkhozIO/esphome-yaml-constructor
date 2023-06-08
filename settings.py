from envparse import Env

env = Env()

UPLOADED_FILES_PATH = "./uploaded_files/"
COMPILE_DIR = "./compile_files/"
COMPILE_CMD = "esphome compile"

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
