# content/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from rest_framework import viewsets, permissions, views, response
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import re
from .models import (
    HeroSection, AboutSection, ContactInfo,
    Experience, Education, Project, 
    SkillCategory, Skill, UiText
)
from .serializers import (
    HeroSectionSerializer, AboutSectionSerializer, ContactInfoSerializer,
    ExperienceSerializer, EducationSerializer, ProjectSerializer,
    SkillCategorySerializer, SkillSerializer, PortfolioSerializer
)

def home_view(request):
    """
    Отображает главную страницу сайта с данными из базы данных
    """
    # Получаем данные для всех секций
    hero = HeroSection.objects.first()
    about = AboutSection.objects.first()
    contact = ContactInfo.objects.first()
    
    experiences = Experience.objects.all().order_by('order')
    educations = Education.objects.all().order_by('order')
    projects = Project.objects.all().order_by('order')
    
    # Получаем категории навыков с их навыками
    skill_categories = SkillCategory.objects.all().order_by('order')
    
    # Получаем тексты интерфейса
    ui_texts = UiText.load()
    
    # Создаем контекст для передачи в шаблон
    context = {
        'hero': hero,
        'about': about,
        'contact': contact,
        'experiences': experiences,
        'educations': educations,
        'projects': projects,
        'skill_categories': skill_categories,
        'ui': ui_texts,  # Добавляем тексты UI в контекст
    }
    
    return render(request, 'index.html', context)

# API вьюсеты
class HeroSectionViewSet(viewsets.ModelViewSet):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self):
        return HeroSection.load()

class AboutSectionViewSet(viewsets.ModelViewSet):
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self):
        return AboutSection.load()

class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self):
        return ContactInfo.load()

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by('order')
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAdminUser]

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().order_by('order')
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAdminUser]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('order')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]

class SkillCategoryViewSet(viewsets.ModelViewSet):
    queryset = SkillCategory.objects.all().order_by('order')
    serializer_class = SkillCategorySerializer
    permission_classes = [permissions.IsAdminUser]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('order')
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAdminUser]

# API для получения всех данных портфолио сразу
class PortfolioView(APIView):
    def get(self, request, format=None):
        hero = HeroSection.objects.first()
        about = AboutSection.objects.first()
        contact = ContactInfo.objects.first()
        
        experiences = Experience.objects.all().order_by('order')
        educations = Education.objects.all().order_by('order')
        projects = Project.objects.all().order_by('order')
        
        skill_categories = []
        for category in SkillCategory.objects.all().order_by('order'):
            skills = Skill.objects.filter(category=category).order_by('order')
            skill_categories.append({
                "id": category.id,
                "name_ru": category.name_ru,
                "name_en": category.name_en,
                "order": category.order,
                "skills": SkillSerializer(skills, many=True).data
            })
        
        data = {
            "hero": HeroSectionSerializer(hero).data if hero else None,
            "about": AboutSectionSerializer(about).data if about else None,
            "contact": ContactInfoSerializer(contact).data if contact else None,
            "experiences": ExperienceSerializer(experiences, many=True).data,
            "educations": EducationSerializer(educations, many=True).data,
            "projects": ProjectSerializer(projects, many=True).data,
            "skill_categories": skill_categories
        }
        
        return Response(data)
