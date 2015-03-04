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
					'static/bower_components/fuelux/dist/js/fuelux.js',
					'static/js/src/main.js'
				],
				dest: 'static/js/tmp/concat.js',
			},
		},

		uglify: {
			options: {
				banner: '/*! Fitness Evaluation <%= grunt.template.today("yyyy-mm-dd") %> */\n'
			},
			dist: {
				files: {
					'static/js/dist/built.js': ['<%= concat.dist.dest %>']
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
				tasks: ['concat', 'uglify', 'clean']
			},
		},
	});

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-watch');

	// grunt.event.on('watch', function(action, filepath, target) {
	// 	grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
	// });

	// Default task(s).
	grunt.registerTask('default', ['concat', 'uglify', 'clean']);

};