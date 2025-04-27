from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from portfolio_cms.views import home_view
from content.views import (
    PortfolioView,
    HeroSectionViewSet, AboutSectionViewSet, ContactInfoViewSet,
    ExperienceViewSet, EducationViewSet, ProjectViewSet, 
    SkillCategoryViewSet, SkillViewSet
)

# Настраиваем маршруты для API
router = routers.DefaultRouter()
router.register(r'hero', HeroSectionViewSet)
router.register(r'about', AboutSectionViewSet)
router.register(r'contact', ContactInfoViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'skill-categories', SkillCategoryViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Используем новое представление из portfolio_cms
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/portfolio/', PortfolioView.as_view(), name='api-portfolio'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Wagtail маршруты
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
] 

# Добавляем обработку медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
