Blockchain Python SDK/Module

Python client library to use the IBM Cloud Blockchain **Service**.

**This module will allow you to use native py functions to leverage the same functionality seen in the [IBP APIs](https://cloud.ibm.com/apidocs/blockchain)**

## Table of Contents

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Explore the SDK](#explore-the-sdk)
* [Using the SDK](#using-the-sdk)
  * [Constructing service clients](#constructing-service-clients)
  * [Authentication](#authentication)
  * [Receiving operation responses](#receiving-operation-responses)
  * [Error Handling](#error-handling)
* [Generation](#generation)
* [License](#license)

## Overview

The IBM Cloud Blockchain Python SDK allows developers to programmatically interact with the
IBM Cloud Blockchain service.

This repository is generated from an OpenAPI file that describes all available APIs.
It is recommended to read through the [IBP API docs](https://cloud.ibm.com/apidocs/blockchain#sdk) to see the list of capabilities.
Any issues with this SDK can be opened here or against the IBM Blockchain Platform service through IBM Cloud support.

## Prerequisites

[ibm-cloud-onboarding]: https://cloud.ibm.com/registration

* An [IBM Cloud][ibm-cloud-onboarding] account.
* An [IBM Blockchain Platform Service instance](https://cloud.ibm.com/catalog/services/blockchain-platform)
* An IAM API key to allow the SDK to access your service instance. Create an account level api key [here](https://cloud.ibm.com/iam/apikeys) (alternatively you can create a service instance level api key from the IBM cloud UI).
* An installation of Python (version 3) on your local machine.

## Installation
Use this command to download and install the Blockchain Python SDK project.
Once this is done your Python application will be able to use it:
```
pip install --upgrade ibm_cloud_sdk_core
pip install --upgrade ibp-python-sdk
```

## Explore the SDK
This module is generated from an OpenAPI (swagger) file.
The same file populated our [IBP APIs documentation](https://cloud.ibm.com/apidocs/blockchain#sdk).
To find desired functionality start by browsing the [IBP APIs documentation](https://cloud.ibm.com/apidocs/blockchain#introduction).
Then find the corresponding python example to the right of the api documentation.

Alternatively you could manually browse the SDK's main file:

- [ibm_cloud/blockchain_v3.py](./ibm_cloud/blockchain_v3.py).

## Using the SDK
This section provides general information on how to use the services contained in this SDK.

### Constructing service clients
Start by requiring the IBP Python SDK and then creating a `client`.
Here's an example of how to construct an instance:

```py
from ibp_python_sdk import BlockchainV3, IAMAuthenticator, ApiException

# create an authenticator - see more examples below
authenticator = IAMAuthenticator(
    apikey='{API-Key}',
)

# Create client from the "BlockchainV3" class
client = BlockchainV3(authenticator=authenticator)
client.set_service_url('https://{API-Endpoint}')


# Service operations can now be called using the "client" variable.

```

### Authentication
Blockchain services use token-based Identity and Access Management (IAM) authentication.

IAM authentication uses an API key to obtain an access token, which is then used to authenticate
each API request. Access tokens are valid for a limited amount of time and must be regenerated.

To provide credentials to the SDK, you supply either an IAM service **API key** or an **access token**:

- Specify the IAM API key to have the SDK manage the lifecycle of the access token.
The SDK requests an access token, ensures that the access token is valid, and refreshes it when
necessary.
- Specify the access token if you want to manage the lifecycle yourself.
For details, see [Authenticating with IAM tokens](https://cloud.ibm.com/docs/services/watson/getting-started-iam.html).

##### Examples:
* Supplying the IAM API key and letting the SDK manage the access token for you:

```py
# Example - letting the SDK manage the IAM access token

# imports
from ibp_python_sdk import BlockchainV3, IAMAuthenticator, ApiException

# Create an authenticator
authenticator = IAMAuthenticator(
	apikey='{API-Key}'
)

# Create client from the "BlockchainV3" class
client = BlockchainV3(authenticator=authenticator)
client.set_service_url('https://{API-Endpoint}')
```

* Supplying the access token (a bearer token) and managing it yourself:

```py
# Example - manage the IAM access token myself

# imports
from ibp_python_sdk import BlockchainV3, IAMAuthenticator, ApiException

# Create an authenticator
authenticator = IAMAuthenticator(
	bearertoken: '{my IAM access token}'
)

# Create client from the "BlockchainV3" class
client = BlockchainV3(authenticator=authenticator)
client.set_service_url('https://{API-Endpoint}')

...

# Later when the access token expires, the application must refresh the access token,
# then set the new access token on the authenticator.
# Subsequent request invocations will include the new access token.
authenticator.bearertoken = # new access token 
```

For more information on authentication, including the full set of authentication schemes supported by
the underlying Python Core library, see
[this page](https://github.com/IBM/python-sdk-core/blob/master/Authentication.md).

### Receiving operation responses
Each service method (operation) will return the following values:
* `response.result` - An operation-specific result (if the operation is defined as returning a result).
* `response.status_code` - the HTTP status code returned in the response message
* `response.headers` - the HTTP headers returned in the response message

##### Example:
1. Here's an example of calling the `GetComponent` operation:
```py
# Create an authenticator
authenticator = IAMAuthenticator(
    apikey: '{API-Key}',
)

# Create client from the "BlockchainV3" class
client = BlockchainV3(authenticator=authenticator)
client.set_service_url('https://{API-Endpoint}')

# Get data for component
try:
    response = client.get_component(id='{Component-ID}')
    print(f'Server status code: {response.status_code}')
    print(f'response:\n {response.result}')
    # handle good response here
except ApiException as e:
    print(f'error status code: {e.code}')
    print(f'error response: {e.message}')
    # handle error here
```

### Error Handling

In the case of an error response from the server endpoint, the Blockchain Python SDK will do the following:
1. The service method (operation) will throw an `ApiException` error.  This `e` object will
contain the error message retrieved from the HTTP response if possible, or a generic error message
otherwise.
2. The `e.message` field will contain the (response if the operation returned a response).
3. The `e.code` field will contain the HTTP response code.


## Generation
This is a note for developers of this repository on how to rebuild the SDK.
- this module was generated/built via the [IBM Cloud OpenAPI SDK generator](https://github.ibm.com/CloudEngineering/openapi-sdkgen)
    - [SDK generator overview](https://github.ibm.com/CloudEngineering/openapi-sdkgen/wiki/SDK-Gen-Overview)
    - [Configuration option code](https://github.ibm.com/CloudEngineering/openapi-sdkgen/blob/ab7d50a1dcdc707faad8cbe4f86de2d2ca510d24/src/main/java/com/ibm/sdk/codegen/IBMDefaultCodegen.java)
    - [IBP's OpenAPI source](https://github.ibm.com/cloud-api-docs/ibp/blob/master/ibp.yaml)
1. download the  latest sdk generator **release** (should see the java file `lib/openapi-sdkgen.jar`)
1. clone/download the IBP OpenAPI file
1. build command w/o shell:
```
cd code/openapi-sdkgen
java -jar C:/code/openapi-sdkgen/lib/openapi-sdkgen-3.19.0.jar generate -g ibm-python --additional-properties initialize=true -i C:/code/cloud-api-docs/ibp.yaml -o C:/code/openapi-sdkgen/node_build --apiref C:/code/cloud-api-docs/apiref-python.json && cp -r C:/code/openapi-sdkgen/node_build/blockchain C:/code/ibp-python-sdk && cp -r C:/code/openapi-sdkgen/node_build/test C:/code/ibp-python-sdk
// inspect the output files in make a PR to this repo if they look okay
```

## License

The IBM Cloud Blockchain Python SDK is released under the Apache 2.0 license. The license's full text can be found in [LICENSE](LICENSE).
