from os import path, getcwd

from src.entry import execute


if __name__ == "__main__":
    # for now just call entry.py
    parameters = {'app_settings': "app_settings.json",
                  'blender_settings': "blender_settings.json",
                  'types': "types.json"}
    full_paths = dict()

    for entry in parameters:
        rel_path = path.join('config', parameters[entry])
        full_paths[entry] = path.join(getcwd(), rel_path)

    execute(full_paths)
