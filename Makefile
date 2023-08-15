test: test_php test_python

test_php:
	@printf "\n\033[92m\033[1mPHP\033[0m\033[0m\n"
	./vendor/bin/phpunit --colors=always --verbose --bootstrap ./tests/php/phpunit.php ./tests/php/

test_python:
	@printf "\n\033[92m\033[1mPYTHON\033[0m\033[0m\n"
	python3 -m unittest discover tests/python/ -p '*_test.py' -v

.PHONY: test test_php test_python
