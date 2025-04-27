from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wagtail.models import Page, Site
from content.models import (
    HeroSection, AboutSection, ContactInfo,
    Experience, Education, Course, Project, 
    SkillCategory, Skill, UiText
)
from portfolio_cms.models import (
    PortfolioPage, SkillCategoryRelation, SkillRelation,
    ExperienceRelation, EducationRelation, CourseRelation,
    ProjectRelation, UISettings
)


class Command(BaseCommand):
    help = 'Переносит данные из моделей Django в модели Wagtail CMS'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем перенос данных в Wagtail CMS...')
        
        # Получаем корневую страницу
        try:
            root_page = Page.objects.get(id=1)
            self.stdout.write(f'Найдена корневая страница: {root_page}')
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не найдена корневая страница Wagtail. Миграция отменена.'))
            return
        
        # Мы работаем с существующей структурой
        self.stdout.write('Существующие страницы:')
        for page in Page.objects.all():
            self.stdout.write(f'ID: {page.id}, Title: {page.title}, Path: {page.path}, Depth: {page.depth}')
        
        # Удаляем все портфолио-страницы Wagtail, если они существуют
        for portfolio in PortfolioPage.objects.all():
            self.stdout.write(f'Удаляем старую страницу портфолио: {portfolio.id}')
            portfolio.delete()
        
        # Находим страницу второго уровня (welcome page) для замены
        welcome_page = Page.objects.filter(depth=2).first()
        
        if welcome_page:
            self.stdout.write(f'Найдена страница приветствия: {welcome_page.title}')
            
            # Создаем новую страницу портфолио на месте welcome page
            portfolio = PortfolioPage(
                title="Портфолио Эдуарда Босака",
                slug=welcome_page.slug,
                seo_title="Портфолио Эдуарда Босака - Менеджер проектов и клиентского сервиса",
                show_in_menus=True,
            )
            
            # Заменяем welcome page нашей страницей
            welcome_page.delete()
            root_page.add_child(instance=portfolio)
            
            self.stdout.write(self.style.SUCCESS(f'Создана страница портфолио с ID: {portfolio.id}'))
            
            # Настраиваем сайт
            site = Site.objects.first()
            if site:
                site.root_page = portfolio
                site.site_name = 'Портфолио Эдуарда Босака'
                site.save()
                self.stdout.write(f'Обновлены настройки сайта: {site}')
        else:
            self.stdout.write('Страница приветствия не найдена, создаем новую страницу портфолио...')
            portfolio = PortfolioPage(
                title="Портфолио Эдуарда Босака",
                slug="home",
                seo_title="Портфолио Эдуарда Босака - Менеджер проектов и клиентского сервиса",
                show_in_menus=True,
            )
            root_page.add_child(instance=portfolio)
            
            # Настраиваем сайт
            site = Site.objects.first()
            if site:
                site.root_page = portfolio
                site.site_name = 'Портфолио Эдуарда Босака'
                site.save()
        
        # Перенос данных из секции Hero
        hero = HeroSection.objects.first()
        if hero:
            self.stdout.write('Переносим данные из секции Hero...')
            portfolio.hero_title_ru = hero.title_ru
            portfolio.hero_title_en = hero.title_en
            portfolio.hero_subtitle_ru = hero.subtitle_ru
            portfolio.hero_subtitle_en = hero.subtitle_en
            portfolio.small_subtitle_ru = hero.small_subtitle_ru
            portfolio.small_subtitle_en = hero.small_subtitle_en
            portfolio.save()
        
        # Перенос данных из секции About
        about = AboutSection.objects.first()
        if about:
            self.stdout.write('Переносим данные из секции About...')
            portfolio.about_me_ru = about.description_ru
            portfolio.about_me_en = about.description_en
            portfolio.save()
        
        # Перенос контактной информации
        contact = ContactInfo.objects.first()
        if contact:
            self.stdout.write('Переносим контактную информацию...')
            portfolio.email = contact.email
            portfolio.phone = contact.phone
            portfolio.location_ru = contact.location_ru
            portfolio.location_en = contact.location_en
            portfolio.save()
        
        # Перенос категорий навыков и навыков
        self.stdout.write('Переносим категории навыков и навыки...')
        for category in SkillCategory.objects.all().order_by('order'):
            skill_category = SkillCategoryRelation(
                page=portfolio,
                name_ru=category.name_ru,
                name_en=category.name_en,
                order=category.order
            )
            skill_category.save()
            
            # Добавляем навыки для этой категории
            for skill in Skill.objects.filter(category=category).order_by('order'):
                SkillRelation.objects.create(
                    category=skill_category,
                    name_ru=skill.name_ru,
                    name_en=skill.name_en,
                    order=skill.order
                )
        
        # Перенос опыта работы
        self.stdout.write('Переносим данные об опыте работы...')
        for exp in Experience.objects.all().order_by('order'):
            ExperienceRelation.objects.create(
                page=portfolio,
                title_ru=exp.title_ru,
                title_en=exp.title_en,
                company_ru=exp.company_ru,
                company_en=exp.company_en,
                period_ru=exp.period_ru,
                period_en=exp.period_en,
                location_ru=exp.location_ru,
                location_en=exp.location_en,
                responsibilities_ru=exp.responsibilities_ru,
                responsibilities_en=exp.responsibilities_en,
                achievements_ru=exp.achievements_ru,
                achievements_en=exp.achievements_en,
                order=exp.order
            )
        
        # Перенос образования и курсов
        self.stdout.write('Переносим данные об образовании и курсах...')
        for edu in Education.objects.all().order_by('order'):
            education = EducationRelation.objects.create(
                page=portfolio,
                degree_ru=edu.degree_ru,
                degree_en=edu.degree_en,
                institution_ru=edu.institution_ru,
                institution_en=edu.institution_en,
                year_ru=edu.year_ru,
                year_en=edu.year_en,
                is_course_section=edu.is_course_section,
                order=edu.order
            )
            
            # Добавляем курсы, если это запись об образовании с курсами
            if edu.is_course_section:
                for course in Course.objects.filter(education_entry=edu).order_by('order'):
                    CourseRelation.objects.create(
                        education=education,
                        name_ru=course.name_ru,
                        name_en=course.name_en,
                        order=course.order
                    )
        
        # Перенос проектов
        self.stdout.write('Переносим данные о проектах...')
        for proj in Project.objects.all().order_by('order'):
            ProjectRelation.objects.create(
                page=portfolio,
                title_ru=proj.title_ru,
                title_en=proj.title_en,
                description_ru=proj.description_ru,
                description_en=proj.description_en,
                # Без изображения пока, т.к. нужно отдельно загружать в Wagtail Media
                order=proj.order
            )
        
        # Перенос UI текстов
        ui_texts = UiText.objects.first()
        if ui_texts:
            self.stdout.write('Переносим тексты интерфейса...')
            # Удаляем старые настройки UI, если они существуют
            UISettings.objects.all().delete()
            
            # Создаем новые настройки UI
            ui_settings = UISettings()
                
            # Копируем все тексты интерфейса
            ui_settings.nav_about_ru = ui_texts.nav_about_ru
            ui_settings.nav_about_en = ui_texts.nav_about_en
            ui_settings.nav_skills_ru = ui_texts.nav_skills_ru
            ui_settings.nav_skills_en = ui_texts.nav_skills_en
            ui_settings.nav_experience_ru = ui_texts.nav_experience_ru
            ui_settings.nav_experience_en = ui_texts.nav_experience_en
            ui_settings.nav_education_ru = ui_texts.nav_education_ru
            ui_settings.nav_education_en = ui_texts.nav_education_en
            ui_settings.nav_projects_ru = ui_texts.nav_projects_ru
            ui_settings.nav_projects_en = ui_texts.nav_projects_en
            ui_settings.nav_contact_ru = ui_texts.nav_contact_ru
            ui_settings.nav_contact_en = ui_texts.nav_contact_en
            
            ui_settings.section_about_ru = ui_texts.section_about_ru
            ui_settings.section_about_en = ui_texts.section_about_en
            ui_settings.section_skills_ru = ui_texts.section_skills_ru
            ui_settings.section_skills_en = ui_texts.section_skills_en
            ui_settings.section_experience_ru = ui_texts.section_experience_ru
            ui_settings.section_experience_en = ui_texts.section_experience_en
            ui_settings.section_education_ru = ui_texts.section_education_ru
            ui_settings.section_education_en = ui_texts.section_education_en
            ui_settings.section_projects_ru = ui_texts.section_projects_ru
            ui_settings.section_projects_en = ui_texts.section_projects_en
            ui_settings.section_contact_ru = ui_texts.section_contact_ru
            ui_settings.section_contact_en = ui_texts.section_contact_en
            
            ui_settings.label_responsibilities_ru = ui_texts.label_responsibilities_ru
            ui_settings.label_responsibilities_en = ui_texts.label_responsibilities_en
            ui_settings.label_achievements_ru = ui_texts.label_achievements_ru
            ui_settings.label_achievements_en = ui_texts.label_achievements_en
            ui_settings.label_graduation_year_ru = ui_texts.label_graduation_year_ru
            ui_settings.label_graduation_year_en = ui_texts.label_graduation_year_en
            ui_settings.label_preferred_contact_ru = ui_texts.label_preferred_contact_ru
            ui_settings.label_preferred_contact_en = ui_texts.label_preferred_contact_en
            
            ui_settings.copyright_text_ru = ui_texts.copyright_text_ru
            ui_settings.copyright_text_en = ui_texts.copyright_text_en
            
            # Копируем тексты кнопок призыва к действию
            portfolio.cta_projects_ru = ui_texts.cta_projects_ru
            portfolio.cta_projects_en = ui_texts.cta_projects_en
            portfolio.cta_contact_ru = ui_texts.cta_contact_ru
            portfolio.cta_contact_en = ui_texts.cta_contact_en
            
            ui_settings.save()
            portfolio.save()
        
        # Публикуем страницу
        revision = portfolio.save_revision()
        revision.publish()
        
        self.stdout.write(self.style.SUCCESS('Перенос данных в Wagtail CMS успешно завершен!'))