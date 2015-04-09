module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		concat: {
			options: {
				stripBanners: true,
				
				// Replace all 'use strict' statements in the code with a single one at the top
				banner: "'use strict';\n",
				
				process: function(src, filepath) {
					return '\n// Source: ' + filepath + '\n' +
					src.replace(/(^|\n)[ \t]*('use strict'|"use strict");?\s*/g, '$1');
				}
			},
			dist: {
				src: [
					'app/bower_components/jquery/dist/jquery.js',
					'app/bower_components/bootstrap/dist/js/bootstrap.js',
					'app/bower_components/angular/angular.js',
					'app/bower_components/angular-route/angular-route.js',
					'app/bower_components/angularjs-ordinal-filter/ordinal.js',
					'app/bower_components/angular-animate/angular-animate.js',
					'app/bower_components/angular-loading-bar/build/loading-bar.js',
					
					'app/app.js',
					'app/athlete/*.js',
					'app/home/*.js',
					'app/navigation/*.js',
					'app/shared/*.js',
					'app/week/*.js',

					'!app/**/*_test.js'

				],
				dest: 'dist/built.js',
			},
		},

		uglify: {
			options: {
				banner: '/*! Fitness Evaluation <%= grunt.template.today("yyyy-mm-dd") %> */\n',
				mangle: false
			},
			dist: {
				files: {
					'dist/built.min.js': ['<%= concat.dist.dest %>']
				}
			}
		},

		watch: {
			scripts: {
				files: ['Gruntfile.js', 'app/**/*.js', 'templates/**/*.html'],
				tasks: ['concat'],
				options: {
					livereload: true
				}
			},
		},
	});

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-newer');

	// grunt.event.on('watch', function(action, filepath, target) {
	// 	grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
	// });

	// Default task(s).
	grunt.registerTask('default', ['concat', 'uglify']);

};