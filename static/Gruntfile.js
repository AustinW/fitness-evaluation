module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		app: 'app',
		dist: 'dist',

		python_templates: '../templates',
		js_build_path: '<%= dist %>/js',
		css_build_path: '<%= dist %>/css',
		bower: '<%= app %>/bower_components',

		concat: {
			options: {
				stripBanners: true,
				
				// Replace all 'use strict' statements in the code with a single one at the top
				banner: "'use strict';\n",
				
				process: function(src, filepath) {
					return '\n/* Source: ' + filepath + ' */\n' +
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
				options: {
					stripBanners: true,
					banner: ""
				},
				src: [
					'<%= bower %>/bootstrap/dist/css/bootstrap.css',
					'<%= bower %>/bootstrap/dist/css/bootstrap-theme.css',
					'<%= bower %>/angular-loading-bar/build/loading-bar.css',
					'<%= bower %>/sweetalert/lib/sweet-alert.css',
					'css/main.css'
				],
				dest: '<%= css_build_path %>/built.css'
			}
		},

		ngtemplates: {
			fitnessApp: {
				src: '<%= app %>/templates/**/*.html',
				dest: '<%= concat.js.dest %>',
				options: {
					append: true,
					prefix: 'static',
					htmlmin: {
						collapseWhitespace: true,
						collapseBooleanAttributes: true,
						remoteComments: true,
						removeRedundantAttributes: true
					}
				}
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

		cacheBust: {
			options: {
				encoding: 'utf8',
				algorithm: 'md5',
				length: '10',
				deleteOriginals: false,
				baseDir: '../',
				rename: false
			},
			assets: {
				files: [{
					src: ['<%= python_templates %>/layout.html']
				}]
			}
		},

		clean: {
			build: ['<%= js_build_path %>', '<%= css_build_path %>']
		},

		watch: {
			scripts: {
				files: ['Gruntfile.js', 'app/**/*.js', 'css/**/*.css', 'templates/**/*.html'],
				tasks: ['dev'],
				options: {
					livereload: true
				}
			},
		},

		notify_hooks: {
			options: {
				enabled: true,
				title: 'Assets compiled',
				success: true
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-angular-templates');
	grunt.loadNpmTasks('grunt-cache-bust');
	grunt.loadNpmTasks('grunt-notify');

	// Default task
	grunt.registerTask('default', [
		'clean:build', 
		'concat', 
		'ngtemplates', 
		'uglify', 
		'cssmin', 
		'cacheBust', 
		'notify_hooks'
	]);

	// Only the fastest tasks (used in `watch`)
	grunt.registerTask('dev', [
		'clean:build', 
		'concat', 
		'ngtemplates', 
		'cssmin', 
		'cacheBust', 
		'notify_hooks'
	]);

};