from django.apps import AppConfig
import os
from django.conf import settings

class TestingConfig(AppConfig):
    name = 'testing'
    
    def ready(self):
        sheets_dir = os.path.join(settings.BASE_DIR, "sheets")
        os.makedirs(sheets_dir, exist_ok=True)
