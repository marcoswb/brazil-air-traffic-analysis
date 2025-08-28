from dotenv import load_dotenv
import os
import shutil

load_dotenv()


def get_env(key_env):
    return os.getenv(key_env)

def create_dirs(path_to_create):
    os.makedirs(path_to_create, exist_ok=True)

def clean_path(path_clean):
    if os.path.exists(path_clean):
        shutil.rmtree(path_clean)
        create_dirs(path_clean)
