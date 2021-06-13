openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy -o api_client -t openapi_templates
if exist "${EGG_FILE}" rm "${EGG_FILE}"
cd api_client && python setup.py install --user
cd ..