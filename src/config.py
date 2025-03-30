import json
import os

class Config:
    settings = dict()

    def get_default_config_path(self):
        return os.path.join(os.path.dirname(__file__), '..', 'default_config.json')

    def get_config_path(self):
        return os.path.join(os.path.dirname(__file__), '..', 'config.json')

    def __init__(self):
        try:
            default_config_path = self.get_default_config_path()
            with open(default_config_path, "r") as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            print("Default configuration file not found. Please ensure 'default_config.json' exists.")
            exit(1)
        except json.JSONDecodeError:
            print("Error decoding JSON from the configuration file.")
            exit(1)

        config_path = self.get_config_path()
        print(f"config path: {config_path}")
        if not os.path.exists(config_path):
            print("Config file does not exist. Creating new one.")
            with open(config_path, "w") as file:
                json.dump(self.settings, file, indent=4)
        print("Configuration loaded successfully.")

    def get_config_value(self, key: str):
        """
        Retrieves a value from the CONFIG dictionary using the provided key.
        :param key: The key for the desired configuration value.
        :return: The value associated with the key, or None if the key does not exist.
        """
        return self.settings.get(key, None)

    def get_config(self):
        return self.settings

    def set_config(self, config: dict):
        new_settings = dict()
        for key, val in self.settings.items():
            if isinstance(val, bool):
                new_settings[key] = key in config
            else:
                new_settings[key] = config[key]
        self.settings = new_settings

        config_path = self.get_config_path()
        with open(config_path, "w") as file:
            json.dump(self.settings, file, indent=4)

config_instance: Config = Config()