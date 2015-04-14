module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		app: 'app',
		dist: 'dist',

		js_build_path: '<%= dist %>/js',
		css_build_path: '<%= dist %>/css',
		bower: '<%= app %>/bower_components',

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
			js: {
				src: [
					'<%= bower %>/jquery/dist/jquery.js',
					'<%= bower %>/bootstrap/dist/js/bootstrap.js',
					'<%= bower %>/angular/angular.js',
					'<%= bower %>/angular-route/angular-route.js',
					'<%= bower %>/angularjs-ordinal-filter/ordinal.js',
					'<%= bower %>/angular-animate/angular-animate.js',
					'<%= bower %>/angular-loading-bar/build/loading-bar.js',
					'<%= bower %>/angular-sweetalert/SweetAlert.js',
					'<%= bower %>/sweetalert/lib/sweet-alert.js',
					
					'<%= app %>/app.js',
					'<%= app %>/athlete/*.js',
					'<%= app %>/home/*.js',
					'<%= app %>/navigation/*.js',
					'<%= app %>/shared/*.js',
					'<%= app %>/week/*.js',

					'!<%= app %>/**/*_test.js'

				],
				dest: '<%= js_build_path %>/built.js',
			},
			css: {
				src: [
					'<%= bower %>/bootstrap/dist/css/bootstrap.css',
					'<%= bower %>/bootstrap/dist/css/bootstrap-theme.css',
					'<%= bower %>/angular-loading-bar/build/loading-bar.css',
					'<%= bower %>/sweetalert/lib/sweet-alert.css'
				],
				dest: '<%= css_build_path %>/built.css'
			}
		},

		uglify: {
			options: {
				banner: '/*! Fitness Evaluation <%= grunt.template.today("yyyy-mm-dd") %> */\n',
				mangle: false
			},
			js: {
				files: {
					'<%= js_build_path %>/built.min.js': ['<%= concat.js.dest %>']
				}
			}
		},

		cssmin: {
			css: {
				src: '<%= concat.css.dest %>',
				dest: '<%= css_build_path %>/built.min.css'
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
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-newer');

	// grunt.event.on('watch', function(action, filepath, target) {
	// 	grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
	// });

	// Default task(s).
	grunt.registerTask('default', ['concat', 'uglify', 'cssmin']);
	grunt.registerTask('dev', ['concat']);

};