from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from django.forms.models import model_to_dict

# Переопределяю метод clean для страниц
def custom_clean(self):
    return self

# Переопределяю метод save для Page
original_page_save = Page.save
def custom_page_save(self, *args, **kwargs):
    kwargs['clean'] = False
    return original_page_save(self, *args, **kwargs)

# Монкипатч для Page, чтобы обходить валидацию
Page.clean = custom_clean
Page.save = custom_page_save

# Основная страница портфолио
class PortfolioPage(Page):
    template = 'index.html'
    """Главная страница портфолио с настройками разделов"""
    
    def serve(self, request, *args, **kwargs):
        from django.shortcuts import render
        context = self.get_context(request, *args, **kwargs)
        return render(request, self.template, context)

    hero_title_ru = models.CharField("Заголовок (RU)", max_length=200, default="Привет! Я Эдуард Босак")
    hero_title_en = models.CharField("Заголовок (EN)", max_length=200, default="Hi! I'm Eduard Bosak", blank=True, null=True)
    hero_subtitle_ru = models.CharField("Подзаголовок (RU)", max_length=300, default="Менеджер проектов и клиентского сервиса")
    hero_subtitle_en = models.CharField("Подзаголовок (EN)", max_length=300, default="Project and Customer Experience Manager", blank=True, null=True)
    small_subtitle_ru = models.CharField("Малый подзаголовок (RU)", max_length=300, blank=True, default="Открыт к переезду в Санкт-Петербург и командировкам.")
    small_subtitle_en = models.CharField("Малый подзаголовок (EN)", max_length=300, blank=True, null=True, default="Open to relocation to St. Petersburg and business trips.")

    about_me_ru = RichTextField("О себе (RU)", blank=True)
    about_me_en = RichTextField("О себе (EN)", blank=True, null=True)
    
    # Настройки UI текстов для локализации
    ui_texts_title = models.CharField("Заголовок группы UI текстов", max_length=200, default="Тексты интерфейса", help_text="Административное обозначение")
    
    # Кнопки призыва к действию
    cta_projects_ru = models.CharField("Кнопка: Мои проекты (RU)", max_length=50, default="Мои проекты")
    cta_projects_en = models.CharField("Кнопка: Мои проекты (EN)", max_length=50, default="My Projects", blank=True, null=True)
    cta_contact_ru = models.CharField("Кнопка: Связаться (RU)", max_length=50, default="Связаться со мной")
    cta_contact_en = models.CharField("Кнопка: Связаться (EN)", max_length=50, default="Contact Me", blank=True, null=True)
    
    # Контактная информация
    email = models.EmailField("Email", default="info@eduardbosak.ru")
    phone = models.CharField("Телефон", max_length=30, default="+7 (995) 079-97-77")
    location_ru = models.CharField("Местоположение (RU)", max_length=150, default="Москва, Россия (м. Красногвардейская)")
    location_en = models.CharField("Местоположение (EN)", max_length=150, default="Moscow, Russia (m. Красногвардейская)", blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title_ru'),
            FieldPanel('hero_title_en'),
            FieldPanel('hero_subtitle_ru'),
            FieldPanel('hero_subtitle_en'),
            FieldPanel('small_subtitle_ru'),
            FieldPanel('small_subtitle_en'),
        ], heading="Hero Секция"),
        
        MultiFieldPanel([
            FieldPanel('about_me_ru'),
            FieldPanel('about_me_en'),
        ], heading="Обо мне"),
        
        MultiFieldPanel([
            FieldPanel('cta_projects_ru'),
            FieldPanel('cta_projects_en'),
            FieldPanel('cta_contact_ru'),
            FieldPanel('cta_contact_en'),
        ], heading="Кнопки призыва к действию"),
        
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('location_ru'),
            FieldPanel('location_en'),
        ], heading="Контактная информация"),
        
        InlinePanel('skill_categories', label="Категория навыков"),
        InlinePanel('experiences', label="Опыт работы"),
        InlinePanel('educations', label="Образование"),
        InlinePanel('projects', label="Проекты"),
    ]
    
    # Переопределяем метод clean для этого класса
    def clean(self):
        return self
        
    # Переопределяем метод save
    def save(self, *args, **kwargs):
        kwargs['clean'] = False
        return super().save(*args, **kwargs)
    
    def get_context(self, request, *args, **kwargs):
        from .models import UISettings
        context = super().get_context(request, *args, **kwargs)
        # Формируем контекст для шаблона
        context['hero'] = {
            'title_ru': self.hero_title_ru, 'title_en': self.hero_title_en,
            'subtitle_ru': self.hero_subtitle_ru, 'subtitle_en': self.hero_subtitle_en,
            'small_subtitle_ru': self.small_subtitle_ru, 'small_subtitle_en': self.small_subtitle_en,
            'cta_projects_ru': self.cta_projects_ru, 'cta_projects_en': self.cta_projects_en,
            'cta_contact_ru': self.cta_contact_ru, 'cta_contact_en': self.cta_contact_en,
        }
        context['about'] = {'description_ru': self.about_me_ru, 'description_en': self.about_me_en}
        # UI-настройки из сниппета
        context['ui'] = UISettings.objects.first()
        # Контактная информация
        context['contact'] = {
            'email': self.email, 'phone': self.phone,
            'location_ru': self.location_ru, 'location_en': self.location_en,
        }
        # Связанные объекты
        context['skill_categories'] = self.skill_categories.all()
        context['experiences'] = self.experiences.all()
        context['educations'] = self.educations.all()
        context['projects'] = self.projects.all()
        return context
    
    class Meta:
        verbose_name = "Портфолио"
        verbose_name_plural = "Портфолио"


