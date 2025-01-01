import yaml


with open("genres.yaml", "r") as file:
    genres_data = yaml.safe_load(file)


keys = list(genres_data.keys())

print(keys)