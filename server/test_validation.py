#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from portfolio_cms.models import PortfolioPage
from wagtail.models import Page

def test_page_creation():
    print("🔍 Тестирование создания страницы...")
    
    try:
        # Получаем корневую страницу
        root = Page.objects.get(depth=1)
        print(f"✅ Корневая страница найдена: {root.title}")
          # Создаем тестовую страницу
        test_page = PortfolioPage(
            title='Test Page Validation',
            slug='test-page-validation',
            hero_title_ru='Тестовый заголовок',
            hero_title_en='Test Title',
            hero_subtitle_ru='Тестовый подзаголовок',
            hero_subtitle_en='Test Subtitle',
            small_subtitle_ru='Малый подзаголовок',
            small_subtitle_en='Small Subtitle',
            about_me_ru='Тестовое описание',
            about_me_en='Test description',
            email='test@example.com',
            phone='+7 (999) 123-45-67',
            location_ru='Тестовая локация',
            location_en='Test Location',
            cta_projects_ru='Проекты',
            cta_projects_en='Projects',
            cta_contact_ru='Контакты',
            cta_contact_en='Contact'
        )
        
        print("🔧 Создание экземпляра страницы...")
        
        # Добавляем как дочернюю страницу
        root.add_child(instance=test_page)
        print("✅ Страница добавлена в дерево")
        
        # Сохраняем
        test_page.save()
        print(f"✅ Страница сохранена с ID: {test_page.id}")
        
        # Проверяем статус
        print(f"📊 Статус страницы: live={test_page.live}, draft={test_page.has_unpublished_changes}")
        
        # Удаляем тестовую страницу
        test_page.delete()
        print("🗑️ Тестовая страница удалена")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании страницы: {str(e)}")
        print(f"💡 Тип ошибки: {type(e).__name__}")
        return False

def test_existing_page():
    print("\n🔍 Тестирование существующей страницы...")
    
    try:
        portfolio = PortfolioPage.objects.first()
        if not portfolio:
            print("❌ Страница портфолио не найдена")
            return False
            
        print(f"✅ Найдена страница: {portfolio.title}")
        print(f"📊 URL: {portfolio.url_path}")
        print(f"📊 Live: {portfolio.live}")
        
        # Пробуем обновить
        portfolio.hero_title_ru = "Обновленный заголовок"
        portfolio.save()
        print("✅ Страница успешно обновлена")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении страницы: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Запуск тестов валидации Wagtail...")
    print("=" * 50)
    
    # Тест 1: Создание новой страницы
    test1_result = test_page_creation()
    
    # Тест 2: Обновление существующей страницы  
    test2_result = test_existing_page()
    
    print("\n" + "=" * 50)
    print("📋 РЕЗУЛЬТАТЫ ТЕСТОВ:")
    print(f"✅ Создание страницы: {'ПРОЙДЕН' if test1_result else 'ПРОВАЛЕН'}")
    print(f"✅ Обновление страницы: {'ПРОЙДЕН' if test2_result else 'ПРОВАЛЕН'}")
    
    if test1_result and test2_result:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Валидация работает корректно.")
    else:
        print("⚠️ ЕСТЬ ПРОБЛЕМЫ с валидацией.")
