from six import string_types
from sensiml.datamanager.pipeline import PipelineStep


class FunctionCall(PipelineStep):
    """The base class for a function call.

    Child classes have their own additional properties and overwrite this docstring."""

    def __init__(self, name, function_type="transform"):
        super(FunctionCall, self).__init__(name=name, step_type="FunctionCall")
        self._type = function_type

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        self._outputs = outputs

    def _check_inputs(self, output_vars=[]):
        """Compares the list of inputs with the given output_vars list

            Args:
                output_vars (list[str]): the current set of output variables

            Returns:
                unmatched_inputs (list[str]): unmatched inputs or an empty list if all inputs are matched
        """
        unmatched_inputs = []
        for param in [getattr(self, input["name"]) for input in self._input_contract]:
            if (
                isinstance(param, string_types)
                and param.find("temp.") > -1
                and not param in output_vars
            ):
                unmatched_inputs.append(param)
        return unmatched_inputs

    def _public_properties(self):
        """Returns the object's public properties, i.e. those that do not start with _"""
        return (name for name in dir(self) if not name.startswith("_"))

    def _to_dict(self):
        prop_dict = {}
        prop_dict["name"] = self._name
        prop_dict["type"] = self._type
        prop_dict["feature_table"] = self._feature_table
        prop_dict["inputs"] = {}
        for prop in [
            input["name"]
            for input in self._input_contract
            if not input.get("handle_by_set", False)
        ]:
            if prop != "outputs":
                prop_dict["inputs"][prop] = getattr(self, prop)
        prop_dict["outputs"] = getattr(self, "outputs")
        return prop_dict
