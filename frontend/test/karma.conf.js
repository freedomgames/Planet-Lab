module.exports = function(config){
  config.set({

    basePath : '../',

    files : [
      'bower_components/danialfarid-angular-file-upload/dist/angular-file-upload-shim.js',
      'bower_components/angular/angular.js',
      'bower_components/danialfarid-angular-file-upload/dist/angular-file-upload.js',
      'bower_components/angular-ui-router/release/angular-ui-router.js',
      'bower_components/angular-resource/angular-resource.js',
      'bower_components/angular-mocks/angular-mocks.js',
      'bower_components/angular-xeditable/dist/js/xeditable.js',
      'app/**/*.js',
      'test/unit/**/*.js'
    ],

    autoWatch : false,

    frameworks: ['jasmine'],

    browsers : ['Chrome', 'Firefox'],

    plugins : [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine'
            ],

    junitReporter : {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }

  });
};
