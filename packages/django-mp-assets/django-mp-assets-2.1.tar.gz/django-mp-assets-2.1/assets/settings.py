
from os.path import join

from cbsettings import DjangoDefaults

from assets import constants


class StaticFileSettings(object):

    STATIC_APPS = []

    IS_LESS_ENABLED = False

    STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

    STATICFILES_FINDERS = DjangoDefaults.STATICFILES_FINDERS + [
        'pipeline.finders.PipelineFinder',
        'djangobower.finders.BowerFinder'
    ]

    STATIC_URL = '/static/'

    @property
    def BOWER_INSTALLED_APPS(self):
        return self._get_static_app_component_list(constants.BOWER_APPS_MAP)

    @property
    def STYLESHEETS(self):
        return self._get_static_app_component_list(constants.APPS_CSS_MAP)

    @property
    def JAVASCRIPT(self):
        return self._get_static_app_component_list(constants.APPS_JS_MAP)

    def _get_static_app_component_list(self, files_map):

        result = []

        for app in self.STATIC_APPS:
            try:
                styles = files_map[app]
            except KeyError:
                continue

            if isinstance(styles, str):
                result.append(styles)
            else:
                result += styles

        return tuple(result)

    @property
    def PIPELINE(self):
        return {
            'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
            'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
            'COMPILERS': self.COMPILERS,
            'STYLESHEETS': {
                'generic': {
                    'source_filenames': self.STYLESHEETS,
                    'output_filename': 'cache/generic.css',
                }
            },
            'JAVASCRIPT': {
                'generic': {
                    'source_filenames': self.JAVASCRIPT,
                    'output_filename': 'cache/generic.js'
                }
            }
        }

    @property
    def STATIC_ROOT(self):
        return join(self.BASE_DIR, 'static-collect')

    @property
    def BOWER_COMPONENTS_ROOT(self):
        return join(self.BASE_DIR, 'static')

    @property
    def STATICFILES_DIRS(self):
        return [
            join(self.BASE_DIR, 'static'),
            join(self.BASE_DIR, 'static', 'bower_components')
        ]

    @property
    def COMPILERS(self):
        if self.IS_LESS_ENABLED:
            return ['pipeline.compilers.less.LessCompiler']
        return []

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'django.contrib.staticfiles',
            'pipeline',
            'djangobower'
        ]

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + [
            'pipeline.middleware.MinifyHTMLMiddleware'
        ]

    @property
    def TEMPLATES(self):
        templates = super().TEMPLATES

        for template in templates:
            template['OPTIONS']['context_processors'] += [
                'django.template.context_processors.static'
            ]

        return templates


class MediaFileSettings(object):

    MEDIA_URL = '/media/'

    FILE_UPLOAD_PERMISSIONS = 0o755

    THUMBNAIL_QUALITY = 85

    IS_WEBP_ENABLED = False
    IS_IMAGES_APP_ENABLED = True

    @property
    def MEDIA_ROOT(self):
        return join(self.BASE_DIR, 'media')

    @property
    def INSTALLED_APPS(self):

        installed_apps =  super().INSTALLED_APPS + [
            'django_cleanup',
            'sorl.thumbnail',
            'assets'
        ]

        if self.IS_IMAGES_APP_ENABLED:
            installed_apps.append('assets.images')

        return installed_apps

    @property
    def TEMPLATES(self):
        templates = super().TEMPLATES

        extra_processors = ['django.template.context_processors.media']

        if self.IS_WEBP_ENABLED:
            extra_processors.append('assets.context_processors.webp')

        for template in templates:
            template['OPTIONS']['context_processors'] += extra_processors

        return templates
