from django.conf import settings
import os

# Path to the service worker implementation.  Default implementation is empty.
PWA_SERVICE_WORKER_PATH = getattr(settings, 
								  'PWA_SERVICE_WORKER_PATH', 
								   os.path.join(os.path.abspath(os.path.dirname(__file__)), 
								   'templates',
                                   'serviceworker.js'))
# App parameters to include in manifest.json and appropriate meta tags
PWA_APP_NAME = getattr(settings, 'PWA_APP_NAME', 'Sahyog')
PWA_APP_DESCRIPTION = getattr(settings, 'PWA_APP_DESCRIPTION', 'The Eye of Police')
PWA_APP_THEME_COLOR = getattr(settings, 'PWA_APP_THEME_COLOR', '#000')
PWA_APP_BACKGROUND_COLOR = getattr(settings, 'PWA_APP_BACKGROUND_COLOR', '#fff')
PWA_APP_DISPLAY = getattr(settings, 'PWA_APP_DISPLAY', 'standalone')
PWA_APP_DEBUG_MODE = getattr(settings, 'PWA_APP_DEBUG_MODE', False)
PWA_APP_ORIENTATION = getattr(settings, 'PWA_APP_ORIENTATION', 'any')
PWA_APP_DIR = getattr(settings, 'PWA_APP_DIR', 'auto')
PWA_APP_LANG = getattr(settings, 'PWA_APP_LANG', 'en-US')