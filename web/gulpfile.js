var gulp      = require('gulp');
var sass      = require('gulp-sass');

// Needs Ruby and ruby scss-lint gem
// sudo apt-get install ruby-full && gem update --system && gem install scss-lint
var scsslint  = require('gulp-scss-lint');
var minifyCss = require('gulp-minify-css');
var rename    = require('gulp-rename');
var watch     = require('gulp-watch');

var static_build_path = './app/static/';

var paths = {
  sass:       ['./scss/*.scss', './scss/**/*.scss', '!./scss/vendor/**/*.scss'],
  templates:  ['./**/*.html'],
  sassConfig: '.sass-lint.yml'
};

gulp.task('watch', function () {
  gulp.watch(paths.sass, ['scss-lint', 'sass']);
});

gulp.task('scss-lint', function() {
  return gulp.src(paths.sass)
    .pipe(scsslint({
      'config': paths.sassConfig,
    }))
    .on('error', function (err) {
      console.error(err);
    });
});

gulp.task('sass', function (done) {
    gulp.src('./scss/main.scss')
    .pipe(sass())
    .pipe(gulp.dest(static_build_path + './css/'))
    .pipe(minifyCss({
      keepSpecialComments: 0
    }))
    .pipe(rename({ extname: '.min.css' }))
    .pipe(gulp.dest(static_build_path + './css/'))
    .on('end', done);
});

gulp.task('build', ['scss-lint', 'sass']);
gulp.task('watch:scss', ['scss-lint', 'sass', 'watch']);
