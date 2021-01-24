import environ
import os


def create_env_vars():
    root = environ.Path(__file__) - 2
    BASE_DIR = root()
    env = environ.Env(DEBUG=(bool, False))
    env.read_env(os.path.join(BASE_DIR, '.migrate_config'))
