`render-app`

**Overview:**

This app performs blender model aggregation and rendering. This is performed by executing blender in a subprocess and executing all the necessary actions to result in a viable render.

Right now all settings are specified via the json files in the config directory. Maybe at some point in the future I will add a GUI, but this will only happen if other people want to use this.

There are quite a few settings in order to use this app appropriately. There are three settings files in the config directory, these are explained below.


**High Level Settings Discussion:**

1. `app_settings.json`
    - This file provides configuration of the parameters for the app itself including the desired models, using the blacklist, whitelist and many other features.
2. `blender_settings.json`
    - This file provides configuration of the blender specific settings including the render settings, view settings and many more.
3. `types.json`
    - This file provides configuration of some basic types that the app can use to trigger different stats and times off of. These are easily expandable to allow for more time tracking and state tracking. This also includes the collection regex, which can be modified to change how the app selects collections when appending and searching.


**In Depth Settings Discussion:**

`app_settings.json:`
```yaml
{
    "collections": {
        "2": "Materials",
        "1": "Centers",
        "0": "Petals"
    },
    "constants": [
    ],
    "material_collection": "Materials",
    "parameters": {
        "enable_blacklist": false,
        "enable_whitelist": true,
        "enable_logging": false,
        "enable_stat_tracking": true,
        "enable_time_tracking": true,
        "overwrite_all": true,
        "enable_material_combinations": false,
        "combinatorial_type": "specified"
    },
    "paths": {
        "blender_collection_path": "\\Collection\\",
        "blender_exe": "blender.exe",
        "blender_file_extension": ".blend",
        "driver": "src\\driver.py",
        "log_dir": "logs",
        "main_file": "blend_file\\template_generator.blend",
        "output_dir": "..\\output",
        "search_dir": ".."
    },
    "blacklist": [
    ],
    "whitelist": [
        "petals014",
        "squarefractal",
        "rosegold"
    ],
    "orthographic_components": [
        "honeycomb"
    ],
    "material_combinations": [
        ["shinygold", "shinysilver"]
    ]
}
```

The `collections` field is used to specify the collections to be searched and appended to the template blender model. Each collection is to be provided a priority (0 is the highest priority), which indicates which model will be appended first and be swapped out the least. Each collections' value is also the directory name that is searched and the actual collection name within the models that are searched within that directory.

This field is intended to be generic such that you can add as many collection types to it as you want. However, this finds all combinations between the collections so the number of renders will increase rapidly with the number of collections.

The `constants` field is used to specify in app constants as needed. Note: none are used currently

The `material_collection` field is used to specify which collection from the collections' field is the materials' collection. This allows the app to distinguish and apply all materials from the collection to the models before rendering. Thus providing a way to render with many combinations.

The `parameters` field is used to specify inputs to the app to trigger different events. Most of these are self-explanatory, but are spelled out here:
- "enable_blacklist" -> enables the blacklist option
- "enable_whitelist" -> enables the whitelist option
- "enable_logging" -> enables output logging to a file
- "enable_stat_tracking" -> enables stats tracking, see `types.json` for stat types
- "enable_time_tracking" -> enables time tracking, see `types.json` for time types
- "overwrite_all" -> will overwrite output files if set to true, will skip over them otherwise
- "enable_material_combinations" -> enables the option to specify which collections use which materials
- "combinatorial_type" -> supports the following currently and will use the computed materials for the renders:
    - product: computes the product for the combinations of materials (every combination)
    - combinations: computes the combinations of the materials
    - permutations: computes the permutations of the materials
      _Note: these use the itertools functions, see the docs for more info: https://docs.python.org/3/library/itertools.html_
    - specified: this allows for manual input specifying each material in order to the highest priority collection

The `paths` field is used to specify the paths to the app, all paths are relative:
- "blender_collection_path" -> the internal blender collection path, recommended leave as default
- "blender_exe" -> the path to your blender executable
- "blender_file_extension" -> the file extension for your blender models, recommended leave as default
- "driver" -> the path to the render app driver, recommended leave as default
- "log_dir" -> the logs output directory
- "main_file" -> the path to the template blender file, recommended leave as default
- "output_dir" -> the path to the output directory
- "search_dir": -> the path to the local directory where the collections directories are located

The `blacklist` field is used to specify which components you want to skip in the processing. These need to include the name blender files minus any non-alphanumerics:
- e.g. "rose_gold" -> "rosegold"

The `whitelist` field is used to specify which components you want to use in the processing. These need to include the name blender files minus any non-alphanumerics:
- e.g. "rose_gold" -> "rosegold"

_Note: There also is an option to wildcard select all of a specific collection, this is done as follows:
- e.g. "all_<COLLECTION>" -> "all_materials", etc._

_Note 2: It is recommended to avoid using both the blacklist and whitelist at the same time as this will lead to not valid renders frequently._
_Note 3: The blacklist has a higher priority than the whitelist._

The `orthographic_components` field is used to specify which models should use the orthographic camera view instead of perspective. The default camera view is perspective. Specify the blender file name with only alphanumerics.

The `materials_combinations` field is used to specify the materials used in the material combinations' computation specified by the `parameters` -> `combinatorial_type` if `enable_material_combinations` is enabled

