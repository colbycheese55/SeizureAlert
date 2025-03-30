import json
import os

CONFIG = dict()


def read_in_config() -> None:
    """
    Reads the configuration from a JSON file and stores it in the CONFIG dictionary.
    """
    global CONFIG
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, "r") as file:
            CONFIG = json.load(file)
        print("Configuration loaded successfully.")
    except FileNotFoundError:
        print("Configuration file not found. Please ensure 'config.json' exists.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the configuration file.")


def get_config_value(key: str):
    """
    Retrieves a value from the CONFIG dictionary using the provided key.
    :param key: The key for the desired configuration value.
    :return: The value associated with the key, or None if the key does not exist.
    """
    return CONFIG.get(key, None)