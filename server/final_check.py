#!/usr/bin/env python
import os
import sys
import django
import requests

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from portfolio_cms.models import PortfolioPage, UISettings
from wagtail.models import Page

def check_database():
    """Проверка состояния базы данных"""
    print("🔍 Проверка базы данных...")
    
    checks = {
        "PortfolioPage": PortfolioPage.objects.count(),
        "UISettings": UISettings.objects.count(),
        "Total Pages": Page.objects.count(),
        "Live Pages": Page.objects.filter(live=True).count()
    }
    
    for check, count in checks.items():
        status = "✅" if count > 0 else "❌"
        print(f"{status} {check}: {count}")
    
    return all(count > 0 for count in checks.values())

def check_wagtail_admin():
    """Проверка доступности Wagtail админки"""
    print("\n🔍 Проверка Wagtail админки...")
    
    try:
        response = requests.get("http://localhost:8000/cms/", timeout=5)
        if response.status_code in [200, 302]:  # 302 - редирект на логин
            print("✅ Wagtail админка доступна")
            return True
        else:
            print(f"❌ Wagtail админка недоступна (статус: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке админки: {str(e)}")
        return False

def check_main_site():
    """Проверка главной страницы сайта"""
    print("\n🔍 Проверка главной страницы...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            content = response.text
            # Проверяем наличие ключевых элементов
            checks = [
                ("Заголовок hero", "hero-title" in content or "Привет! Я Эдуард" in content),
                ("Навигация", "nav" in content and "menu" in content.lower()),
                ("Секция about", "about" in content.lower()),
                ("Контакты", "contact" in content.lower()),
                ("CSS стили", "style.css" in content),
                ("JavaScript", "script.js" in content)
            ]
            
            success = True
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"{status} {check_name}")
                if not result:
                    success = False
            
            return success
        else:
            print(f"❌ Главная страница недоступна (статус: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке главной страницы: {str(e)}")
        return False

def check_api():
    """Проверка API endpoints"""
    print("\n🔍 Проверка API...")
    
    endpoints = [
        "/api/",
        "/api/portfolio/",
        "/api/hero/",
        "/api/about/",
        "/api/contact/"
    ]
    
    success = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            status = "✅" if response.status_code in [200, 401] else "❌"  # 401 для защищенных endpoints
            print(f"{status} {endpoint} (статус: {response.status_code})")
            if response.status_code not in [200, 401]:
                success = False
        except Exception as e:
            print(f"❌ {endpoint} - Ошибка: {str(e)}")
            success = False
    
    return success

def check_wagtail_functionality():
    """Проверка функциональности Wagtail"""
    print("\n🔍 Проверка функциональности Wagtail...")
    
    try:
        # Получаем существующую страницу
        portfolio = PortfolioPage.objects.first()
        if not portfolio:
            print("❌ Страница портфолио не найдена")
            return False
        
        # Проверяем контекст шаблона
        from django.test import RequestFactory
        request = RequestFactory().get('/')
        context = portfolio.get_context(request)
        
        required_context = ['hero', 'about', 'contact', 'ui', 'skill_categories', 'experiences', 'educations', 'projects']
        missing_context = [key for key in required_context if key not in context]
        
        if missing_context:
            print(f"❌ Отсутствуют ключи контекста: {missing_context}")
            return False
        else:
            print("✅ Контекст шаблона содержит все необходимые данные")
        
        # Проверяем UISettings
        ui_settings = UISettings.objects.first()
        if ui_settings:
            print("✅ UISettings настроены")
        else:
            print("❌ UISettings не найдены")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке функциональности: {str(e)}")
        return False

def main():
    print("🚀 ФИНАЛЬНАЯ КОМПЛЕКСНАЯ ПРОВЕРКА ПРОЕКТА")
    print("=" * 60)
    
    checks = [
        ("База данных", check_database),
        ("Wagtail админка", check_wagtail_admin), 
        ("Главная страница", check_main_site),
        ("API endpoints", check_api),
        ("Функциональность Wagtail", check_wagtail_functionality)
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    print("\n" + "=" * 60)
    print("📋 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    
    all_passed = True
    for check_name, result in results.items():
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{status:15} {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ! Проект готов к использованию.")
        print("📌 Рекомендации:")
        print("   • Wagtail админка: http://localhost:8000/cms/")
        print("   • Главная страница: http://localhost:8000/")
        print("   • API: http://localhost:8000/api/")
    else:
        print("⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ. Проверьте детали выше.")
    
    return all_passed

if __name__ == "__main__":
    main()
