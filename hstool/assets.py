from django_assets import Bundle, register


CSS_ASSETS = (
    'css/bootstrap.min.css',
    'css/bootstrap-datetimepicker.css',
    'css/jquery.dataTables.css',
    'css/style.css',
    'css/d3_relations.css',
)


JS_ASSETS = (
    'js/lib/jquery.min.js',
    'js/lib/bootstrap.min.js',
    'js/lib/moment.js',
    'js/lib/bootstrap-datetimepicker.min.js',
    'js/lib/jquery.dataTables.min.js',
    'js/main.js',
)

JS_D3 = (
    'js/lib/d3.js',
    'js/lib/d3.min.js',
    'js/d3_relations.js',
)


css = Bundle(*CSS_ASSETS, filters='cssmin', output='packed.css')
js = Bundle(*JS_ASSETS, filters='jsmin', output='packed.js')
js_d3 = Bundle(*JS_D3, filters='jsmin', output='packed_d3.js')
register('css', css)
register('js', js)
register('js_d3', js_d3)
