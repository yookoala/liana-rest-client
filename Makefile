test:
	@echo "\nPHP"
	./vendor/bin/phpunit --colors --bootstrap ./tests/php/phpunit.php ./tests/php/

	@echo "\nPYTHON"
	python3 -m unittest discover tests/python/ -p '*_test.py'
