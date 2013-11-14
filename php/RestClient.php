<?php

require_once 'Conf.php';
require_once 'config.php';

/**
 * RestClient
 * Example:
 * $client = new RestCLient(...);
 */
class RestClient
{

	protected $api_key;
	protected $api_user;
	protected $api_url;
	protected $api_version;

	static protected $instance = null;

	public function __construct($api_user, $api_key, $api_url, $api_version) {
		$this->api_user = $api_user;
		$this->api_key = $api_key;
		$this->api_url = $api_url;
		$this->api_version = $api_version;
	}

	public function call($method, $args = array()) {
		return $this->request($method, $args);
	}

	protected function sign($message) {
		return hash_hmac('sha256', implode("\n", $message), $this->api_key);
	}

	protected function request($method, $args = array()) {
		$contents = json_encode($args);
		$md5 = md5($contents);
		$timestamp = date('c');
		$type = empty($args) ? 'GET' : 'POST';
		$url = $this->api_url . '/rest/v'. $this->api_version .'/' . $method;

		$message = array(
			$type,
			$md5,
			'application/json',
			$timestamp,
			$contents,
			'/rest/v'. $this->api_version .'/' . $method
		);

		$signature = $this->sign($message);
		$user_id = $this->api_user;

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
			'Content-Type: application/json',
			"Content-MD5: {$md5}",
			"Date: {$timestamp}",
			"Authorization: LMUI {$user_id}:{$signature}"
		));
		curl_setopt($ch, CURLOPT_USERAGENT, 'PHP-LMAPI');
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_TIMEOUT, 10);
		curl_setopt($ch, CURLOPT_POST, $type == 'POST');
		curl_setopt($ch, CURLOPT_POSTFIELDS, $contents);
		$result = curl_exec($ch);
		curl_close($ch);

		return $result ? json_decode($result, true) : false;
	}

}