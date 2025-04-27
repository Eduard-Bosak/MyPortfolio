import os
import re
from django.core.management.base import BaseCommand
from striprtf.striprtf import rtf_to_text
from content.models import (
    AboutSection, ContactInfo, HeroSection,
    Experience, Education, SkillCategory, Skill
)

class Command(BaseCommand):
    help = "Импорт данных из резюме (RTF) в модели Django"

    def add_arguments(self, parser):
        parser.add_argument('rtf_path', type=str, help='Путь к файлу резюме в формате RTF')

    def handle(self, *args, **options):
        rtf_path = options['rtf_path']
        if not os.path.exists(rtf_path):
            self.stderr.write(f"Файл {rtf_path} не найден!")
            return

        # Читаем и конвертируем RTF в текст
        text = self.read_rtf(rtf_path)
        self.stdout.write(self.style.SUCCESS("=== Извлечённый текст резюме ==="))
        self.stdout.write(text[:1000] + "\n...")  # выводим первые 1000 символов

        # Парсинг основных разделов
        email, phone, location = self.parse_contacts(text)
        about_text = self.parse_about(text)
        experiences = self.parse_experiences(text)
        educations = self.parse_educations(text)
        skills = self.parse_skills(text)
        recommendations = self.parse_recommendations(text)
        personal_qualities = self.parse_personal_qualities(text)

        # Вывод распознанных данных в консоль
        self.stdout.write(f"\nКонтакты: email={email}, телефон={phone}, локация={location}")
        self.stdout.write("\nСекция 'О себе':")
        self.stdout.write(about_text[:300] + "\n...")
        self.stdout.write(f"\nНайдено {len(experiences)} записей опыта работы.")
        self.stdout.write(f"\nНайдено {len(educations)} записей образования.")
        self.stdout.write(f"\nНайдено {len(skills)} навыков: " + ", ".join(skills))
        if recommendations:
            self.stdout.write("\nРекомендации:")
            self.stdout.write(recommendations)
        if personal_qualities:
            self.stdout.write("\nЛичные качества:")
            self.stdout.write(personal_qualities)

        # Сохранение данных в БД

        # Обновляем контактную информацию
        contact = ContactInfo.load()
        if email:
            contact.email = email
        if phone:
            contact.phone = phone
        if location:
            contact.location_ru = location
        contact.save()
        self.stdout.write(self.style.SUCCESS("Контактная информация обновлена."))

        # Обновляем секцию "О себе"
        if about_text:
            about = AboutSection.load()
            about.description_ru = about_text.strip()
            about.save()
            self.stdout.write(self.style.SUCCESS("Секция 'О себе' обновлена."))
        else:
            self.stdout.write("Секция 'О себе' не найдена.")

        # Создаём записи опыта работы
        for exp_data in experiences:
            exp = Experience.objects.create(
                period_ru=exp_data.get('period_ru', ''),
                company_ru=exp_data.get('company_ru', 'Не указано'),
                title_ru=exp_data.get('title_ru', 'Не указано'),
                responsibilities_ru=exp_data.get('responsibilities_ru', ''),
                achievements_ru=exp_data.get('achievements_ru', ''),
                location_ru=exp_data.get('location_ru', ''),
            )
            self.stdout.write(self.style.SUCCESS(f"Создан Experience: {exp.title_ru} / {exp.company_ru}"))

        # Создаём записи образования
        for edu_data in educations:
            edu = Education.objects.create(
                year_ru=edu_data.get('year_ru', ''),
                institution_ru=edu_data.get('institution_ru', 'Не указано'),
                degree_ru=edu_data.get('degree_ru', 'Не указано'),
            )
            self.stdout.write(self.style.SUCCESS(f"Создан Education: {edu.degree_ru} / {edu.institution_ru}"))

        # Навыки: создаём категорию "Из резюме" и записываем все навыки
        if skills:
            cat, _ = SkillCategory.objects.get_or_create(name_ru="Из резюме", defaults={'name_en': 'From resume'})
            for i, s in enumerate(skills, start=1):
                Skill.objects.create(
                    category=cat,
                    name_ru=s,
                    name_en=s,
                    order=i,
                )
            self.stdout.write(self.style.SUCCESS(f"Добавлено навыков: {len(skills)}"))

        self.stdout.write(self.style.SUCCESS("Импорт завершён!"))

    # ------------------- Вспомогательные функции -------------------

    def read_rtf(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            rtf_data = f.read()
        return rtf_to_text(rtf_data)

    def parse_contacts(self, text):
        # Поиск email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else ''
        # Поиск телефона
        phone_match = re.search(r'\+?\d[\d\s\(\)\-]{7,}', text)
        phone = phone_match.group(0) if phone_match else ''
        # Поиск локации (строка после "Проживает:")
        loc_match = re.search(r'Проживает:\s*(.+)', text)
        location = loc_match.group(1).strip() if loc_match else ''
        return email, phone, location

    def parse_about(self, text):
        # Ищем блок "О себе" или "Обо мне" — от заголовка до следующего раздела
        pattern = r'(О себе|Обо мне)[\s:]*\n(.*?)(?=\n(?:Опыт работы|Образование|Навыки|Рекомендации|Дополнительная информация)|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(2).strip()
        return ''

    def parse_experiences(self, text):
        # Ищем блок "Опыт работы" — от слова "Опыт работы" до начала следующего крупного раздела
        pattern_block = r'Опыт работы\s*(—\s*\S+)?\s*\n(.*?)(?=\n(?:Образование|Повышение квалификации|Дополнительная информация)|$)'
        match = re.search(pattern_block, text, re.DOTALL | re.IGNORECASE)
        if not match:
            return []
        block = match.group(2).strip()
        # Разбиваем блок по записям, предполагая, что каждая запись начинается с диапазона дат
        date_pattern = r'((?:Январь|Февраль|Март|Апрель|Май|Июнь|Июль|Август|Сентябрь|Октябрь|Ноябрь|Декабрь)\s+\d{4}\s+—\s+(?:Январь|Февраль|Март|Апрель|Май|Июнь|Июль|Август|Сентябрь|Октябрь|Ноябрь|Декабрь)\s+\d{4})'
        parts = re.split(date_pattern, block)
        experiences = []
        # Ожидается формат: [вводный текст, period, content, period, content, ...]
        for i in range(1, len(parts), 2):
            period = parts[i].strip()
            content = parts[i+1].strip() if i+1 < len(parts) else ''
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            company = lines[0] if lines else 'Не указано'
            title = "Не указано"
            for line in lines:
                if any(keyword in line for keyword in ['Тьютор', 'Менеджер', 'Tutor']):
                    title = line
                    break
            responsibilities = ""
            achievements = ""
            if "Основные обязанности" in content:
                parts_resp = re.split(r'Основные обязанности[:]?+', content, flags=re.IGNORECASE)
                if len(parts_resp) > 1:
                    subparts = re.split(r'Достижения[:]?+', parts_resp[1], flags=re.IGNORECASE)
                    responsibilities = subparts[0].strip()
                    if len(subparts) > 1:
                        achievements = subparts[1].strip()
            experiences.append({
                'period_ru': period,
                'company_ru': company,
                'title_ru': title,
                'responsibilities_ru': responsibilities,
                'achievements_ru': achievements,
                'location_ru': '',  # если можно извлечь город, добавить логику здесь
            })
        return experiences

    def parse_educations(self, text):
        # Ищем блок "Образование" до следующих разделов (например, "Повышение квалификации")
        pattern_block = r'Образование\s*\n(.*?)(?=\n(?:Повышение квалификации|Тесты|Электронные сертификаты|Навыки|О себе)|$)'
        match = re.search(pattern_block, text, re.DOTALL | re.IGNORECASE)
        if not match:
            return []
        block = match.group(1).strip()
        # Разбиваем по записям: каждая запись начинается с года (4 цифры)
        entries = re.split(r'\n(?=\d{4}\b)', block)
        results = []
        for entry in entries:
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            if not lines:
                continue
            year = lines[0]
            institution = lines[1] if len(lines) > 1 else "Не указано"
            degree = "Не указано"
            for line in lines:
                if re.search(r'(Магистр|Бакалавр|Специалитет|Курсы)', line, re.IGNORECASE):
                    degree = line
                    break
            results.append({
                'year_ru': year,
                'institution_ru': institution,
                'degree_ru': degree,
            })
        return results

    def parse_skills(self, text):
        # Ищем блок "Навыки" — от слова "Навыки" до раздела "Дополнительная информация" или конца
        pattern = r'Навыки\s*\n(.*?)(?=\n(?:Дополнительная информация|Обо мне)|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not match:
            return []
        skills_block = match.group(1).strip()
        # Разбиваем по двойным пробелам или переводам строк
        skill_list = re.split(r'\s{2,}|\n', skills_block)
        skill_list = [s.strip('• \n\r\t-') for s in skill_list if s.strip()]
        skill_list = [s for s in skill_list if len(s) > 2]
        return skill_list

    def parse_recommendations(self, text):
        # Ищем раздел "Рекомендации" — предполагаем, что он начинается со слова "Рекомендации"
        pattern = r'Рекомендации\s*\n(.*?)(?=\n|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ''

    def parse_personal_qualities(self, text):
        # Ищем раздел "Обо мне" или "Личные качества" после заголовка "Обо мне" (если есть)
        pattern = r'Обо мне\s*\n(Личные качества:.*?)(?=\nО себе:|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ''
