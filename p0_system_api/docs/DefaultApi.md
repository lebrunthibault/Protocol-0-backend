# p0_system_api.DefaultApi

All URIs are relative to *http://127.0.0.1:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate_rev2_editor**](DefaultApi.md#activate_rev2_editor) | **GET** /activate_rev2_editor | Activate Rev2 Editor
[**arrow_down**](DefaultApi.md#arrow_down) | **GET** /arrow_down | Arrow Down
[**arrow_up**](DefaultApi.md#arrow_up) | **GET** /arrow_up | Arrow Up
[**bad_request**](DefaultApi.md#bad_request) | **GET** /bad_request | Bad Request
[**click**](DefaultApi.md#click) | **GET** /click/{x}/{y} | Click
[**double_click**](DefaultApi.md#double_click) | **GET** /double_click/{x}/{y} | Double Click
[**focus_window**](DefaultApi.md#focus_window) | **GET** /focus_window/{window_name} | Focus Window
[**health**](DefaultApi.md#health) | **GET** /health | Health
[**hide_plugins**](DefaultApi.md#hide_plugins) | **GET** /hide_plugins | Hide Plugins
[**index**](DefaultApi.md#index) | **GET** / | Index
[**pixel_has_color**](DefaultApi.md#pixel_has_color) | **GET** /pixel_has_color/{x}/{y}/{color} | Pixel Has Color
[**reload_ableton**](DefaultApi.md#reload_ableton) | **GET** /reload_ableton | Reload Ableton
[**search**](DefaultApi.md#search) | **GET** /search/{search} | Search
[**show_device_view**](DefaultApi.md#show_device_view) | **GET** /show_device_view | Show Device View
[**show_hide_plugins**](DefaultApi.md#show_hide_plugins) | **GET** /show_hide_plugins | Show Hide Plugins
[**show_plugins**](DefaultApi.md#show_plugins) | **GET** /show_plugins | Show Plugins
[**show_windows**](DefaultApi.md#show_windows) | **GET** /show_windows | Show Windows
[**sync_presets**](DefaultApi.md#sync_presets) | **GET** /sync_presets | Sync Presets
[**toggle_ableton_button**](DefaultApi.md#toggle_ableton_button) | **GET** /toggle_ableton_button/{x}/{y}/{activate} | Toggle Ableton Button


# **activate_rev2_editor**
> object activate_rev2_editor()

Activate Rev2 Editor

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Activate Rev2 Editor
        api_response = api_instance.activate_rev2_editor()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->activate_rev2_editor: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrow_down**
> object arrow_down()

Arrow Down

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Arrow Down
        api_response = api_instance.arrow_down()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->arrow_down: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrow_up**
> object arrow_up()

Arrow Up

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Arrow Up
        api_response = api_instance.arrow_up()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->arrow_up: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bad_request**
> object bad_request()

Bad Request

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Bad Request
        api_response = api_instance.bad_request()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->bad_request: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **click**
> object click(x, y)

Click

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    x = 56 # int | 
y = 56 # int | 

    try:
        # Click
        api_response = api_instance.click(x, y)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->click: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x** | **int**|  | 
 **y** | **int**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **double_click**
> object double_click(x, y)

Double Click

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    x = 56 # int | 
y = 56 # int | 

    try:
        # Double Click
        api_response = api_instance.double_click(x, y)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->double_click: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x** | **int**|  | 
 **y** | **int**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **focus_window**
> object focus_window(window_name)

Focus Window

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    window_name = 'window_name_example' # str | 

    try:
        # Focus Window
        api_response = api_instance.focus_window(window_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->focus_window: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **window_name** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health**
> object health()

Health

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Health
        api_response = api_instance.health()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->health: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **hide_plugins**
> object hide_plugins()

Hide Plugins

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Hide Plugins
        api_response = api_instance.hide_plugins()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->hide_plugins: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **index**
> object index()

Index

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Index
        api_response = api_instance.index()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->index: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pixel_has_color**
> bool pixel_has_color(x, y, color)

Pixel Has Color

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    x = 56 # int | 
y = 56 # int | 
color = 'color_example' # str | 

    try:
        # Pixel Has Color
        api_response = api_instance.pixel_has_color(x, y, color)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->pixel_has_color: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x** | **int**|  | 
 **y** | **int**|  | 
 **color** | **str**|  | 

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reload_ableton**
> object reload_ableton()

Reload Ableton

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Reload Ableton
        api_response = api_instance.reload_ableton()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->reload_ableton: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search**
> object search(search)

Search

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    search = 'search_example' # str | 

    try:
        # Search
        api_response = api_instance.search(search)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->search: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **show_device_view**
> object show_device_view()

Show Device View

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Show Device View
        api_response = api_instance.show_device_view()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->show_device_view: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **show_hide_plugins**
> object show_hide_plugins()

Show Hide Plugins

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Show Hide Plugins
        api_response = api_instance.show_hide_plugins()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->show_hide_plugins: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **show_plugins**
> object show_plugins()

Show Plugins

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Show Plugins
        api_response = api_instance.show_plugins()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->show_plugins: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **show_windows**
> object show_windows()

Show Windows

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Show Windows
        api_response = api_instance.show_windows()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->show_windows: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sync_presets**
> str sync_presets()

Sync Presets

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    
    try:
        # Sync Presets
        api_response = api_instance.sync_presets()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->sync_presets: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **toggle_ableton_button**
> object toggle_ableton_button(x, y, activate)

Toggle Ableton Button

### Example

```python
from __future__ import print_function
import time
import p0_system_api
from p0_system_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://127.0.0.1:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = p0_system_api.Configuration(
    host = "http://127.0.0.1:8000"
)


# Enter a context with an instance of the API client
with p0_system_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = p0_system_api.DefaultApi(api_client)
    x = 56 # int | 
y = 56 # int | 
activate = True # bool | 

    try:
        # Toggle Ableton Button
        api_response = api_instance.toggle_ableton_button(x, y, activate)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->toggle_ableton_button: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x** | **int**|  | 
 **y** | **int**|  | 
 **activate** | **bool**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

