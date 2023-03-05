import yaml


def get_yaml_data(path_to_file):
    with open(path_to_file) as f:
        data = yaml.safe_load(f)
    return data
