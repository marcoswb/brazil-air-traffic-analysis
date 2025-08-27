from dotenv import load_dotenv
import os

load_dotenv()


def get_env(key_env):
    return os.getenv(key_env)

def create_dirs(path_to_create):
    os.makedirs(path_to_create, exist_ok=True)