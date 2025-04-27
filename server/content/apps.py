# content/apps.py
from django.apps import AppConfig

class ContentConfig(AppConfig): # <-- Убедитесь, что имя класса именно такое
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content' # <-- Имя вашего приложения