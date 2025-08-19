from dotenv import load_dotenv
import os

load_dotenv()


def get_env(key_env):
    return os.getenv(key_env)
