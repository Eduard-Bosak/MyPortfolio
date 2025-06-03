from django.core.management.base import BaseCommand
from django.conf import settings
from wagtail.models import Site, Page

class Command(BaseCommand):
    help = 'Настраивает сайт в Wagtail для связи с корневой страницей'

    def handle(self, *args, **options):
        # Проверка, существует ли уже сайт
        if Site.objects.exists():
            site = Site.objects.first()
            self.stdout.write(self.style.SUCCESS(f'Сайт уже существует: {site.hostname}, root_page_id={site.root_page_id}'))
            return

        # Получаем корневую страницу
        try:
            root_page = Page.objects.get(id=1)
            
            # Создаем сайт, связанный с корневой страницей
            site = Site.objects.create(
                hostname='localhost',
                port=8000,
                root_page=root_page,
                is_default_site=True,
                site_name='Портфолио Эдуарда Босака'
            )
            self.stdout.write(self.style.SUCCESS(f'Успешно создан сайт: {site.hostname}:{site.port}'))
            
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR('Корневая страница не найдена'))
            return