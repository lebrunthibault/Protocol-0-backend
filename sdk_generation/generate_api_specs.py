import inspect
import itertools
import json
import os
from enum import Enum
from typing import Callable, List, Dict

from apispec import APISpec
from loguru import logger
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError
from protocol0.utils.decorators import EXPOSED_P0_METHODS


class ApiEnum(Enum):
    @property
    def title(self):
        # type: () -> str
        return " ".join(word.title() for word in self.name.split("_")) + " API"

    @property
    def methods(self):
        # type: () -> List[Callable]
        return [getattr(cls, method_name) for method_name, cls in self.value.items()]

    P0_SCRIPT = EXPOSED_P0_METHODS


class OpenAPISpec():
    def __init__(self, apiEnum):
        # type: (ApiEnum) -> None
        self.folder_name = apiEnum.name.lower()
        self.spec = self._generate_bare_spec(title=apiEnum.title)

        for method in apiEnum.methods:
            self._add_spec_path_from_method(method=method)

        try:
            validate_spec(self.spec.to_dict())
            logger.info("spec is valid")
        except OpenAPIValidationError as e:
            logger.error(e)
            return

    @staticmethod
    def get_openapi_string_type(obj):
        # noinspection PyUnresolvedReferences
        if isinstance(obj, basestring):
            return "string"
        elif isinstance(obj, int):
            return "integer"
        elif isinstance(obj, float):
            return "number"
        elif isinstance(obj, list):
            return "array"
        else:
            return "object"

    @staticmethod
    def generate_api_specs():
        for apiEnum in ApiEnum:
            OpenAPISpec(apiEnum=apiEnum)._write_to_file()

    @staticmethod
    def _generate_bare_spec(title):
        # type: (str) -> APISpec
        return APISpec(
            title=title,
            version="1.0.0",
            openapi_version="3.0.2",
            info=dict(description=title),
        )

    def _add_spec_path_from_method(self, method):
        # type: (Callable) -> APISpec

        return self.spec.path(
            path="/%s" % method.__name__,
            parameters=list(self._get_parameters_dict_from_method(method)),
            operations={
                "get": {
                    "operationId": method.__name__,
                    "responses": {
                        "200": {
                            "description": ""
                        }
                    }
                }
            }
        )

    def _get_parameters_dict_from_method(self, method):
        s = inspect.getargspec(method)
        names = s.args
        if len(names) and names[0] == "self":
            names = names[1:]

        required = object()  # unique object
        total_defaults = [required] * (len(names))
        if s.defaults:
            total_defaults[-len(s.defaults):] = s.defaults

        for name, default in itertools.izip(names, total_defaults):
            param = {
                "in": "query",
                "name": name,
                "required": default == required,
                "schema": {}
            }
            if default != required:
                param["schema"]["default"] = default
                param["schema"]["type"] = self.get_openapi_string_type(default)
            yield param

    def _get_dict_from_signature_parameter(self, required, arg):
        # type: (bool, str) -> Dict
        return {
            "required": required,
            "name": arg,
            "in": "query",
            "schema": {}
        }

    def _write_to_file(self):
        folder_name = "%s/%s" % (os.path.dirname(__file__), self.folder_name)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        with open("%s/openapi.yaml" % folder_name, "w") as f:
            f.write(self.spec.to_yaml())
        with open("%s/openapi_config.json" % folder_name, "w") as f:
            f.write(json.dumps({"packageName": "%s_api" % self.folder_name}))
        logger.info("wrote spec files %s" % folder_name)


if __name__ == "__main__":
    OpenAPISpec.generate_api_specs()
