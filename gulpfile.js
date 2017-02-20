// requirements
var gulp = require('gulp');
var gulpBrowser = require("gulp-browser");
var reactify = require('reactify');
var del = require('del');
var size = require('gulp-size');

// tasks

gulp.task('transform', function() {
    //add task
    var stream = gulp.src('./ChiBurger/static/scripts/jsx/*.js')
        .pipe(gulpBrowser.browserify({transform:['reactify']}))
        .pipe(gulp.dest('./ChiBurger/static/scripts/js/'))
        .pipe(size());
    return stream;
});

gulp.task('del', function() {
    //add task
    return del(['.ChiBurger/static/scripts/js']);
});

gulp.task('default', ['del'], function() {
    // console.log("hello!");
    gulp.start('transform');
    gulp.watch('./ChiBurger/static/scripts/jsx/*.js', ['transform']);
});