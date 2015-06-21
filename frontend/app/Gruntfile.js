/**
 * File: Gruntfile.js
 * Description: Grunt taskrunner for the project
 * Dependencies: see package.json
 *
 * @package Planet-Lab
 */

'use strict';

module.exports = function(grunt) {
    /* === Initial Config === */
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            options: {
                banner: '(function () {',
                footer: '})();'
            },
            dist: {
                src: ['app.js', '*/*.js'],
                dest: 'scripts.js'
            }
        },
        ngAnnotate: {
            app1: {
                files: {
                    'scripts.js': ['scripts.js']
                }
            }
        },
        sass: {
            dist: {
                options: {
                    style: 'expanded'
                },
                files: {
                    'assets/css/main.css': 'assets/sass/main.scss'
                }
            }
        },
        uglify: {
            build: {
                src: 'scripts.js',
                dest: 'scripts.min.js'
            }
        },
        watch: {
            scripts: {
                files: ['assets/sass/*.scss', 'assets/sass/*/*.scss', 'app.js', '*/*.js'],
                tasks: ['sass', 'concat']
            }
        }
    });

    /* === Loading Plugins === */
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-ng-annotate');

    /* === Register Tasks ===  */
    grunt.registerTask('default', ['concat', 'ngAnnotate', 'sass', 'watch']);
    grunt.registerTask('deploy', ['concat', 'ngAnnotate', 'sass', 'uglify']);
};
