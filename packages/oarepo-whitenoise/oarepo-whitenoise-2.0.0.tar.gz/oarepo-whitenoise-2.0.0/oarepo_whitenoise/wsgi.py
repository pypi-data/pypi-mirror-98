"""WhiteNoise bridge to flask app."""

import os

from oarepo_micro_api.wsgi import application as application
from whitenoise import WhiteNoise
from whitenoise.string_utils import decode_path_info

static_folder = os.environ.get('WHITENOISE_ROOT', '/whitenoise')

assert os.path.exists(static_folder)


class IndexWhiteNoise(WhiteNoise):
    """Modified whitenoise to serve index.html for any not-found url apart from api"""

    def __call__(self, environ, start_response):
        """Call api or whitenoise"""
        path = decode_path_info(environ.get("PATH_INFO", ""))

        if 'html' in environ.get('HTTP_ACCEPT', ''):
            if self.autorefresh:
                static_file = self.find_file(path)
            else:
                static_file = self.files.get(path)
            if static_file is None:
                if self.autorefresh:
                    static_file = self.find_file('/index.html')
                else:
                    static_file = self.files.get('/index.html')

            return self.serve(static_file, environ, start_response)

        return self.application(environ, start_response)


application.wsgi_app = IndexWhiteNoise(application.wsgi_app, root=static_folder)
