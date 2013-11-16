module.exports = function(grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		phpunit: {
			classes: {
				dir: 'tests/php/'
			},
			options: {
				bin: 'vendor/bin/phpunit',
				bootstrap: 'tests/php/phpunit.php',
				colors: true
			}
		}
	});
	
	grunt.loadNpmTasks('grunt-phpunit');
	
	grunt.registerTask('default', ['phpunit']);
};