`blender_settings.json:`
```yaml
{
    "render_settings": {
        "render_engine": "BLENDER_EEVEE",
        "resolution_x": 2400,
        "resolution_y": 2400,
        "resolution_percentage": 100,
        "use_border": false,
        "film_transparent": true
    },
    "eevee_settings": {
        "samples": 256,
        "bloom": true,
        "ambient_occlusion": true,
        "bloom_intensity": 0.025
    },
    "cycles_settings": {
        "samples": 32,
        "device": "GPU"
    },
    "scene_settings": {
        "frame_start": 1,
        "frame_end": 1
    },
    "view_settings": {
        "look": "Very High Contrast",
        "view_transform": "Filmic",
        "default_exposure": 0.0,
        "exposure_step": 0.0,
        "start_exposure": -2.0,
        "end_exposure": 2.0,
        "enable_exposure_variability": false
    },
    "image_settings": {
        "file_format": "PNG",
        "color_mode": "RGB",
        "color_depth": "8",
        "compression": 0
    },
    "background_settings": {
        "default_emission": 0.5,
        "emission_step": 0.5,
        "max_emission": 1.0,
        "emission_color": [1.0, 1.0, 1.0, 1.0],
        "enable_emission_variability": false,
        "enable_hdri": true,
        "hdri_dir": "hdris",
        "hdris": [
            "courtyard.exr"
        ]
    }
}
```

The majority of these settings are inputs to Blender and are basically exact copies of the types in Blender.

The `render_settings` field specifies generic render information to Blender:
- "render_engine" -> specifies the Blender render engine "BLENDER_EEVEE", "CYCLES"
- "resolution_x" -> the x resolution of the output
- "resolution_y" -> the y resolution of the output
- "resolution_percentage" -> the resolution % of the output
- "use_border" -> indicates that the render should use a border
- "film_transparent" -> indicates if the background should be shown, film transparency

The `eevee_settings` field specifies parameters to the Eevee render engine:
- "samples" -> the render samples to use
- "bloom" -> enables bloom
- "ambient_occlusion" -> enables ambient occlusion
- "bloom_intensity" -> the bloom intensity

The `cycles_settings` field specifies parameters to the Cycles render engine:
- "samples" -> the render samples to use
- "device" -> the render device, "GPU", "CPU", etc.

The `scene_settings` field specifies the frames to render:
- "frame_start" -> the start frame
- "frame_end" -> the end frame
_Note: leave both at 1 to obtain a still image_

The `view_settings` field specifies parameters to the view settings segment:
- "look" -> the contrast level to use
- "view_transform" -> the view transform to use
- "default_exposure" -> the default exposure to use if "enable_exposure_variability" is disabled
- "exposure_step" -> the amount to increase the exposure with each step of the variability
- "start_exposure" -> the starting exposure level
- "end_exposure": -> the ending exposure level
- "enable_exposure_variability" -> specifies if the exposure variability should be used, uses "default_exposure" if disabled

The `image_settings` field specifies parameters to the image settings segment:
- "file_format" -> the output render file type
- "color_mode" -> the output render color mode: "RGB", "RGBA", etc.
- "color_depth" -> the color bit depth to render "8", "16"
- "compression" -> the amount of compression to use 0 -> 100

The `background_settings` field specifies parameters to the background settings segment:
- "default_emission" -> the default emission to start with
- "emission_step" -> the amount to increase the emission with each step of the variability
- "max_emission" -> the ending emission level
- "emission_color" -> the emission color specified by a list of 4 digits: [1.0, 1.0, 1.0, 1.0]
- "enable_emission_variability" -> specifies if the emission variability should be used, uses "default_emission" if disabled
- "enable_hdri" -> specifies if the background should use hdris, this takes priority over the emission variability
- "hdri_dir" -> the directory where the hdris are located, recommended leave as default
- "hdris" -> each hdri that is desired to be rendered against


`types.json:`
```yaml
{
    "stat_types": [
        "clear_all",
        "camera_align",
        "camera_perspective",
        "append_for_collection",
        "render",
        "skipped",
        "invalid_materials"
    ],
    "time_types": [
        "clear_all",
        "clear_collection",
        "get_meshes",
        "update_meshes",
        "get_materials",
        "append",
        "render",
        "camera_align",
        "execution"
    ]
}
```

The `stat_types` field specifies the different actions that the app should track if `enable_stat_tracking` is enabled. At the end of execution, the app will output how many times each action occurred.

The `time_types` field specifies the different actions that the app should track if `enable_time_tracking` is enabled. At the end of execution, the app will output how long the app spent in each area of the code performing each action. This is useful for debugging and finding where the app is spending most of its time.


**Other Important Notes:**

Once everything is set appropriately in the settings files, the directory structure needs to be specified as follows:

- All collection directories need to be at the path of `search_dir`
- The output directory should be at the path of `output_dir`. If it is not, it will be created

The models inside each of the blender files need to have their collection to be found named the same as the collection specified. For example:

- In a material collection that is specified in `app_settings.json` as "Materials", each blender file needs to have a collection named "Materials"

If you wish to change the name of the settings files, then you will need to update them in `main.py`.

**Figma Board:**

https://www.figma.com/file/9Bkj0qB5tsCosPKz8Tawl0/Render-App?type=whiteboard&node-id=0%3A1&t=7nKfHeNIx1pvY9Wy-1

**High Level Design:**
![High Level Design](https://github.com/7kevinr7/render-app/blob/master/design/design_flow.png)
