import yaml


def load_config(config_path, encoding='utf-8'):
    """Load a YAML configuration file."""
    with open(config_path, 'r', encoding=encoding) as file:
        return yaml.safe_load(file)
