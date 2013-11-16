<?php

require 'RestClient.php';

class Mockup_RestClient extends RestClient {
	public function sign(array $msg) {
		return parent::sign($msg);
	} 
}

class RestClientTest extends PHPUnit_Framework_TestCase {
	public function testSign() {
		$obj = new Mockup_RestClient('99999', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'http://mailer.localdomain', '0');
		$hmac = $obj->sign(array('foo', 'bar'));
		$this->assertEquals($hmac, 'c82dbf3d9574513a27f6b70cd007d16fa21686b377a9c3818f005b3af32cd04f', 'message signing');

	}
}
