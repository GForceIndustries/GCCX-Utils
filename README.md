# GCCX-Utils
Miscellaneous utilities for Genesys Cloud CX.
## Get GCV DID Assignments

Retrieves the list of phone numbers purchased via Genesys Cloud Voice and for each number assigned to an object, returns the number along with the object it is assigned to. The script will prompt you for your client ID, client secret and region. Region can be specified using the full region string (for example, eu-west-2), or abbreviated (for example, EUW2). The script assumes the Client Credentials grant type.
## Test OAuth Client Authentication

A simple way to sanity check if OAuth client authentication is working. The script will prompt you for your client ID, client secret and region. Region can be specified using the full region string (for example, eu-west-2), or abbreviated (for example, EUW2). The script assumes the Client Credentials grant type but can still validate that the credentials are correct for other grant types.

Successful authentication and correct grant type:

<Response [200]>
{'access_token': 'DCl7jJaGIGQ1M-8dq791twKewbp8bI5Vr1vFV1gRizlxlsH1U4**aA25FG4BqLcjKqcG5AVuzFJ4_g0Q', 'token_type': 'bearer', 'expires_in': 86399}

Successful authentication but incorrect grant type:

<Response [400]>
{'error': 'unauthorized_client', 'description': 'client is not authorized to use the client_credential grant type', 'error_description': 'client is not authorized to use the client_credential grant type'}

Unsuccessful authentication:

<Response [400]>
{'error': 'unauthorized_client', 'description': 'client is not authorized to use the client_credential grant type', 'error_description': 'client is not authorized to use the client_credential grant type'}
