from wagtail import hooks
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

@hooks.register('construct_page_editor_form')
def override_page_editor_form(instance, form):
    # Отключаем валидацию формы принудительно
    form.is_valid = lambda: True
    return form

@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def bypass_validation(request, page):
    # Принудительно устанавливаем is_valid в True для всех форм
    if hasattr(request, 'form'):
        request.form.is_valid = lambda: True
    return None

@hooks.register('insert_editor_js')
def disable_validation_js():
    js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        // Скрываем кнопку предпросмотра
        const previewButton = document.querySelector("[data-action='preview']");
        if (previewButton) previewButton.style.display = "none";
        // Отключаем HTML5-валидацию при сабмите
        const form = document.querySelector("#page-edit-form");
        if (form) {
            form.addEventListener('submit', function() {
                form.querySelectorAll('input,textarea,select').forEach(i => i.required = false);
            });
        }
    });
    </script>
    """
    return mark_safe(js)

@hooks.register('before_serve_page')
def allow_serve_any_page(page, request, serve_args, serve_kwargs):
    # Разрешаем обслуживание страницы даже если есть проблемы с валидацией
    return None