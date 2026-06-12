from django import forms
from urllib.parse import urlparse
from django.core.exceptions import ValidationError

from .models import Project


def validate_github_url(value):
    """Проверяет, что ссылка ведёт на GitHub."""
    if not value:
        return
    parsed = urlparse(value)
    if not parsed.scheme or 'github.com' not in parsed.netloc.lower():
        raise ValidationError('Ссылка должна вести на Github')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        validate_github_url(url)
        return url