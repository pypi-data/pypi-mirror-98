# ComboCurve client for Python

## Authorization

`combocurve_api` requires the API key and service account provided by Inside Petroleum, as shown in the example below:

```python
from combocurve_api_v1 import ServiceAccount, ComboCurveAuth

# Use this to create your service account manually
service_account = ServiceAccount(
    client_email='YOUR_CLIENT_EMAIL',
    client_id='YOUR_CLIENT_ID',
    private_key='YOUR_PRIVATE_KEY',
    private_key_id='YOUR_PRIVATE_KEY_id'
)
# Or use this to load it from a JSON file
# service_account = ServiceAccount.from_file("PATH_TO_JSON_FILE")

# Set your API key
api_key = 'YOUR_API_KEY'

combocurve_auth = ComboCurveAuth(service_account, api_key)

# Get auth headers
headers = combocurve_auth.get_auth_headers()
```
