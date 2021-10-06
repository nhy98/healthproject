import yaml


def get_config():
    with open('./src/config/config.yaml', 'rb') as f:
        cfg = yaml.safe_load(f)
    return cfg
