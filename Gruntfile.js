module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		concat: {
			options: {
				separator: ';',
				stripBanners: true,
				banner: '/*! <%= pkg.name %> - v<%= pkg.version %> - ' +
						'<%= grunt.template.today("yyyy-mm-dd") %> */',
			},
			dist: {
				src: [
					'static/bower_components/jquery/dist/jquery.js',
					'static/bower_components/bootstrap/dist/js/bootstrap.js',
					'static/bower_components/angular/angular.js',
					'static/bower_components/angular-route/angular-route.js',
					'static/bower_components/angularjs-ordinal-filter/ordinal.js',
					'static/bower_components/angular-animate/angular-animate.js',
					'static/bower_components/angular-loading-bar/build/loading-bar.js',
					'static/js/src/app.js'
				],
				dest: 'static/js/dist/built.js',
			},
		},

		uglify: {
			options: {
				banner: '/*! Fitness Evaluation <%= grunt.template.today("yyyy-mm-dd") %> */\n',
				mangle: false
			},
			dist: {
				files: {
					'static/js/dist/built.min.js': ['<%= concat.dist.dest %>']
				}
			}
		},

		clean: {
			concat: {
				src: ['static/js/tmp']
			}
		},

		watch: {
			scripts: {
				files: ['Gruntfile.js', 'static/js/src/**/*.js'],
				tasks: ['concat', 'clean'],
				options: {
					livereload: true
				}
			},
		},
	});

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-newer');

	// grunt.event.on('watch', function(action, filepath, target) {
	// 	grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
	// });

	// Default task(s).
	grunt.registerTask('default', ['concat', 'uglify', 'clean']);
	grunt.registerTask('original', ['concat', 'clean'])

};