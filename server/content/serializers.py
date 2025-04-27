# content/serializers.py
from rest_framework import serializers
from .models import (
    HeroSection, AboutSection, ContactInfo,
    Experience, Education, Course, Project, SkillCategory, Skill, UiText
)

class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'

class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = SkillCategory
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Education
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'

class UiTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = UiText
        fields = '__all__'

# Сводный сериализатор для отображения всех данных портфолио
class PortfolioSerializer(serializers.Serializer):
    hero = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    skill_categories = serializers.SerializerMethodField()
    ui_texts = serializers.SerializerMethodField()
    
    def get_hero(self, obj):
        hero = HeroSection.objects.first()
        return HeroSectionSerializer(hero).data if hero else None
    
    def get_about(self, obj):
        about = AboutSection.objects.first()
        return AboutSectionSerializer(about).data if about else None
    
    def get_contact(self, obj):
        contact = ContactInfo.objects.first()
        return ContactInfoSerializer(contact).data if contact else None
    
    def get_experiences(self, obj):
        experiences = Experience.objects.all().order_by('order')
        return ExperienceSerializer(experiences, many=True).data
    
    def get_educations(self, obj):
        educations = Education.objects.all().order_by('order')
        return EducationSerializer(educations, many=True).data
    
    def get_projects(self, obj):
        projects = Project.objects.all().order_by('order')
        return ProjectSerializer(projects, many=True).data
    
    def get_skill_categories(self, obj):
        categories = []
        for category in SkillCategory.objects.all().order_by('order'):
            skills = Skill.objects.filter(category=category).order_by('order')
            categories.append({
                "id": category.id,
                "name_ru": category.name_ru,
                "name_en": category.name_en,
                "order": category.order,
                "skills": SkillSerializer(skills, many=True).data
            })
        return categories
    
    def get_ui_texts(self, obj):
        ui_text = UiText.load()
        return UiTextSerializer(ui_text).data