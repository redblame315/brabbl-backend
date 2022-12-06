'use strict';
var gulp = require('gulp'),
    rimraf = require('rimraf'),
    $ = require('gulp-load-plugins')(),

    config = {
      dist: '../brabbl/static/css/',
      src: 'src/'
    };


var onError = function(error) {
  $.notify.onError({
    title:    "Gulp",
    subtitle: "Failure!",
    message:  "Error: <%= error.message %>",
    sound:    "Beep"
  })(error);
  this.emit("end");
}


gulp.task('scss', function() {
  return gulp.src([config.src + '**/*.scss',
                   '!' + config.src + '**/_*.scss'])
    .pipe($.plumber({errorHandler: onError}))
    .pipe($.sourcemaps.init())
    .pipe($.sass({
      outputStyle: 'compressed',
      precision: 10
    }))
    .pipe($.autoprefixer({
      browsers: ['> 2%'],
      cascade: false,
      remove: true
    }))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest(config.dist));
});

gulp.task('build', ['scss']);

gulp.task('watch', function() {
  gulp.watch(config.src + '**/*.scss', ['scss']);
});

gulp.task('default', ['clean', 'build', 'webserver', 'watch']);
