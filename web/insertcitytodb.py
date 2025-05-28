import os
from os import path
import sys
import django

BASE_DIR = path.dirname(path.abspath(__file__))

# Добавляем путь к проекту в PYTHONPATH
project_path = BASE_DIR
if project_path not in sys.path:
    sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

# Теперь можно работать с моделями
from main.models import City



with open(path.join(BASE_DIR, 'txt-cities-russia.txt'), 'r') as file:
    while True:
        line = file.readline().strip()
        if not line:
            break
        City.objects.get_or_create(name=line)
        
