from django.core.management.base import BaseCommand
from content.models import (
    HeroSection, AboutSection, ContactInfo,
    Experience, Education, Project, 
    SkillCategory, Skill, UiText
)

class Command(BaseCommand):
    help = 'Создает демонстрационный контент для портфолио'

    def handle(self, *args, **options):
        self.stdout.write('Создание демонстрационного контента...')
        
        # Создаем или обновляем основные секции (синглтоны)
        hero = HeroSection.load()
        hero.title_ru = 'Привет! Я Эдуард Босак'
        hero.title_en = 'Hi! I\'m Eduard Bosak'
        hero.subtitle_ru = 'Менеджер проектов и клиентского сервиса'
        hero.subtitle_en = 'Project and Customer Experience Manager'
        hero.small_subtitle_ru = 'Открыт к переезду в Санкт-Петербург и командировкам.'
        hero.small_subtitle_en = 'Open to relocation to St. Petersburg and business trips.'
        hero.save()
        self.stdout.write(self.style.SUCCESS('Секция Hero создана/обновлена'))
        
        about = AboutSection.load()
        about.description_ru = """Менеджер проектов и клиентского сервиса с более чем 3-летним опытом. Специализируюсь на управлении проектами, улучшении клиентского опыта (CX), бизнес-аналитике и стратегическом маркетинге. Имею опыт работы в образовательных учреждениях, IT-компаниях и гостиничном бизнесе.

Обладаю высокими коммуникативными навыками, эмпатией и проактивным подходом. Постоянно стремлюсь к личностному и профессиональному росту, применяя инновационные решения и лучшие практики. Ответственен и надежен, всегда довожу начатое до конца.

Проживаю в Москве, готов к переезду в Санкт-Петербург и к командировкам."""
        about.description_en = """Project and Customer Experience Manager with over 3 years of experience. I specialize in project management, customer experience (CX) improvement, business analysis, and strategic marketing. Experienced in educational institutions, IT companies, and the hospitality industry.

Possess strong communication skills, empathy, and a proactive approach. Continuously strive for personal and professional growth, applying innovative solutions and best practices. Responsible and reliable, always seeing tasks through to completion.

Based in Moscow, open to relocation to St. Petersburg and business trips."""
        about.save()
        self.stdout.write(self.style.SUCCESS('Секция About создана/обновлена'))
        
        # Создаем или обновляем интерфейсные тексты
        ui_texts = UiText.load()
        # Значения по умолчанию уже установлены в модели, но можно их изменить
        ui_texts.nav_about_ru = 'Обо мне'
        ui_texts.nav_about_en = 'About'
        ui_texts.nav_skills_ru = 'Навыки'
        ui_texts.nav_skills_en = 'Skills'
        ui_texts.nav_experience_ru = 'Опыт'
        ui_texts.nav_experience_en = 'Experience'
        ui_texts.nav_education_ru = 'Образование'
        ui_texts.nav_education_en = 'Education'
        ui_texts.nav_projects_ru = 'Проекты'
        ui_texts.nav_projects_en = 'Projects'
        ui_texts.nav_contact_ru = 'Контакты'
        ui_texts.nav_contact_en = 'Contact'
        
        ui_texts.cta_projects_ru = 'Мои проекты'
        ui_texts.cta_projects_en = 'My Projects'
        ui_texts.cta_contact_ru = 'Связаться со мной'
        ui_texts.cta_contact_en = 'Contact Me'
        
        ui_texts.section_about_ru = 'Обо мне'
        ui_texts.section_about_en = 'About Me'
        ui_texts.section_skills_ru = 'Ключевые навыки'
        ui_texts.section_skills_en = 'Key Skills'
        ui_texts.section_experience_ru = 'Опыт работы'
        ui_texts.section_experience_en = 'Work Experience'
        ui_texts.section_education_ru = 'Образование'
        ui_texts.section_education_en = 'Education'
        ui_texts.section_projects_ru = 'Проекты'
        ui_texts.section_projects_en = 'Projects'
        ui_texts.section_contact_ru = 'Контакты'
        ui_texts.section_contact_en = 'Contact'
        
        ui_texts.label_responsibilities_ru = 'Обязанности:'
        ui_texts.label_responsibilities_en = 'Responsibilities:'
        ui_texts.label_achievements_ru = 'Достижения:'
        ui_texts.label_achievements_en = 'Achievements:'
        ui_texts.label_graduation_year_ru = 'Год окончания:'
        ui_texts.label_graduation_year_en = 'Graduation Year:'
        ui_texts.label_preferred_contact_ru = '(Предпочтительный способ связи)'
        ui_texts.label_preferred_contact_en = '(Preferred contact method)'
        
        ui_texts.copyright_text_ru = 'Все права защищены.'
        ui_texts.copyright_text_en = 'All rights reserved.'
        
        ui_texts.save()
        self.stdout.write(self.style.SUCCESS('Интерфейсные тексты созданы/обновлены'))
        
        contact = ContactInfo.load()
        contact.email = 'info@eduardbosak.ru'
        contact.phone = '+7 (995) 079-97-77'
        contact.location_ru = 'Москва, Россия (м. Красногвардейская)'
        contact.location_en = 'Moscow, Russia (m. Krasnogvardeyskaya)'
        contact.save()
        self.stdout.write(self.style.SUCCESS('Секция Contact создана/обновлена'))
        
        # Создаем категории навыков
        # Очищаем существующие категории и навыки для демонстрации
        SkillCategory.objects.all().delete()
        Skill.objects.all().delete()
        
        # Управление проектами
        pm = SkillCategory.objects.create(
            name_ru='Управление проектами',
            name_en='Project Management',
            order=1
        )
        skills_pm = [
            ('Agile, Scrum', 'Agile, Scrum'),
            ('Управление бэклогом', 'Backlog Management'),
            ('Разработка ТЗ', 'Requirements Specification Development'),
            ('Контроль реализации проектов', 'Project Execution Monitoring'),
            ('Управление техническими проектами (ЛВС, видеонаблюдение, телефония)', 'Technical Project Management (LAN, CCTV, Telephony)'),
            ('Управление веб-проектами (CMS, аналитика)', 'Web Project Management (CMS, Analytics)')
        ]
        for i, (name_ru, name_en) in enumerate(skills_pm):
            Skill.objects.create(category=pm, name_ru=name_ru, name_en=name_en, order=i+1)
            
        # Клиентский опыт
        cx = SkillCategory.objects.create(
            name_ru='Клиентский опыт (CX)',
            name_en='Customer Experience (CX)',
            order=2
        )
        skills_cx = [
            ('CJM (Customer Journey Mapping)', 'CJM (Customer Journey Mapping)'),
            ('UX-исследования, Глубокие интервью', 'UX Research, Deep Interviews'),
            ('Проектирование модели клиентского сервиса', 'Customer Service Model Design'),
            ('Работа с обратной связью, решение претензий', 'Feedback Management, Complaint Resolution'),
            ('Разработка СОП', 'SOP Development'),
            ('Проведение тренингов по качеству обслуживания', 'Service Quality Training')
        ]
        for i, (name_ru, name_en) in enumerate(skills_cx):
            Skill.objects.create(category=cx, name_ru=name_ru, name_en=name_en, order=i+1)
            
        # Аналитика и Маркетинг
        analytics = SkillCategory.objects.create(
            name_ru='Аналитика и Маркетинг',
            name_en='Analytics & Marketing',
            order=3
        )
        skills_analytics = [
            ('Бизнес-аналитика', 'Business Analysis'),
            ('Выявление потребностей клиента, формирование ЦА', 'Client Needs Assessment, Target Audience Definition'),
            ('Анализ и обработка клиентских баз', 'Customer Database Analysis & Processing'),
            ('Стратегический маркетинг', 'Strategic Marketing'),
            ('Разработка маркетинговых стратегий', 'Marketing Strategy Development'),
            ('Анализ конкурентов', 'Competitor Analysis')
        ]
        for i, (name_ru, name_en) in enumerate(skills_analytics):
            Skill.objects.create(category=analytics, name_ru=name_ru, name_en=name_en, order=i+1)
            
        # Инструменты и Технологии
        tools = SkillCategory.objects.create(
            name_ru='Инструменты и Технологии',
            name_en='Tools & Technologies',
            order=4
        )
        skills_tools = [
            ('Miro, Figma, Notion, Google Workspace', 'Miro, Figma, Notion, Google Workspace'),
            ('Python (базовый)', 'Python (basic)'),
            ('CRM (Битрикс24)', 'CRM (Bitrix24)'),
            ('Системы веб-аналитики', 'Web Analytics Systems'),
            ('CMS', 'CMS')
        ]
        for i, (name_ru, name_en) in enumerate(skills_tools):
            Skill.objects.create(category=tools, name_ru=name_ru, name_en=name_en, order=i+1)
        
        self.stdout.write(self.style.SUCCESS('Категории навыков и навыки созданы'))
        
        # Очищаем существующий опыт работы для демонстрации
        Experience.objects.all().delete()
        
        # Создаем опыт работы
        experiences = [
            {
                'title_ru': 'Тьютор (Веб-разработка)',
                'title_en': 'Tutor (Web Development)',
                'company_ru': 'Московский финансово-промышленный университет "Синергия"',
                'company_en': 'Moscow University for Industry and Finance "Synergy"',
                'period_ru': 'Фев 2022 – Июн 2024 (2 г. 5 мес.)',
                'period_en': 'Feb 2022 – Jun 2024 (2 yrs 5 mos)',
                'location_ru': 'Москва',
                'location_en': 'Moscow',
                'responsibilities_ru': """Проверка практических работ студентов, оценка соответствия стандартам.
Предоставление конструктивной обратной связи и ревью кода.
Разработка домашних заданий и проверочных тестов.
Внедрение лучших учебных практик.""",
                'responsibilities_en': """Reviewing student practical work, assessing compliance with standards.
Providing constructive feedback and code reviews.
Developing homework assignments and assessment tests.
Implementing best teaching practices.""",
                'achievements_ru': """Внедрил персонализированный подход к обучению.
Получил высокий уровень положительных отзывов от студентов за своевременную проверку и поддержку.""",
                'achievements_en': """Implemented a personalized approach to teaching.
Received a high level of positive feedback from students for timely reviews and support.""",
                'order': 1
            },
            {
                'title_ru': 'Менеджер по подготовке проектов',
                'title_en': 'Project Preparation Manager',
                'company_ru': 'Willstream',
                'company_en': 'Willstream',
                'period_ru': 'Авг 2023 – Ноя 2023 (4 мес.)',
                'period_en': 'Aug 2023 – Nov 2023 (4 mos)',
                'location_ru': 'Москва',
                'location_en': 'Moscow',
                'responsibilities_ru': """Выявление потребностей клиента, помощь в формировании ЦА.
Содействие в разработке ТЗ для сценариев обзвона.
Составление и обработка клиентских баз.
Разработка сценариев для обзвона.""",
                'responsibilities_en': """Identifying client needs, assisting in defining target audience.
Assisting in developing technical specifications for call scripts.
Compiling and processing client databases.
Developing call scripts.""",
                'achievements_ru': """Эффективно выявлял потребности клиентов для разработки ТЗ.
Сократил время на подготовку клиентских баз на 20% за счет оптимизации методов обработки.""",
                'achievements_en': """Effectively identified client needs for technical specification development.
Reduced client database preparation time by 20% through optimized processing methods.""",
                'order': 2
            }
        ]
        
        for exp_data in experiences:
            Experience.objects.create(**exp_data)
        self.stdout.write(self.style.SUCCESS('Опыт работы создан'))
        
        # Очищаем существующее образование для демонстрации
        Education.objects.all().delete()
        
        # Создаем образование
        educations = [
            {
                'degree_ru': 'Магистр, Управление клиентским опытом и инновации в сервисе',
                'degree_en': 'Master\'s Degree, Customer Experience Management and Service Innovation',
                'institution_ru': 'Российский университет дружбы народов (РУДН), Высшая школа управления, Москва',
                'institution_en': 'Peoples\' Friendship University of Russia (RUDN), Higher School of Management, Moscow',
                'year_ru': '2023',
                'year_en': '2023',
                'order': 1,
                'is_course_section': False
            },
            {
                'degree_ru': 'Специалитет (неоконченное)',
                'degree_en': 'Specialist Degree (incomplete)',
                'institution_ru': 'Красноярский институт железнодорожного транспорта',
                'institution_en': 'Krasnoyarsk Institute of Railway Transport',
                'year_ru': '2020',
                'year_en': '2020',
                'order': 2,
                'is_course_section': False
            },
            {
                'degree_ru': 'Курсы повышения квалификации / Дополнительное образование:',
                'degree_en': 'Professional Development Courses / Additional Education:',
                'institution_ru': '',
                'institution_en': '',
                'year_ru': '',
                'year_en': '',
                'order': 3,
                'is_course_section': True
            }
        ]
        
        for edu_data in educations:
            Education.objects.create(**edu_data)
        
        # Создаем курсы (для раздела дополнительного образования)
        course_section = Education.objects.get(is_course_section=True)
        courses = [
            {
                'name_ru': 'Python-разработка (Синергия, 2024)',
                'name_en': 'Python Development (Synergy, 2024)',
                'order': 1
            },
            {
                'name_ru': 'Менеджмент проектов (Синергия, 2024)',
                'name_en': 'Project Management (Synergy, 2024)',
                'order': 2
            },
            {
                'name_ru': 'Директор по клиентскому сервису (Нетология, 2023)',
                'name_en': 'Customer Service Director (Netology, 2023)',
                'order': 3
            }
        ]
        
        for course_data in courses:
            course_section.courses.create(**course_data)
        
        self.stdout.write(self.style.SUCCESS('Образование и курсы созданы'))
        
        # Очищаем существующие проекты для демонстрации
        Project.objects.all().delete()
        
        # Создаем проекты
        projects = [
            {
                'title_ru': 'Комплексная Модель Клиентского Сервиса (Отель)',
                'title_en': 'Comprehensive Customer Service Model (Hotel)',
                'description_ru': 'Разработка и внедрение модели для улучшения взаимодействия с гостями и повышения удовлетворенности. Результат: снижение времени обработки отзывов в 2 раза, достижение KPI.',
                'description_en': 'Developed and implemented a model to improve guest interaction and satisfaction. Result: reduced feedback processing time by 50%, achieved KPIs.',
                'order': 1
            },
            {
                'title_ru': 'Внедрение CRM Битрикс24 (Отель)',
                'title_en': 'Bitrix24 CRM Implementation (Hotel)',
                'description_ru': 'Ведение проекта по внедрению CRM-системы для оптимизации работы с клиентской базой и улучшения внутренних процессов.',
                'description_en': 'Managed the implementation project of a CRM system to optimize client database management and improve internal processes.',
                'order': 2
            },
            {
                'title_ru': 'Коммерческий Запуск Сайта (IT)',
                'title_en': 'Commercial Website Launch (IT)',
                'description_ru': 'Управление проектом по созданию и запуску сайта для клиента, включая последующее ежемесячное обслуживание.',
                'description_en': 'Managed the project for creating and launching a client\'s website, including subsequent monthly maintenance.',
                'order': 3
            },
            {
                'title_ru': 'Внедрение Agile (IT)',
                'title_en': 'Agile Implementation (IT)',
                'description_ru': 'Реализация методологии Agile для сокращения времени выполнения задач, улучшения коммуникации и повышения гибкости управления проектами.',
                'description_en': 'Implemented Agile methodology to reduce task completion times, improve communication, and increase project management flexibility.',
                'order': 4
            }
        ]
        
        for project_data in projects:
            Project.objects.create(**project_data)
        
        self.stdout.write(self.style.SUCCESS('Проекты созданы'))
        
        self.stdout.write(self.style.SUCCESS('Демонстрационный контент успешно создан!'))