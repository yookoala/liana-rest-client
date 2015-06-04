REST Client
===========

REST client in each programming language to use for LianaTech RESTful services.

Usage
=====

PHP

	<?php
	require 'php/RestClient.php';
	$client = new LianaTech\RestClient(<API_USER>, <API_KEY>, <API_URL>, <API_VERSION>, <REALM>);
	try {
		$res = $client->call('pingpong', array('ping' => 'foo'));
	} catch (LianaTech\RestClientAuthorizationException $e) {
		echo "\n\tERROR: Authorization failed\n\n";
	} catch (exception $e) {
		echo "\n\tERROR: " . $e->getmessage() . "\n\n";
	}


Development
===========

Project is using NodeJS and Grunt for simplifying development tasks.

1. Install [NodeJS](http://nodejs.org/)

2. Clone this repository (and go to folder)

3. [Install composer](https://github.com/composer/composer)

4. Install required PHP dependencies (it will read composer.json file)

	php composer.phar install

5. Install required NodeJS plugins (it will read package.json file)

	npm install

6. Running tasks (currently only unit tests) just execute grunt

	grunt


