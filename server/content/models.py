from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Модель для хранения общих текстовых блоков (Hero, About)
class SingletonModel(models.Model):
    """Абстрактная модель, гарантирующая только один экземпляр."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1  # Устанавливаем первичный ключ в 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass # Запрещаем удаление

    @classmethod
    def load(cls):
        # Получаем или создаем единственный экземпляр
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class HeroSection(SingletonModel):
    title_ru = models.CharField("Заголовок (RU)", max_length=200, default="Привет! Я Эдуард Босак")
    title_en = models.CharField("Заголовок (EN)", max_length=200, default="Hi! I'm Eduard Bosak")
    subtitle_ru = models.CharField("Подзаголовок (RU)", max_length=300, default="Менеджер проектов и клиентского сервиса")
    subtitle_en = models.CharField("Подзаголовок (EN)", max_length=300, default="Project and Customer Experience Manager")
    small_subtitle_ru = models.CharField("Малый подзаголовок (RU)", max_length=300, blank=True, default="Открыт к переезду в Санкт-Петербург и командировкам.")
    small_subtitle_en = models.CharField("Малый подзаголовок (EN)", max_length=300, blank=True, default="Open to relocation to St. Petersburg and business trips.")

    class Meta:
        verbose_name = "Секция Hero"
        verbose_name_plural = "Секция Hero"

    def __str__(self):
        return "Настройки секции Hero"

class AboutSection(SingletonModel):
    description_ru = models.TextField("Описание (RU)", default="Текст обо мне на русском...")
    description_en = models.TextField("Описание (EN)", default="About me text in English...")
    # Можно добавить ImageField для фото, если нужно
    # profile_picture = models.ImageField("Фото профиля", upload_to='profile/', blank=True, null=True)

    class Meta:
        verbose_name = "Секция 'Обо мне'"
        verbose_name_plural = "Секция 'Обо мне'"

    def __str__(self):
        return "Настройки секции 'Обо мне'"

# --- Навыки ---
class SkillCategory(models.Model):
    name_ru = models.CharField("Название категории (RU)", max_length=100)
    name_en = models.CharField("Название категории (EN)", max_length=100)
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Чем меньше число, тем выше категория")

    class Meta:
        verbose_name = "Категория навыков"
        verbose_name_plural = "Категории навыков"
        ordering = ['order']

    def __str__(self):
        return self.name_ru

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE, verbose_name="Категория")
    name_ru = models.CharField("Название навыка (RU)", max_length=150)
    name_en = models.CharField("Название навыка (EN)", max_length=150)
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Чем меньше число, тем выше навык внутри категории")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.category.name_ru} - {self.name_ru}"

# --- Опыт работы ---
class Experience(models.Model):
    title_ru = models.CharField("Должность (RU)", max_length=200)
    title_en = models.CharField("Должность (EN)", max_length=200)
    company_ru = models.CharField("Компания (RU)", max_length=200)
    company_en = models.CharField("Компания (EN)", max_length=200)
    period_ru = models.CharField("Период (RU)", max_length=100, help_text="Например: Фев 2022 – Июн 2024 (2 г. 5 мес.)")
    period_en = models.CharField("Период (EN)", max_length=100, help_text="Example: Feb 2022 – Jun 2024 (2 yrs 5 mos)")
    location_ru = models.CharField("Местоположение (RU)", max_length=100, blank=True)
    location_en = models.CharField("Местоположение (EN)", max_length=100, blank=True)
    responsibilities_ru = models.TextField("Обязанности (RU)", help_text="Каждый пункт с новой строки, можно использовать markdown или html")
    responsibilities_en = models.TextField("Обязанности (EN)", help_text="Each item on a new line, markdown or html can be used")
    achievements_ru = models.TextField("Достижения (RU)", blank=True, help_text="Каждый пункт с новой строки")
    achievements_en = models.TextField("Достижения (EN)", blank=True, help_text="Each item on a new line")
    order = models.PositiveIntegerField("Порядок", default=0, help_text="Чем меньше число, тем выше позиция в списке")

    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"
        ordering = ['order']

    def __str__(self):
        return f"{self.title_ru} в {self.company_ru}"

# --- Образование ---
class Education(models.Model):
    degree_ru = models.CharField("Степень/Название (RU)", max_length=250)
    degree_en = models.CharField("Степень/Название (EN)", max_length=250)
    institution_ru = models.CharField("Учебное заведение (RU)", max_length=300)
    institution_en = models.CharField("Учебное заведение (EN)", max_length=300)
    year_ru = models.CharField("Год окончания (RU)", max_length=50)
    year_en = models.CharField("Год окончания (EN)", max_length=50)
    is_course_section = models.BooleanField("Это секция доп. курсов?", default=False, help_text="Отметьте, если это заголовок для списка курсов")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Образование / Квалификация"
        verbose_name_plural = "Образование и Квалификации"
        ordering = ['order']

    def __str__(self):
        return self.degree_ru

class Course(models.Model):
    # Связываем с записью Education, которая помечена как is_course_section
    # Или можно сделать отдельную модель для заголовка курсов
    education_entry = models.ForeignKey(Education, related_name='courses', on_delete=models.CASCADE, verbose_name="Раздел образования", limit_choices_to={'is_course_section': True})
    name_ru = models.CharField("Название курса (RU)", max_length=200)
    name_en = models.CharField("Название курса (EN)", max_length=200)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Дополнительный курс"
        verbose_name_plural = "Дополнительные курсы"
        ordering = ['order']

    def __str__(self):
        return self.name_ru


# --- Проекты ---
class Project(models.Model):
    title_ru = models.CharField("Название проекта (RU)", max_length=200)
    title_en = models.CharField("Название проекта (EN)", max_length=200)
    description_ru = models.TextField("Описание (RU)")
    description_en = models.TextField("Описание (EN)")
    # Можно добавить поля для ссылки, изображения и т.д.
    # link = models.URLField("Ссылка на проект", blank=True)
    # image = models.ImageField("Изображение проекта", upload_to='projects/', blank=True, null=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['order']

    def __str__(self):
        return self.title_ru

# --- Контакты ---
class ContactInfo(SingletonModel):
    email = models.EmailField("Email", default="info@eduardbosak.ru")
    phone = models.CharField("Телефон", max_length=30, default="+7 (995) 079-97-77")
    location_ru = models.CharField("Местоположение (RU)", max_length=150, default="Москва, Россия (м. Красногвардейская)")
    location_en = models.CharField("Местоположение (EN)", max_length=150, default="Moscow, Russia (m. Krasnogvardeyskaya)")
    # Можно добавить поля для соцсетей
    # linkedin_url = models.URLField("LinkedIn URL", blank=True)
    # telegram_username = models.CharField("Telegram Username", max_length=100, blank=True)

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return "Контактная информация"

# --- UI Texts Model ---
class UiText(SingletonModel):
    """Модель для хранения интерфейсных текстов сайта"""
    # Меню навигации
    nav_about_ru = models.CharField("Меню: Обо мне (RU)", max_length=50, default="Обо мне")
    nav_about_en = models.CharField("Меню: Обо мне (EN)", max_length=50, default="About")
    nav_skills_ru = models.CharField("Меню: Навыки (RU)", max_length=50, default="Навыки")
    nav_skills_en = models.CharField("Меню: Навыки (EN)", max_length=50, default="Skills")
    nav_experience_ru = models.CharField("Меню: Опыт (RU)", max_length=50, default="Опыт")
    nav_experience_en = models.CharField("Меню: Опыт (EN)", max_length=50, default="Experience")
    nav_education_ru = models.CharField("Меню: Образование (RU)", max_length=50, default="Образование")
    nav_education_en = models.CharField("Меню: Образование (EN)", max_length=50, default="Education")
    nav_projects_ru = models.CharField("Меню: Проекты (RU)", max_length=50, default="Проекты")
    nav_projects_en = models.CharField("Меню: Проекты (EN)", max_length=50, default="Projects")
    nav_contact_ru = models.CharField("Меню: Контакты (RU)", max_length=50, default="Контакты")
    nav_contact_en = models.CharField("Меню: Контакты (EN)", max_length=50, default="Contact")
    
    # Кнопки призыва к действию
    cta_projects_ru = models.CharField("Кнопка: Мои проекты (RU)", max_length=50, default="Мои проекты")
    cta_projects_en = models.CharField("Кнопка: Мои проекты (EN)", max_length=50, default="My Projects")
    cta_contact_ru = models.CharField("Кнопка: Связаться (RU)", max_length=50, default="Связаться со мной")
    cta_contact_en = models.CharField("Кнопка: Связаться (EN)", max_length=50, default="Contact Me")
    
    # Заголовки секций
    section_about_ru = models.CharField("Заголовок: Обо мне (RU)", max_length=50, default="Обо мне")
    section_about_en = models.CharField("Заголовок: Обо мне (EN)", max_length=50, default="About Me")
    section_skills_ru = models.CharField("Заголовок: Навыки (RU)", max_length=50, default="Ключевые навыки")
    section_skills_en = models.CharField("Заголовок: Навыки (EN)", max_length=50, default="Key Skills")
    section_experience_ru = models.CharField("Заголовок: Опыт (RU)", max_length=50, default="Опыт работы")
    section_experience_en = models.CharField("Заголовок: Опыт (EN)", max_length=50, default="Work Experience")
    section_education_ru = models.CharField("Заголовок: Образование (RU)", max_length=50, default="Образование")
    section_education_en = models.CharField("Заголовок: Образование (EN)", max_length=50, default="Education")
    section_projects_ru = models.CharField("Заголовок: Проекты (RU)", max_length=50, default="Проекты")
    section_projects_en = models.CharField("Заголовок: Проекты (EN)", max_length=50, default="Projects")
    section_contact_ru = models.CharField("Заголовок: Контакты (RU)", max_length=50, default="Контакты")
    section_contact_en = models.CharField("Заголовок: Контакты (EN)", max_length=50, default="Contact")
    
    # Метки в разделах
    label_responsibilities_ru = models.CharField("Метка: Обязанности (RU)", max_length=50, default="Обязанности:")
    label_responsibilities_en = models.CharField("Метка: Обязанности (EN)", max_length=50, default="Responsibilities:")
    label_achievements_ru = models.CharField("Метка: Достижения (RU)", max_length=50, default="Достижения:")
    label_achievements_en = models.CharField("Метка: Достижения (EN)", max_length=50, default="Achievements:")
    label_graduation_year_ru = models.CharField("Метка: Год окончания (RU)", max_length=50, default="Год окончания:")
    label_graduation_year_en = models.CharField("Метка: Год окончания (EN)", max_length=50, default="Graduation Year:")
    label_preferred_contact_ru = models.CharField("Метка: Предпочтительный способ связи (RU)", max_length=100, default="(Предпочтительный способ связи)")
    label_preferred_contact_en = models.CharField("Метка: Предпочтительный способ связи (EN)", max_length=100, default="(Preferred contact method)")
    
    # Копирайт
    copyright_text_ru = models.CharField("Копирайт (RU)", max_length=100, default="Все права защищены.")
    copyright_text_en = models.CharField("Копирайт (EN)", max_length=100, default="All rights reserved.")

    class Meta:
        verbose_name = "Тексты интерфейса"
        verbose_name_plural = "Тексты интерфейса"

    def __str__(self):
        return "Тексты интерфейса сайта"