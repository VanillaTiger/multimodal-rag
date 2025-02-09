import os, yaml

def read_secret_keys_to_environ():
    # Read the secrets.yaml file and export each variable
    with open('secrets/secrets.yaml', 'r') as file:
        secrets = yaml.safe_load(file)
        for key, value in secrets.items():
            os.environ[key] = str(value)