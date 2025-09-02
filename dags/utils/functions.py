import os
import shutil

def create_dirs(path_to_create):
    os.makedirs(path_to_create, exist_ok=True)

def clean_path(path_clean):
    if os.path.exists(path_clean):
        shutil.rmtree(path_clean)
        create_dirs(path_clean)
