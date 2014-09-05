from django_assets import Bundle, register


CSS_ASSETS = (
    'css/bootstrap.min.css',
    'css/bootstrap-datetimepicker.css',
    'css/jquery.dataTables.css',
    'css/style.css',
)


JS_ASSETS = (
    'js/lib/jquery.min.js',
    'js/lib/bootstrap.min.js',
    'js/lib/bootstrap-datetimepicker.min.js',
    'js/lib/jquery.dataTables.min.js',
    'js/main.js',
)


css = Bundle(*CSS_ASSETS, filters='cssmin', output='packed.css')
js = Bundle(*JS_ASSETS, filters='jsmin', output='packed.js')
register('css', css)
register('js', js)
