import yaml

def load_config():
    with open("config.yaml", "r") as fd:
        conf = yaml.safe_load(fd)

    return conf
