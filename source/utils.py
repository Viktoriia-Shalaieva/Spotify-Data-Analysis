import yaml


def get_secrets(secret_group):
    with open('.credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)

    secrets = credentials.get(secret_group)

    return secrets