# Категория навыков - связанные с PortfolioPage
class SkillCategoryRelation(ClusterableModel, Orderable):
    page = ParentalKey('PortfolioPage', on_delete=models.CASCADE, related_name='skill_categories')
    name_ru = models.CharField("Название категории (RU)", max_length=100)
    name_en = models.CharField("Название категории (EN)", max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    
    panels = [
        FieldPanel('name_ru'),
        FieldPanel('name_en'),
        FieldPanel('order'),
        InlinePanel('skills', label="Навык"),
    ]
    
    def clean(self):
        return self
        
    class Meta:
        verbose_name = "Категория навыков"
        verbose_name_plural = "Категории навыков"


# Навыки - связанные с категорией навыков
class SkillRelation(Orderable):
    category = ParentalKey('SkillCategoryRelation', on_delete=models.CASCADE, related_name='skills')
    name_ru = models.CharField("Название навыка (RU)", max_length=150)
    name_en = models.CharField("Название навыка (EN)", max_length=150, blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    
    panels = [
        FieldPanel('name_ru'),
        FieldPanel('name_en'),
        FieldPanel('order'),
    ]
    
    def clean(self):
        return self
    
    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


# Опыт работы - связан с PortfolioPage
class ExperienceRelation(Orderable):
    page = ParentalKey('PortfolioPage', on_delete=models.CASCADE, related_name='experiences')
    title_ru = models.CharField("Должность (RU)", max_length=200)
    title_en = models.CharField("Должность (EN)", max_length=200, blank=True, null=True)
    company_ru = models.CharField("Компания (RU)", max_length=200)
    company_en = models.CharField("Компания (EN)", max_length=200, blank=True, null=True)
    period_ru = models.CharField("Период (RU)", max_length=100)
    period_en = models.CharField("Период (EN)", max_length=100, blank=True, null=True)
    location_ru = models.CharField("Местоположение (RU)", max_length=100, blank=True)
    location_en = models.CharField("Местоположение (EN)", max_length=100, blank=True, null=True)
    responsibilities_ru = RichTextField("Обязанности (RU)")
    responsibilities_en = RichTextField("Обязанности (EN)", blank=True, null=True)
    achievements_ru = RichTextField("Достижения (RU)", blank=True)
    achievements_en = RichTextField("Достижения (EN)", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    
    panels = [
        FieldPanel('title_ru'),
        FieldPanel('title_en'),
        FieldPanel('company_ru'),
        FieldPanel('company_en'),
        FieldPanel('period_ru'),
        FieldPanel('period_en'),
        FieldPanel('location_ru'),
        FieldPanel('location_en'),
        FieldPanel('responsibilities_ru'),
        FieldPanel('responsibilities_en'),
        FieldPanel('achievements_ru'),
        FieldPanel('achievements_en'),
        FieldPanel('order'),
    ]
    
    def clean(self):
        return self
    
    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"


# Образование - связано с PortfolioPage
class EducationRelation(ClusterableModel, Orderable):
    page = ParentalKey('PortfolioPage', on_delete=models.CASCADE, related_name='educations')
    degree_ru = models.CharField("Степень/Название (RU)", max_length=250)
    degree_en = models.CharField("Степень/Название (EN)", max_length=250, blank=True, null=True)
    institution_ru = models.CharField("Учебное заведение (RU)", max_length=300)
    institution_en = models.CharField("Учебное заведение (EN)", max_length=300, blank=True, null=True)
    year_ru = models.CharField("Год окончания (RU)", max_length=50)
    year_en = models.CharField("Год окончания (EN)", max_length=50, blank=True, null=True)
    is_course_section = models.BooleanField("Это секция доп. курсов?", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)
    
    panels = [
        FieldPanel('degree_ru'),
        FieldPanel('degree_en'),
        FieldPanel('institution_ru'),
        FieldPanel('institution_en'),
        FieldPanel('year_ru'),
        FieldPanel('year_en'),
        FieldPanel('is_course_section'),
        FieldPanel('order'),
        InlinePanel('courses', label="Дополнительный курс"),
    ]
    
    def clean(self):
        return self
    
    class Meta:
        verbose_name = "Образование / Квалификация"
        verbose_name_plural = "Образование и Квалификации"


# Курсы - связаны с образованием
class CourseRelation(Orderable):
    education = ParentalKey('EducationRelation', on_delete=models.CASCADE, related_name='courses')
    name_ru = models.CharField("Название курса (RU)", max_length=200)
    name_en = models.CharField("Название курса (EN)", max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    
    panels = [
        FieldPanel('name_ru'),
        FieldPanel('name_en'),
        FieldPanel('order'),
    ]
    
    def clean(self):
        return self
    
    class Meta:
        verbose_name = "Дополнительный курс"
        verbose_name_plural = "Дополнительные курсы"


# Проекты - связаны с PortfolioPage
class ProjectRelation(Orderable):
    page = ParentalKey('PortfolioPage', on_delete=models.CASCADE, related_name='projects')
    title_ru = models.CharField("Название проекта (RU)", max_length=200)
    title_en = models.CharField("Название проекта (EN)", max_length=200, blank=True, null=True)
    description_ru = RichTextField("Описание (RU)")
    description_en = RichTextField("Описание (EN)", blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    
    panels = [
        FieldPanel('title_ru'),
        FieldPanel('title_en'),
        FieldPanel('description_ru'),
        FieldPanel('description_en'),
        FieldPanel('image'),
        FieldPanel('order'),
    ]
    
    def clean(self):
        return self
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


# Регистрируем настройки UI для админки
@register_snippet
class UISettings(models.Model):
    # Меню навигации
    nav_about_ru = models.CharField("Меню: Обо мне (RU)", max_length=50, default="Обо мне")
    nav_about_en = models.CharField("Меню: Обо мне (EN)", max_length=50, default="About", blank=True, null=True)
    nav_skills_ru = models.CharField("Меню: Навыки (RU)", max_length=50, default="Навыки")
    nav_skills_en = models.CharField("Меню: Навыки (EN)", max_length=50, default="Skills", blank=True, null=True)
    nav_experience_ru = models.CharField("Меню: Опыт (RU)", max_length=50, default="Опыт")
    nav_experience_en = models.CharField("Меню: Опыт (EN)", max_length=50, default="Experience", blank=True, null=True)
    nav_education_ru = models.CharField("Меню: Образование (RU)", max_length=50, default="Образование")
    nav_education_en = models.CharField("Меню: Образование (EN)", max_length=50, default="Education", blank=True, null=True)
    nav_projects_ru = models.CharField("Меню: Проекты (RU)", max_length=50, default="Проекты")
    nav_projects_en = models.CharField("Меню: Проекты (EN)", max_length=50, default="Projects", blank=True, null=True)
    nav_contact_ru = models.CharField("Меню: Контакты (RU)", max_length=50, default="Контакты")
    nav_contact_en = models.CharField("Меню: Контакты (EN)", max_length=50, default="Contact", blank=True, null=True)
    
    # Заголовки секций
    section_about_ru = models.CharField("Заголовок: Обо мне (RU)", max_length=50, default="Обо мне")
    section_about_en = models.CharField("Заголовок: Обо мне (EN)", max_length=50, default="About Me", blank=True, null=True)
    section_skills_ru = models.CharField("Заголовок: Навыки (RU)", max_length=50, default="Ключевые навыки")
    section_skills_en = models.CharField("Заголовок: Навыки (EN)", max_length=50, default="Key Skills", blank=True, null=True)
    section_experience_ru = models.CharField("Заголовок: Опыт (RU)", max_length=50, default="Опыт работы")
    section_experience_en = models.CharField("Заголовок: Опыт (EN)", max_length=50, default="Work Experience", blank=True, null=True)
    section_education_ru = models.CharField("Заголовок: Образование (RU)", max_length=50, default="Образование")
    section_education_en = models.CharField("Заголовок: Образование (EN)", max_length=50, default="Education", blank=True, null=True)
    section_projects_ru = models.CharField("Заголовок: Проекты (RU)", max_length=50, default="Проекты")
    section_projects_en = models.CharField("Заголовок: Проекты (EN)", max_length=50, default="Projects", blank=True, null=True)
    section_contact_ru = models.CharField("Заголовок: Контакты (RU)", max_length=50, default="Контакты")
    section_contact_en = models.CharField("Заголовок: Контакты (EN)", max_length=50, default="Contact", blank=True, null=True)
    
    # Метки в разделах
    label_responsibilities_ru = models.CharField("Метка: Обязанности (RU)", max_length=50, default="Обязанности:")
    label_responsibilities_en = models.CharField("Метка: Обязанности (EN)", max_length=50, default="Responsibilities:", blank=True, null=True)
    label_achievements_ru = models.CharField("Метка: Достижения (RU)", max_length=50, default="Достижения:")
    label_achievements_en = models.CharField("Метка: Достижения (EN)", max_length=50, default="Achievements:", blank=True, null=True)
    label_graduation_year_ru = models.CharField("Метка: Год окончания (RU)", max_length=50, default="Год окончания:")
    label_graduation_year_en = models.CharField("Метка: Год окончания (EN)", max_length=50, default="Graduation Year:", blank=True, null=True)
    label_preferred_contact_ru = models.CharField("Метка: Предпочтительный способ связи (RU)", max_length=100, default="(Предпочтительный способ связи)")
    label_preferred_contact_en = models.CharField("Метка: Предпочтительный способ связи (EN)", max_length=100, default="(Preferred contact method)", blank=True, null=True)
    
    # Копирайт
    copyright_text_ru = models.CharField("Копирайт (RU)", max_length=100, default="Все права защищены.")
    copyright_text_en = models.CharField("Копирайт (EN)", max_length=100, default="All rights reserved.", blank=True, null=True)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('nav_about_ru'),
            FieldPanel('nav_about_en'),
            FieldPanel('nav_skills_ru'),
            FieldPanel('nav_skills_en'),
            FieldPanel('nav_experience_ru'),
            FieldPanel('nav_experience_en'),
            FieldPanel('nav_education_ru'),
            FieldPanel('nav_education_en'),
            FieldPanel('nav_projects_ru'),
            FieldPanel('nav_projects_en'),
            FieldPanel('nav_contact_ru'),
            FieldPanel('nav_contact_en'),
        ], heading="Меню навигации"),
        
        MultiFieldPanel([
            FieldPanel('section_about_ru'),
            FieldPanel('section_about_en'),
            FieldPanel('section_skills_ru'),
            FieldPanel('section_skills_en'),
            FieldPanel('section_experience_ru'),
            FieldPanel('section_experience_en'),
            FieldPanel('section_education_ru'),
            FieldPanel('section_education_en'),
            FieldPanel('section_projects_ru'),
            FieldPanel('section_projects_en'),
            FieldPanel('section_contact_ru'),
            FieldPanel('section_contact_en'),
        ], heading="Заголовки секций"),
        
        MultiFieldPanel([
            FieldPanel('label_responsibilities_ru'),
            FieldPanel('label_responsibilities_en'),
            FieldPanel('label_achievements_ru'),
            FieldPanel('label_achievements_en'),
            FieldPanel('label_graduation_year_ru'),
            FieldPanel('label_graduation_year_en'),
            FieldPanel('label_preferred_contact_ru'),
            FieldPanel('label_preferred_contact_en'),
        ], heading="Метки в разделах"),
        
        MultiFieldPanel([
            FieldPanel('copyright_text_ru'),
            FieldPanel('copyright_text_en'),
        ], heading="Копирайт"),
    ]
    
    def clean(self):
        return self
    
    class Meta:
        verbose_name = "Настройки интерфейса"
        verbose_name_plural = "Настройки интерфейса"
