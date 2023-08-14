<?php

class Mockup_RestClient extends LianaTech\RestClient {
	public function sign(array $msg) {
		return parent::sign($msg);
	}
}

class RestClientTest extends \PHPUnit\Framework\TestCase {
	public function testSign() {
		$obj = new Mockup_RestClient('99999', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'http://mailer.localdomain', '1', 'BTLM');
		$hmac = $obj->sign(array('foo', 'bar'));
		$this->assertEquals($hmac, 'c82dbf3d9574513a27f6b70cd007d16fa21686b377a9c3818f005b3af32cd04f', 'message signing');
	}
}
