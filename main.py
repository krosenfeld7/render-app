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
    """
    app_settings_path = os.path.join(os.getcwd(), "config")
    app_settings_path = os.path.join(app_settings_path, "app_settings.json")
    blender_settings_path = os.path.join(os.getcwd(), "config")
    blender_settings_path = os.path.join(blender_settings_path, "blender_settings.json")

    app_settings = app_settings(app_settings_path)
    blender_settings = blender_settings(blender_settings_path)

    #print(blender_settings.__dict__)
    #print(blender_settings.render_settings().__dict__)
    #print(blender_settings.eevee_settings().__dict__)
    #print(blender_settings.cycles_settings().__dict__)
    #print(blender_settings.background_settings().__dict__)

    type_settings_path = os.path.join(os.getcwd(), "config")
    type_settings_path = os.path.join(type_settings_path, "types.json")
    type_settings = type_settings(type_settings_path)
    """
