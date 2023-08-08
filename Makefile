test_php:
	@echo -e "\n\033[92m\033[1mPHP\033[0m\033[0m"
	./vendor/bin/phpunit --colors=always --verbose --bootstrap ./tests/php/phpunit.php ./tests/php/

test_python:
	@echo -e "\n\033[92m\033[1mPYTHON\033[0m\033[0m"
	python3 -m unittest discover tests/python/ -p '*_test.py' -v

test:
	make test_php
	make test_python
