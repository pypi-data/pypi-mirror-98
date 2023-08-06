import json
import datetime
from pandas import DataFrame
import re
import warnings

import sensiml.base.utility as utility


class QueryColumns(object):
    """Base class for the query columns and metadata_columns properties"""

    def __init__(self, columns=[]):
        if len(columns) > 0:
            self._columns = columns
        else:
            self._columns = []

    def add(self, *items):
        """Adds a column name or names for query selection.

            Args:
                items (str or list[str]): column names to add

            Note:
                The named column(s) must exist in the project and duplicate column names will be ignored
        """
        for item in items:
            if item not in self._columns:
                self._columns.append(item)

    def remove(self, item):
        """Removes a column name from query selection.

            Args:
                item (str): column name to remove
        """
        if item in self._columns:
            self._columns.remove(item)

    def clear(self):
        """Clears all column names from query selection"""
        self._columns = []

    def __str__(self):
        return json.dumps(self._columns)


class Query(object):
    """Base class for a query.

    Queries extract project data, or a subset of project data, for use in a pipeline. The query must specify which
    columns of data to extract and what filter conditions to apply, and KnowledgeBuilder takes care of the database
    joins required to produce a clean, analysis-ready data frame.
    """

    def __init__(self, connection, project):
        """Initializes a query instance"""
        self._uuid = ""
        self._name = ""
        self._columns = QueryColumns()
        self._metadata_columns = QueryColumns()
        self._metadata_filter = ""
        self._segmenter = None
        self._label_column = ""
        self._combine_labels = None
        self._dirty = False
        self._capture_configurations = ""
        self._connection = connection
        self._project = project
        self._created_at = None

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self._uuid = value

    @property
    def name(self):
        """Name of the query"""
        return self._name

    @name.setter
    def name(self, value):
        self._dirty = True
        self._name = value

    @property
    def columns(self):
        """Sensor columns to include in the query result

        Note:
            Columns must correspond to actual project sensor columns or the reserved word 'SequenceID' for the
            original sample index.
        """
        self._dirty = True
        return self._columns

    @property
    def created_at(self):
        """Date of the Pipeline creation"""
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = datetime.datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")

    @property
    def label_column(self):
        """Label columns to use in the query result

        Note:
            Columns must correspond to actual project label column"""

        self._dirty = True
        return self._label_column

    @label_column.setter
    def label_column(self, value):
        self._dirty = True
        self._label_column = value

    @property
    def combine_labels(self):
        """Combine label values into new value to use in the query result

        Label = Gesture
        Label_Values = A,B,C,D,E
        combine_labels = {'Group1':['A','B',C'],'Group2':['D','E']}

        the labels that will be returned will be group1 and group2
        """

        self._dirty = True
        return self._combine_labels

    @combine_labels.setter
    def combine_labels(self, value):
        self._dirty = True
        self._combine_labels = value

    @property
    def metadata_columns(self):
        """Metadata columns to include in the query result

        Note:
            Columns must correspond to actual project metadata columns.
        """
        self._dirty = True
        return self._metadata_columns

    @property
    def metadata_filter(self):
        """Filter criteria of the query

        Args:
            value (str): similar to a SQL WHERE clause, the string can contain any number of AND-concatenated
              expressions where square brackets surround the column name and comparison value, with the operator in
              between. Supported operators: >, >=, <, <=, =, !=, IN

        Examples::

            metadata_filter = '[Subject] > [5] AND [Subject] <= [15]'
            metadata_filter = '[Gender] = [Female] AND [Activity] != [Walking]'
            metadata_filter = '[Subject] IN [5, 7, 9, 11, 13, 15]'

        Note:
            Queries do not support OR-concatenation between expressions, but often the IN operator can be used to
            achieve OR-like functionality on a single column. For example::

                [Gesture] IN [A, M, L]

            is equivalent to::

                [Gesture] = [A] OR [Gesture] = [M] OR [Gesture] = [L]

        """
        return self._metadata_filter

    @metadata_filter.setter
    def metadata_filter(self, value):
        self._dirty = True
        self._metadata_filter = value

    @property
    def capture_configurations(self):
        return self._capture_configurations

    @capture_configurations.setter
    def capture_configurations(self, value):
        self._dirty = True

        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list):
            raise Exception("capture_configurations must be List or String")

        self._capture_configurations = json.dumps(value)

    @property
    def segmenter(self):
        """Segmenter to use for the query

        Args:
            value (int): ID of segmenter.

        """
        return self._segmenter

    @segmenter.setter
    def segmenter(self, value):
        if value is None or isinstance(value, int):
            self._segmenter = value
        else:
            raise ValueError("Value must be a integer")

    def insert(self, renderer=None):
        """Calls the REST API and inserts a new query."""

        url = "project/{0}/query/".format(self._project.uuid)

        data = {
            "name": self.name,
            "columns": self.columns._columns,
            "metadata_columns": self.metadata_columns._columns,
            "metadata_filter": self.metadata_filter,
            "segmenter_id": self._segmenter,
            "label_column": self.label_column,
            "combine_labels": self.combine_labels,
            "capture_configurations": self.capture_configurations,
        }

        request = self._connection.request("post", url, data)
        response, err = utility.check_server_response(request, renderer=renderer)
        if err is False:
            self.uuid = response["uuid"]
            self._dirty = False

    def update(self, renderer=None):
        """Calls the REST API and updates the query object on the server."""

        url = "project/{0}/query/{1}/".format(self._project.uuid, self.uuid)

        self._checked = None
        data = {
            "name": self.name,
            "columns": self.columns._columns,
            "metadata_columns": self.metadata_columns._columns,
            "metadata_filter": self.metadata_filter,
            "segmenter_id": self._segmenter,
            "label_column": self.label_column,
            "combine_labels": self.combine_labels,
            "capture_configurations": self.capture_configurations,
        }

        if len(data["columns"]) > 0 or len(data["metadata_columns"]) > 0:
            filters = (
                self._metadata_filter.split("AND")
                if len(self._metadata_filter) > 0
                else []
            )

            for i, filter in enumerate([filter for filter in filters if len(filters)]):
                match = re.search(
                    "\[(?P<key>[0-9A-Za-z_\-\. \)\(]+)\]([ ]*(?P<symbol>[\>\=|\<\=|\=|\<\>|\>|\<|in|IN|!=]+)[ ]*\[(?P<value>.+)\])?",
                    str(filter),
                )
                if not match:
                    self._checked = 1
            if self._checked is None:
                request = self._connection.request("put", url, data)
                response, err = utility.check_server_response(
                    request, renderer=renderer
                )
            else:
                self._metadata_filter = ""
                print("Metadata Filter is not formatted correctly!")
        else:
            print(
                "Sensor columns and, or metadata columns must be specified in order to query!"
            )

    def delete(self, renderer=None):
        """Calls the REST API and deletes the query object from the server."""
        url = "project/{0}/query/{1}/".format(self._project.uuid, self.uuid)
        request = self._connection.request("delete", url)
        response, err = utility.check_server_response(request, renderer=renderer)
        self._dirty = False
        if err is False:
            print(response["result"])

    def statistics_segments(self, renderer=None):
        """Returns metadata statistics for the query."""

        url = "project/{0}/query/{1}/statistics/".format(self._project.uuid, self.uuid)
        request = self._connection.request("get", url)
        response_data, err = utility.check_server_response(request, renderer=renderer)
        if err is False:
            return DataFrame(response_data)
        else:
            return None

    def statistics(self, renderer=None):
        """Returns metadata statistics for the query."""
        if self._dirty:
            self.update(renderer=renderer)

        url = "project/{0}/query/{1}/statistics/".format(self._project.uuid, self.uuid)
        request = self._connection.request("get", url)
        response_data, err = utility.check_server_response(request, renderer=renderer)
        if err is False:
            df = DataFrame(response_data)
            df.drop("Segment Length", axis=1, inplace=True)
            data = (
                df.groupby(
                    ["Capture"] + self.metadata_columns._columns + [self.label_column]
                )[self.label_column]
                .size()
                .unstack(fill_value=0)
            )

            return data
        else:
            return None

    def plot_statistics(self, renderer=None, **kwargs):
        """ Generates a bar plot of the query statistics """
        data = self.statistics(renderer=renderer)
        if data is not None:
            data.sum().plot(kind="bar", **kwargs)

    def data(self):
        """Calls the REST API for query execution and returns the result.

        Note:
            Intended for previewing the query result before creating a query call object and using it in a sandbox
            step. The resulting DataFrame is not cached on the server, but once it is used in a sandbox it may be
            cached.
        """
        warnings.warn("This call has a timeout of two minutes.")

        if self._dirty:
            self.update()

        url = "project/{0}/query/{1}/data/".format(self._project.uuid, self.uuid)
        request = self._connection.request("get", url)
        response_data, err = utility.check_server_response(request)
        if err is False:
            error_report = None
            if not isinstance(response_data, list):
                data = DataFrame(response_data)
            else:
                try:
                    data = DataFrame(response_data[0])
                    error_report = response_data[1]
                except:
                    data = DataFrame(response_data)

            # Post-processing to get numeric index
            data["sample"] = data.index.astype(int)
            data = data.set_index("sample")
            data.index.names = [None]
            data = data.sort_index(axis=0)
            cols = data.columns.tolist()
            if "id" in cols:
                data = data[["id"] + [c for c in cols if c != "id"]]

            return data.sort_index(axis=0), error_report
        else:
            return None

    def size(self):
        """Returns the size of the dataframe which would result from the query."""
        # Sync the client-side query with server-side query object before we check the size
        if self._dirty:
            self.update()

        url = "project/{0}/query/{1}/size/".format(self._project.uuid, self.uuid)
        request = self._connection.request("get", url)
        response_data, err = utility.check_server_response(request)
        if not err:
            query_result = response_data
        else:
            query_result = None
        return query_result

    def refresh(self):
        """Calls the REST API and self populate using the uuid."""
        url = "project/{0}/query/{1}/".format(self._project.uuid, self.uuid)
        request = self._connection.request("get", url)
        response, err = utility.check_server_response(request)

        if err is False:
            self.uuid = response["uuid"]
            self.name = response["name"]
            self._columns = QueryColumns(response["columns"])
            self._label_column = response["label_column"]
            self._metadata_columns = QueryColumns(response["metadata_columns"])
            self.metadata_filter = response["metadata_filter"]
            self.segmenter = response["segmenter_id"]
            self.combine_labels = response["combine_labels"]
            self.capture_configurations = response["capture_configurations"]
            self._dirty = False

    def initialize_from_dict(self, data):
        """Reads a json dict and populates a single query."""
        self.uuid = data["uuid"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self._columns = QueryColumns(data["columns"])
        self._metadata_columns = QueryColumns(data["metadata_columns"])
        self.metadata_filter = data["metadata_filter"]
        self.label_column = data.get("label_column", "")
        self.segmenter = data.get("segmenter_id", None)
        self.combine_labels = data.get("combine_labels", None)
        self.capture_configurations = data.get("capture_configurations", "")

        self._dirty = False

    def post_feature_statistics(self, window_size=None):
        """Returns metadata statistics for the query."""
        data = {"window_size": window_size}
        url = "project/{0}/query/{1}/featurestatistics/".format(
            self._project.uuid, self._uuid
        )
        response = self._connection.request("post", url, data)

        response_data, err = utility.check_server_response(response)

        if err is False:
            return response_data

    def get_feature_statistics(self):
        """Returns metadata statistics for the query."""
        url = "project/{0}/query/{1}/featurestatistics/".format(
            self._project.uuid, self._uuid
        )
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)

        if err is False:
            return response_data

    def __str__(self):
        return (
            "NAME: {0}\n"
            "COLUMNS: {1}\n"
            "METADATA_COLUMNS: {2}\n"
            "METADATA FILTER: {3}\n"
            "SEGMENTER ID: {4}\n"
            "LABEL COLUMN {5}\n"
            "COMBINE LABELS {6}\n"
            "CAPTURE CONFIGURATIONS {7}"
        ).format(
            self.name,
            self.columns,
            self.metadata_columns,
            self.metadata_filter,
            self.segmenter,
            self.label_column,
            self.combine_labels,
            self.capture_configurations,
        )

    def _to_dict(self):
        return {
            "name": self.name,
            "sensor_columns": self.columns._columns,
            "metadata_columns": self.metadata_columns._columns,
            "metadata_filter": self.metadata_filter,
            "segmenter_id": self.segmenter,
            "label_column": self.label_column,
            "capture_configurations": self.capture_configurations,
        }
