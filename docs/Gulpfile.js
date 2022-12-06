'use strict';
var gulp = require('gulp'),
    drakov = require('drakov'),
    $ = require('gulp-load-plugins')();

var onError = function(error) {
  $.notify.onError({
    title:    "Gulp",
    subtitle: "Failure!",
    message:  "Error: <%= error.message %>",
    sound:    "Beep"
  })(error);
  this.emit("end");
}

gulp.task('build-docs', function() {
  return gulp.src(['src/brabbl.apib'])
    .pipe($.plumber({errorHandler: onError}))
    .pipe($.concat('brabbl.apib'))
    .pipe($.aglio({template: 'default'}))
    .pipe($.rename('index.html'))
    .pipe(gulp.dest('build'));
});

gulp.task('webserver', function() {
  gulp.src('build/')
    .pipe($.webserver({
      port: 9000,
      livereload: true,
      open: true
    }));
});

gulp.task('mock-server', function() {
    var argv = {
        sourceFiles: 'src/brabbl.apib',
        serverPort: 4000
    };

    drakov.run(argv, function() {
    });
});

gulp.task('watch', function() {
  gulp.watch('src/*.apib', ['build-docs']);
});


gulp.task('default', ['build-docs', 'webserver', 'watch']);
