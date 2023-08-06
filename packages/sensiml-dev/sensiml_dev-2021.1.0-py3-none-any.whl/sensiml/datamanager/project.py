import json
import os
import pandas as pd
from pandas import DataFrame
import datetime
from sensiml.datamanager.featurefiles import FeatureFiles
from sensiml.datamanager.captures import Captures
from sensiml.datamanager.knowledgepack import KnowledgePack
from sensiml.datamanager.sandboxes import Sandboxes
from sensiml.datamanager.queries import Queries
from sensiml.method_calls.functioncall import FunctionCall
from sensiml.datamanager.capture_configurations import CaptureConfigurations
import sensiml.base.utility as utility


class Project(object):
    """Base class for a project."""

    _uuid = ""
    _name = ""
    _created_at = None
    _schema = {}
    _settings = {}
    _query_optimized = True

    def __init__(self, connection):
        """Initialize a project instance.

            Args:
                connection (connection object)
        """
        self._connection = connection
        self._feature_files = FeatureFiles(self._connection, self)
        self._captures = Captures(self._connection, self)
        self._sandboxes = Sandboxes(self._connection, self)
        self._queries = Queries(self._connection, self)
        self._plugin_config = None
        self._capture_configurations = CaptureConfigurations(self._connection, self)

    @property
    def uuid(self):
        """Auto generated unique identifier for the project object"""
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self._uuid = value

    @property
    def name(self):
        """Name of the project object"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def created_at(self):
        """Date of the project creation"""
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        if value:
            self._created_at = datetime.datetime.strptime(
                value[:-6], "%Y-%m-%dT%H:%M:%S.%f"
            )

    @property
    def schema(self):
        """Schema of the project object"""
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    @property
    def plugin_config(self):
        """Plugin Config of the project object"""
        return self._plugin_config

    @plugin_config.setter
    def plugin_config(self, value):
        self._plugin_config = value

    @property
    def settings(self):
        """Global settings of the project object"""
        return self._settings

    @property
    def query_optimized(self):
        return self._query_optimized

    def add_segmenter(self, name, segmenter, preprocess=None, custom=False):
        """Saves a segmentation algorithm as the project's global segmentation setting.

            Args:
                name(str): Name to call the segmenter
                segmenter(FunctionCall): segmentation call object that the project will use by default
                preprocess(dict): Segment transforms to perform before segmenter
                custom(bool): a custom segmenter, or one of our server side segmenters


        """
        url = "project/{0}/segmenter/".format(self.uuid)
        if segmenter is not None:
            if not isinstance(segmenter, FunctionCall):
                print("segmenter is not a function call.")
                return
            segmenter_dict = segmenter._to_dict()
            if not segmenter_dict["type"] == "segmenter":
                print("segmenter is not a function call for a segmenter")
                return
            parameters = json.dumps(segmenter_dict)
        else:
            parameters = None

        if not isinstance(custom, bool):
            print("Custom must either be true or false.")
            return

        if preprocess:
            if isinstance(preprocess, dict):
                preprocess = json.dumps(preprocess)

        segmenter_info = {
            "custom": custom,
            "name": str(name),
            "parameters": parameters,
            "preprocess": preprocess,
        }

        request = self._connection.request("post", url, segmenter_info)
        response, err = utility.check_server_response(request)
        if err is False:
            print("Segmenter Uploaded.")
            return response

    def insert(self):
        """Calls the REST API to insert a new object, uses only the name and schema."""
        url = "project/"
        project_info = {
            "name": self.name,
            "capture_sample_schema": self.schema,
            "settings": self.settings,
            "plugin_config": self.plugin_config,
        }
        request = self._connection.request("post", url, project_info)
        response, err = utility.check_server_response(request)
        if err is False:
            self.uuid = response["uuid"]
            self._settings = response["settings"]
            self._query_optimized = response.get("optimized", True)
            self.plugin_config = response["plugin_config"]

    def update(self):
        """Calls the REST API to update the object."""
        url = "project/{0}/".format(self.uuid)
        project_info = {
            "name": self.name,
            "capture_sample_schema": self.schema,
            "settings": self.settings,
            "plugin_config": self.plugin_config,
        }
        request = self._connection.request("patch", url, project_info)
        response, err = utility.check_server_response(request)
        if err is False:
            self.plugin_config = response.get("plugin_config", None)

    def delete(self):
        """Calls the REST API to delete the object."""
        url = "project/{0}/".format(self.uuid)
        request = self._connection.request("delete", url)
        response, err = utility.check_server_response(request)

    def refresh(self):
        """Calls the REST API and self populates from the server."""
        url = "project/{0}/".format(self.uuid)
        request = self._connection.request("get", url)
        response, err = utility.check_server_response(request)
        if err is False:
            self.name = response["name"]
            self.schema = response["capture_sample_schema"]
            self._query_optimized = response.get("optimized", True)
            self.plugin_config = response.get("plugin_config", None)
            self.created_at = response.get("created_at", None)

    def query_optimize(self, force=False):
        self.refresh()
        """Calls the REST API and optimizes or re-optimizes the project for querying."""
        if not self.schema or not len(self._captures.get_captures()):
            print(
                "Cannot query optimize {} until there are uploaded captures.".format(
                    self._name
                )
                + "If data was uploaded, try dsk.project.refresh() followed by dsk.project.query_optimize()."
            )
        elif not self._query_optimized:
            print(
                "{} is not optimized for querying. Optimizing now...".format(self._name)
            )
            self._create_profile()
        elif force:
            print("Re-optimizing {} for querying now...".format(self._name))
            self._delete_profile()
            self._create_profile()

    def _create_profile(self):
        """Calls the REST API and creates a profile for optimized query times."""
        url = "project/{0}/profile/".format(self.uuid)
        request = self._connection.request("post", url)
        response, err = utility.check_server_response(request, is_octet=True)
        self.refresh()

        return response

    def _delete_profile(self):
        """Calls the REST API and drops the project profile."""
        url = "project/{0}/profile/".format(self.uuid)
        # Make a call to delete the profile
        request = self._connection.request("delete", url)
        response, err = utility.check_server_response(request, is_octet=True)
        self.refresh()

        return response

    def get_knowledgepack(self, kp_uuid):
        """Gets the KnowledgePack(s) created by the sandbox.

            Returns:
                a KnowledgePack instance, list of instances, or None
        """
        url = "knowledgepack/{0}/".format(kp_uuid)
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)
        if err is False:
            kp = KnowledgePack(
                self._connection, self.uuid, response_data.get("sandbox_uuid")
            )
            kp.initialize_from_dict(response_data)
            return kp

    def _get_knowledgepacks(self):
        """Gets the KnowledgePack(s) created by the sandbox.

            Returns:
                a KnowledgePack instance, list of instances, or None
        """
        url = "project/{0}/knowledgepack/".format(self.uuid)
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)
        if err is False:
            return DataFrame(response_data)

    def list_knowledgepacks(self):
        """Lists all of the knowledgepacks associated with this project

        Returns:
            DataFrame: knowledpacks on kb cloud
        """

        knowledgepacks = self._get_knowledgepacks().rename(
            columns={
                "name": "Name",
                "project_name": "Project",
                "sandbox_name": "Pipeline",
                "uuid": "kp_uuid",
                "created_at": "Created",
                "knowledgepack_description": "kp_description",
            }
        )

        if len(knowledgepacks) < 1:
            print("No Knowledgepacks stored for this project on the cloud.")
            return None
        return knowledgepacks[knowledgepacks["Name"] != ""][
            ["Name", "Created", "Project", "Pipeline", "kp_uuid", "kp_description"]
        ]

    def initialize_from_dict(self, dict):
        """Reads a json dict and populates a single project.

            Args:
                dict (dict): contains the project's 'name', 'uuid', 'schema', and 'settings' properties
        """
        self.uuid = dict["uuid"]
        self.name = dict["name"]
        self.schema = dict["capture_sample_schema"]
        self._settings = dict.get("settings", [])
        self._query_optimized = dict.get("optimized", True)
        self.plugin_config = dict.get("plugin_config", None)
        self.created_at = dict.get("created_at", None)

    def __getitem__(self, key):
        if type(key) is str:
            return self.captures.get_capture_by_filename(key)
        else:
            return self.captures.get_captures()[key]

    @property
    def featurefiles(self):
        return self._feature_files

    @property
    def captures(self):
        return self._captures

    @property
    def sandboxes(self):
        return self._sandboxes

    @property
    def queries(self):
        return self._queries

    @property
    def capture_configurations(self):
        return self._capture_configurations

    def columns(self):
        """Returns the sensor columns available in the project.

            Returns:
                columns (list[str]): a list of string names of the project's sensor columns
        """
        try:
            columnnames = self.schema.keys()
            return columnnames
        except:
            return None

    def metadata_columns(self):
        """Returns the metadata columns available in the project.

            Returns:
                columns (list[str]): a list of string names of the project's metadata columns
        """
        return self.captures.get_metadata_names()

    def metadata_values(self):
        return self.captures.get_metadata_names_and_values()

    def label_values(self):
        return self.captures.get_label_names_and_values()

    def label_columns(self):
        """Returns the label columns available in the project.

            Returns:
                columns (list[str]): a list of string names of the project's metadata columns
        """
        return self.captures.get_label_names()

    def statistics(self):
        """Gets all capture statistics for the project.

            Returns:
                DataFrame of capture statistics
        """
        url = "project/{0}/statistics/".format(self.uuid)
        data = {"events": False}
        response = self._connection.request("get", url, json=data)
        response_data, err = utility.check_server_response(response)
        if err is False:
            data, error_report = utility.make_statistics_table(response_data)
            return data, error_report
        else:
            return None

    def get_active_pipelines(self):
        url = "project/{0}/active/".format(self.uuid)
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)
        if err is False:
            if response_data:
                return response_data

        return None

    def get_segmenters(self):
        url = "project/{0}/segmenter/".format(self.uuid)
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)
        if err is False:
            if response_data:
                return DataFrame(response_data).set_index("id")

        return None

    def get_project_summary(self):
        url = "project/{0}/capture-stats/".format(self.uuid)
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)
        if err is False:
            if response_data:
                return DataFrame(response_data)

        return None
