import os
import json
import IPython
from collections import namedtuple
from operator import attrgetter
from pandas import DataFrame
from ipywidgets import widgets
from ipywidgets import (
    Layout,
    Button,
    VBox,
    HBox,
    Box,
    FloatText,
    Textarea,
    Dropdown,
    Label,
    Tab,
    IntSlider,
    Checkbox,
    Text,
    Button,
    SelectMultiple,
    HTML,
)
from IPython.display import display
from ipywidgets import IntText
from json import dumps as jdump
from sensiml.widgets.base_widget import BaseWidget
from sensiml.widgets.renderers import WidgetAttributeRenderer


category_item_layout = Layout(
    # display='flex',
    size=16,
    # border='solid 2px',
    justify_content="flex-start",
    # background_color= 'red',
    overflow="visible",
)


def clean_name(name):
    return "".join(e if e.isalnum() else "_" for e in name)


class DownloadWidget(BaseWidget):
    def __init__(self, dsk=None, level="Project", folder="knowledgepacks"):
        self._dsk = dsk
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.setup(level=level)

    def setup(self, level):
        self.kb_description = {"parent": {}, "sub": {"Report": "Report"}}

        self.kb_dict = {"parent": [], "sub": []}
        self.level = level

    def select_platform(self, b):
        platform = self._dsk.platforms.get_platform_by_id(self._widget_platform.value)
        supported_source_drivers = platform.supported_source_drivers
        supported_source_keys = {x: x for x in list(supported_source_drivers.keys())}

        capture_configurations = {
            k: v.uuid
            for k, v in self._dsk.project.capture_configurations.build_capture_list().items()
        }

        supported_source_keys.update(capture_configurations)
        supported_source_keys["Custom"] = "Custom"

        default_source_driver = supported_source_drivers.get("Default", None)
        supported_outputs = platform.supported_outputs

        if default_source_driver is not None:
            # Remove the Default option from the list.
            supported_source_keys.pop("Default")

        self._widget_source.options = supported_source_keys
        if len(self._widget_source.options) > 0:
            if capture_configurations:
                self._widget_source.value = next(iter(capture_configurations.items()))[
                    1
                ]
            else:
                self._widget_source.value = "Custom"
        else:
            self._widget_source.options = {"Custom": "Custom"}
            self._widget_source.value = self._widget_source.options[0]
        self._widget_app_outputs.options = supported_outputs
        self._widget_app_outputs.value = supported_outputs
        self._change_rate("value")
        if len(self._widget_source_rate.options) > 0:
            self._widget_source_rate.value = self._widget_source_rate.options[0]
        else:
            self._widget_source_rate.options = [""]
            self._widget_source_rate.value = ""
        self._widget_target_os.options = platform.target_os_options
        self._widget_target_os.value = self._widget_target_os.options[0]

        if platform.can_build_binary:
            self._widget_download_type.options = ["Binary", "Library"]
        else:
            self._widget_download_type.options = ["Library"]
        self._widget_download_type.value = self._widget_download_type.options[0]

    def generate_description(self, b):
        if hasattr(self._dsk, "_auto_sense_ran"):
            if self._dsk._auto_sense_ran:
                self.renderer.render(
                    "KnowledgePack List Needs updating. Updating Now... Reselect and redownload."
                )
                self._refresh_models_list(None)
                self._dsk._auto_sense_ran = False
                return

        platform = self._dsk.platforms.get_platform_by_id(self._widget_platform.value)
        supported_outputs = platform.supported_outputs
        parent_name = None
        parent_uuid = None
        description = {}
        self.set_parent_model(None)
        if not self.kb_description["parent"]:
            self.renderer.render("No Parent Model Selected.")
            return
        for key in self.kb_description["parent"]:
            description = {
                clean_name(key): {
                    "uuid": self.kb_description["parent"][key],
                    "results": {},
                    "source": self._widget_source.value,
                }
            }
            parent_name = clean_name(key)
            parent_uuid = self.kb_description["parent"][key]
        for parent in self.kb_dict["parent"][0][1:]:
            description[parent_name]["results"].update(
                {format(parent.description.split("-")[0]): clean_name(parent.value)}
            )
        for key in self.kb_description["sub"]:
            if key != "Report":
                sub_description = {
                    "uuid": self.kb_description["sub"][key],
                    "parent": parent_name,
                    "segmenter_from": "parent",
                }
                description.update({clean_name(key): sub_description})
        board_name = self._dsk.platforms.get_platform_by_id(
            self._widget_platform.value
        ).board_name

        kp_uuid = parent_uuid
        kp_platform = self._widget_platform.value
        kp_debug = self._widget_debug.value
        kp_test_data = self._widget_test_data.value
        kp_download_type = self._widget_download_type.value

        debug_level = self._widget_debug_level.value
        profile = self._widget_profile.value
        profile_iterations = self._widget_profile_iterations.value

        sample_rate = (
            self._widget_source_rate.value
            if self._widget_source_rate.value in self._widget_source_rate.options
            else 100
        )
        output_options = [x.lower() for x in self._widget_app_outputs.value]

        execution_parameters = platform.execution_parameters

        if "ble" in supported_outputs and "ble" not in output_options:
            output_options.insert("ble")

        kp_application = execution_parameters.get("application", "Default")

        if kp_uuid is not None:
            kp = self._dsk.get_knowledgepack(kp_uuid)
        else:
            return None

        if kp.knowledgepack_description is not None:
            description = kp.knowledgepack_description
            description["Parent"]["source"] = self._widget_source.value

        config = {
            "target_platform": kp_platform,
            "test_data": kp_test_data,
            "debug": kp_debug,
            "application": kp_application,
            "sample_rate": sample_rate,
            "output_options": output_options,
            "kb_description": description,
            "debug_level": debug_level,
            "profile": profile,
            "profile_iterations": profile_iterations,
        }
        print(config)

        self.renderer.render("Generating Knowledge Pack")

        if kp_download_type == "Library":
            save_path, saved = kp.download_library(
                config=config, folder="knowledgepacks", renderer=self.renderer
            )
        if kp_download_type == "Binary":
            save_path, saved = kp.download_binary(
                config=config, folder="knowledgepacks", renderer=self.renderer
            )

    def set_parent_model(self, b):

        if self._widget_parent_select.value is None:
            return

        kp = self._dsk.get_knowledgepack(self._widget_parent_select.value)
        kp_item = []
        kp_item.append(Label(value=kp.name))

        for key, value in kp.class_map.items():
            kp_item.append(
                Dropdown(
                    options=self.kb_description["sub"],
                    description="{} - {}".format(key, value),
                )
            )

        self.kb_description["parent"] = {kp.name: kp.uuid}
        self.kb_dict["parent"] = [kp_item]
        self.update_models()

    def get_kp_dict(self):
        if self.level.lower() == "project":
            kps = self._dsk.project.list_knowledgepacks()
        elif self.level.lower() == "pipeline":
            kps = self._dsk.pipeline.list_knowledgepacks()
        else:
            kps = self._dsk.list_knowledgepacks()

        if isinstance(kps, DataFrame) and len(kps):
            kps = sorted(
                [
                    (name, value)
                    for name, value in kps[["Name", "kp_uuid"]].values
                    if name
                ],
                key=lambda s: s[0].lower(),
            )

            return kps

        return [("", None)]

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    def get_model_list(self):
        return (
            [Label(value="Parent Model")]
            + self.flatten(self.kb_dict["parent"])
            + [Label(value="Sub Model")]
            + self.flatten(self.kb_dict["sub"])
        )

    def get_feature_file_list(self):
        ff = self._dsk.list_featurefiles(silent=True)
        if ff is not None:
            return list(ff["Name"].values)
        else:
            return []

    def get_platform_names(self):
        named_platform = namedtuple("Platform", ["name", "version", "id"])
        platform_list = []
        for platform in self._dsk.platforms.platform_list:
            platform_list.append(
                named_platform(
                    platform.platform, platform.platform_version, platform.id
                )
            )
        platform_list = sorted(platform_list, key=attrgetter("name", "version"))
        ret_dict = {}
        for platform in platform_list:
            ret_dict["{} {}".format(platform.name, platform.version)] = platform.id

        return ret_dict

    def _refresh(self):
        if self._dsk is None:
            return
        self._widget_platform.options = self.get_platform_names()
        # self._widget_platform.value = 10
        self._widget_platform.observe(self.select_platform)
        self.select_platform(None)
        self._widget_test_data.options = [None] + self.get_feature_file_list()
        self._widget_parent_select.options = self.get_kp_dict()
        self._widget_parent_select.value = self._widget_parent_select.options[0][1]
        self._widget_class_map.options = self._get_class_map()

    def _clear(self):
        self._widget_parent_select.options = [""]
        self._widget_parent_select.value = ""
        self._widget_class_map.options = []

    def _update_class_map(self, *args):
        self._widget_class_map.options = self._get_class_map()

    def _get_class_map(self):

        if self._widget_parent_select.value:
            class_map = self._dsk.get_knowledgepack(
                self._widget_parent_select.value
            ).class_map
            return sorted(
                ["{} - {}".format(key, value) for key, value in class_map.items()]
            )
        else:
            return ""

    def _refresh_models_list(self, b):
        if self._dsk:
            if self._dsk.pipeline:
                self._widget_parent_select.options = self.get_kp_dict()
                self._widget_parent_select.value = self._widget_parent_select.options[
                    0
                ][1]
                self._widget_class_map.options = self._get_class_map()

    def update_models(self):
        if self._dsk is None:
            return

        if self.kb_dict["parent"]:
            for output in self.kb_dict["parent"][0][1:]:
                output.options = [k for k, v in self.kb_description["sub"].items()]

    def _change_rate(self, change):
        platform = self._dsk.platforms.get_platform_by_id(self._widget_platform.value)
        supported_source_drivers = platform.supported_source_drivers

        if self._widget_source.value == "Custom":
            self._widget_source_rate.options = [""]
            self._widget_source_rate.value = None
        else:
            self._widget_source_rate.options = supported_source_drivers.get(
                self._widget_source.value, [""]
            )

        if self._widget_source_rate.options[0] == "":
            self._widget_source_rate.layout.visibility = "hidden"
        else:
            self._widget_source_rate.layout.visibility = "visible"

    def create_widget(self):

        info_layout = Layout(width="35px", visibility="visible")

        description_style = {"description_width": "112px"}

        self._info_test_data = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Select a test file to upload. The knowledge pack will replace incoming sensor
                    data with this test data. Allows for validating model performance on the device 
                    with known results. Once the end of the test data is reached, the knowledge pack
                    will start from the start of the test data again.
                    """,
            layout=info_layout,
        )

        self._info_debug = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Enable Debug output over serial. 
                    """,
            layout=info_layout,
        )

        self._info_debug_level = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Debug Level 1: Classification 
                    Debug Level 2: Feature Vector 
                    Debug Level 3: Raw Data Fed into Feature Extractors
                    """,
            layout=info_layout,
        )
        self._info_profile = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Adds profiling to code which will output the MIPS and Average seconds for
                    each feature extractor and classifier.
                    """,
            layout=info_layout,
        )

        self._info_profile_iterations = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    The number of iterations to perform when profiling each feature extrator and classifier.
                    """,
            layout=info_layout,
        )

        self._button_generate = Button(
            icon="download", tooltip="Generate and Download", layout=Layout(width="15%")
        )
        self._button_refresh = Button(
            icon="refresh", layout=Layout(width="15%"), tooltip="Refresh Model List"
        )
        self._widget_platform = Dropdown(description="HW Platform", options=[])
        self._widget_target_os = Dropdown(description="Target OS")
        self._widget_app_outputs = SelectMultiple(description="Output", options=[])
        self._widget_download_type = Dropdown(description="Format", options=[])
        self._widget_source = Dropdown(description="Data Source", options=[])
        self._widget_source_rate = Dropdown(description="Sample Rate", options=[])
        self._widget_debug = Dropdown(
            description="Debug", options=[False, True], style=description_style
        )
        self._widget_debug_level = Dropdown(
            description="Debug Level", options=[1, 2, 3], style=description_style
        )
        self._widget_profile = Dropdown(
            description="Profile", options=[False, True], style=description_style
        )
        self._widget_profile_iterations = IntText(
            description="Profile Iterations", default=1000, style=description_style
        )
        self._widget_test_data = Dropdown(
            description="Test Data", options=[None], style=description_style
        )
        self._widget_parent_select = Dropdown(
            description="Model Name", options=[], layout=Layout(width="85%")
        )
        self._widget_class_map = SelectMultiple(description="Class Map", options=[""])

        self._widget_render_space = HTML()

        self.renderer = WidgetAttributeRenderer(self._widget_render_space, "value")

        self.kb_items = VBox(
            [
                Tab(
                    [
                        VBox(
                            [
                                HBox(
                                    [
                                        self._widget_parent_select,
                                        self._button_refresh,
                                        self._button_generate,
                                    ]
                                ),
                                self._widget_class_map,
                                Label(
                                    value="Target Device Options",
                                    layout=category_item_layout,
                                ),
                                HBox(
                                    [
                                        VBox(
                                            [
                                                self._widget_platform,
                                                self._widget_target_os,
                                                self._widget_download_type,
                                                self._widget_source,
                                                self._widget_source_rate,
                                            ]
                                        ),
                                        self._widget_app_outputs,
                                    ]
                                ),
                            ]
                        ),
                        HBox(
                            [
                                VBox(
                                    [
                                        HBox(
                                            [
                                                self._widget_test_data,
                                                self._info_test_data,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [self._widget_debug, self._info_debug],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [
                                                self._widget_debug_level,
                                                self._info_debug_level,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [self._widget_profile, self._info_profile],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [
                                                self._widget_profile_iterations,
                                                self._info_profile_iterations,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                self._widget_render_space,
            ]
        )

        self.kb_items.children[0].set_title(0, "Main Settings")
        self.kb_items.children[0].set_title(1, "Advanced Settings")

        self._button_generate.on_click(self.generate_description)
        self._button_refresh.on_click(self._refresh_models_list)
        self._widget_source.observe(self._change_rate, names="value")
        self._widget_parent_select.observe(self._update_class_map)

        self._refresh()

        return self.kb_items
