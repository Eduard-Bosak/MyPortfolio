from django.contrib import admin
from .models import (
    HeroSection, AboutSection, ContactInfo,
    Experience, Education, Course, Project, 
    SkillCategory, Skill
)

# --- Настройка Singleton моделей (Hero, About, Contact) ---
# Эти модели должны иметь только одну запись в БД.
# Мы запрещаем добавление новых и удаление существующих записей.

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Запрещаем добавление новых записей, т.к. это синглтон
        return False

    def has_delete_permission(self, request, obj=None):
        # Запретить удаление
        return False

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# --- Настройка остальных моделей ---

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    ordering = ['order']

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_en', 'order')
    list_editable = ('order',)
    inlines = [SkillInline]

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'company_ru', 'period_ru', 'order')
    list_editable = ('order',)
    search_fields = ('title_ru', 'title_en', 'company_ru', 'company_en', 'responsibilities_ru', 'achievements_ru')

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1
    exclude = ('order',)
    ordering = ['order']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree_ru', 'institution_ru', 'year_ru', 'is_course_section', 'order')
    list_editable = ('order', 'is_course_section')
    list_filter = ('is_course_section',)
    search_fields = ('degree_ru', 'degree_en', 'institution_ru', 'institution_en')
    inlines = [CourseInline]

    # Опционально: Динамическое отображение инлайнов
    # def get_inline_instances(self, request, obj=None):
    #     if obj and obj.is_course_section:
    #         return [inline(self.model, self.admin_site) for inline in self.inlines]
    #     return []

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'order')
    list_editable = ('order',)
    search_fields = ('title_ru', 'title_en', 'description_ru', 'description_en')

# Модель Skill и Course регистрировать отдельно не нужно,
# так как они редактируются внутри SkillCategory и Education соответственно.
# Но если нужно отдельное управление ими, можно раскомментировать:
# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ('name_ru', 'category', 'order')
#     list_editable = ('order',)
#     list_filter = ('category',)

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('name_ru', 'education_entry', 'order')
#     list_editable = ('order',)
#     list_filter = ('education_entry',)