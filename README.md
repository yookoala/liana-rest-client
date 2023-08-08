# REST Client

REST client in each programming language to use for LianaTech RESTful services.

## Usage

PHP

```php
<?php
require 'php/RestClient.php';
$client = new LianaTech\RestClient(<API_USER>, <API_KEY>, <API_URL>, <API_VERSION>, <REALM>);
try {
	$res = $client->call('pingpong', array('ping' => 'foo'), 'POST');
} catch (LianaTech\RestClientAuthorizationException $e) {
	echo "\n\tERROR: Authorization failed\n\n";
} catch (LianaTech\APIException $e) {
	echo  "\n\nERROR: API exception : " . $e->getMessage() . "\n\n";
} catch (exception $e) {
	echo "\n\tERROR: " . $e->getmessage() . "\n\n";
}
```

Python

```python
import sys
sys.path.append('./python')

from RestClient import RestClient, APIException

api_user = <API_USER_ID>
api_secret = <API_KEY>
api_url = <API_URL>
api_realm = <API_REALM>
api_version = <API_VERSION>

client = RestClient(api_user, api_secret, api_url, api_version, api_realm)

try:
	data = client.call('echoMessage', ['Hello World!'], 'POST')
except APIException as e:
	response = client.get_http_response()
	print('API call failed: '+ str(e))
	print(response.status_code)
	print(response.headers)
	print(response.text)
	exit(1)

print(data)
```

## Development

1. Clone this repository (and go to folder)

2. [Install composer](https://github.com/composer/composer)

3. Install required PHP dependencies (it will read composer.json file)

   `php composer.phar install`

4. Running tasks (currently only unit tests)

   `make test`
