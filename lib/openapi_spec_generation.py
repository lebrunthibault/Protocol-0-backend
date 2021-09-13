# Executed with python 2

import inspect
import itertools
import json
import logging
import sys
from typing import Callable, Dict, Iterator

from apispec import APISpec
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_api_specs(title, methods_dict, out_folder, package_name):
    # type: (str, Dict, str) -> None
    methods = [getattr(cls, method_name) for method_name, cls in methods_dict.items()]
    spec = _generate_bare_spec(title=title)

    for method in methods:
        _add_spec_path_from_method(spec=spec, method=method)

    try:
        validate_spec(spec.to_dict())
        logger.info("spec is valid")
    except OpenAPIValidationError as e:
        logger.error(e)
        return

    _write_to_file(folder_name=out_folder, spec=spec, package_name=package_name)


def _generate_bare_spec(title):
    # type: (str) -> APISpec
    return APISpec(
        title=title,
        version="1.0.0",
        openapi_version="3.1.0",
        info=dict(description=title),
    )


def _add_spec_path_from_method(spec, method):
    # type: (APISpec, Callable) -> APISpec

    return spec.path(
        path="/%s" % method.__name__,
        parameters=list(_get_parameters_dict_from_method(method)),
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


def _get_openapi_string_type(obj):
    # noinspection PyUnresolvedReferences
    if sys.version_info.major == 2:
        str_class = basestring  # noqa
    else:
        str_class = str
    if isinstance(obj, str_class):
        return "string"
    if isinstance(obj, bool):
        return "boolean"
    elif isinstance(obj, int):
        return "integer"
    elif isinstance(obj, float):
        return "number"
    elif isinstance(obj, list):
        return "array"
    else:
        return "object"


# noinspection PyUnresolvedReferences
def _get_parameters_dict_from_method(method):
    # type: (Callable) -> Iterator
    if sys.version_info.major == 2:
        inspector = inspect.getargspec
    else:
        inspector = inspect.getfullargspec

    s = inspector(method)
    names = s.args
    if len(names) and names[0] == "self":
        names = names[1:]

    required = object()  # unique object
    total_defaults = [required] * (len(names))
    if s.defaults:
        total_defaults[-len(s.defaults):] = s.defaults

    # noinspection PyUnresolvedReferences
    zipper = zip if sys.version_info.major == 3 else itertools.izip
    # noinspection PyUnresolvedReferences
    for name, default in zipper(names, total_defaults):
        param = {
            "in": "query",
            "name": name,
            "required": default == required,
            "schema": {}
        }
        if default != required:
            param["schema"]["default"] = default
            param["schema"]["type"] = _get_openapi_string_type(default)
        yield param


def _write_to_file(folder_name, spec, package_name):
    # type: (str, APISpec) -> None
    with open("%s/openapi.yaml" % folder_name, "w") as f:
        f.write(spec.to_yaml())
    with open("%s/openapi_config.json" % folder_name, "w") as f:
        f.write(json.dumps({"packageName": package_name}))
    logger.info("wrote spec files %s" % folder_name)
