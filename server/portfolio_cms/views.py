from django.shortcuts import render
from django.http import HttpResponse
from wagtail.models import Page
from content.models import UiText
from portfolio_cms.models import PortfolioPage, UISettings

# Отображение главной страницы
def home_view(request):
    # Получаем страницу портфолио из Wagtail
    portfolio = PortfolioPage.objects.live().first()
    
    # Если страница не найдена, используем резервный контент из обычных моделей
    if not portfolio:
        from content.views import home_view as content_home_view
        return content_home_view(request)
    
    # Получаем настройки интерфейса из Wagtail или из обычных моделей
    ui_settings = UISettings.objects.first()
    
    # Если настройки интерфейса не найдены в Wagtail, берем их из обычной модели
    ui = ui_settings if ui_settings else UiText.load()
    
    # Адаптируем данные Wagtail для шаблона
    context = {
        'hero': {
            'title_ru': portfolio.hero_title_ru,
            'title_en': portfolio.hero_title_en,
            'subtitle_ru': portfolio.hero_subtitle_ru,
            'subtitle_en': portfolio.hero_subtitle_en,
            'small_subtitle_ru': portfolio.small_subtitle_ru,
            'small_subtitle_en': portfolio.small_subtitle_en,
        },
        'about': {
            'description_ru': portfolio.about_me_ru,
            'description_en': portfolio.about_me_en,
        },
        'contact': {
            'email': portfolio.email,
            'phone': portfolio.phone,
            'location_ru': portfolio.location_ru,
            'location_en': portfolio.location_en,
        },
        'ui': ui,
        'skill_categories': [],
        'experiences': [],
        'educations': [],
        'projects': [],
    }
    
    # Добавляем категории навыков
    for category in portfolio.skill_categories.all().order_by('order'):
        skill_data = {
            'name_ru': category.name_ru,
            'name_en': category.name_en,
            'skills': [{
                'name_ru': skill.name_ru, 
                'name_en': skill.name_en
            } for skill in category.skills.all().order_by('order')]
        }
        context['skill_categories'].append(skill_data)
    
    # Добавляем опыт работы
    for exp in portfolio.experiences.all().order_by('order'):
        exp_data = {
            'title_ru': exp.title_ru,
            'title_en': exp.title_en,
            'company_ru': exp.company_ru,
            'company_en': exp.company_en,
            'period_ru': exp.period_ru,
            'period_en': exp.period_en,
            'location_ru': exp.location_ru,
            'location_en': exp.location_en,
            'responsibilities_ru': exp.responsibilities_ru,
            'responsibilities_en': exp.responsibilities_en,
            'achievements_ru': exp.achievements_ru,
            'achievements_en': exp.achievements_en,
        }
        context['experiences'].append(exp_data)
    
    # Добавляем образование и курсы
    for edu in portfolio.educations.all().order_by('order'):
        edu_data = {
            'degree_ru': edu.degree_ru,
            'degree_en': edu.degree_en,
            'institution_ru': edu.institution_ru,
            'institution_en': edu.institution_en,
            'year_ru': edu.year_ru,
            'year_en': edu.year_en,
            'is_course_section': edu.is_course_section,
        }
        
        # Добавляем курсы, если это секция с курсами
        if edu.is_course_section:
            edu_data['courses'] = [{
                'name_ru': course.name_ru,
                'name_en': course.name_en
            } for course in edu.courses.all().order_by('order')]
        
        context['educations'].append(edu_data)
    
    # Добавляем проекты
    for proj in portfolio.projects.all().order_by('order'):
        proj_data = {
            'title_ru': proj.title_ru,
            'title_en': proj.title_en,
            'description_ru': proj.description_ru,
            'description_en': proj.description_en,
        }
        # Добавляем изображение, если оно есть
        if proj.image:
            proj_data['image'] = proj.image
        
        context['projects'].append(proj_data)

    # Проверка и отладка
    print("Рендеринг шаблона index.html с контекстом: ")
    for key in context:
        if key != 'ui':
            print(f"- {key}: {context[key]}")
    
    # Рендерим HTML шаблон
    return render(request, 'index.html', context)
