import os
from typing import List, Callable

# If no exception is raised by validate_spec(), the spec is valid.
from a_protocol_0.utils.decorators import EXPOSED_METHODS
from openapi_spec_validator import validate_spec

print(EXPOSED_METHODS)

from apispec import APISpec


class OpenApiSpecDescription():
    def __init__(self, title: str, methods: List[Callable], filename: str):
        self.title = title
        self.methods = methods
        self.filename = f"{os.path.dirname(__file__)}/{filename}"


class OpenAPISpec():
    _P0_INTERNAL_API_SPEC_DESCRIPTION = OpenApiSpecDescription(title="P0 Internal API", methods=EXPOSED_METHODS,
                                                               filename="p0_internal_api.yaml")

    def __init__(self, spec_description: OpenApiSpecDescription):
        self.spec_description = spec_description
        self.spec = self._generate_bare_spec()
        for method in self.spec_description.methods:
            self._add_spec_path_from_method(method=method)

        validate_spec(self.spec)

    @staticmethod
    def generate_api_specs():
        OpenAPISpec(spec_description=OpenAPISpec._P0_INTERNAL_API_SPEC_DESCRIPTION)._write_to_file()

    def _generate_bare_spec(self) -> APISpec:
        return APISpec(
            title=self.spec_description.title,
            version="1.0.0",
            openapi_version="3.0.2",
            info=dict(description=self.spec_description.title),
        )

    def _add_spec_path_from_method(self, method: Callable) -> APISpec:
        # signature = inspect.signature(test)
        # print(signature)
        # print(signature.parameters)
        return self.spec.path(
            path=f"/{method.__name__}",
            operations=dict(
                get=dict(
                    responses={
                        "200": {
                            "description": ""
                        }
                    }
                ))
        )

    def _write_to_file(self):
        with open(self.spec_description.filename, "w") as f:
            f.write(self.spec.to_yaml())


if __name__ == "__main__":
    OpenAPISpec.generate_api_specs()
