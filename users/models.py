import random
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .managers import UserManager

AVATAR_COLORS = [
    '#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5',
    '#2196F3', '#009688', '#4CAF50', '#FF9800', '#795548',
]


def generate_avatar(name):
    color = random.choice(AVATAR_COLORS)
    size = 200
    image = Image.new('RGB', (size, size), color)
    draw = ImageDraw.Draw(image)
    letter = (name or '?')[0].upper()

    
    font = None
    for font_path in (
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        'C:/Windows/Fonts/arial.ttf',
    ):
        try:
            font = ImageFont.truetype(font_path, 100)
            break
        except (IOError, OSError):
            continue
    
    if font is None:
        font = ImageFont.load_default()


    try:
        bbox = draw.textbbox((0, 0), letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (size - w) / 2 - bbox[0]
        y = (size - h) / 2 - bbox[1]
    except AttributeError:
        w, h = draw.textsize(letter, font=font)
        x, y = (size - w) / 2, (size - h) / 2

    draw.text((x, y), letter, fill='white', font=font)

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{letter.lower()}_avatar.png')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    name = models.CharField('Имя', max_length=124)
    surname = models.CharField('Фамилия', max_length=124)
    avatar = models.ImageField('Аватар', upload_to='avatars/')
    phone = models.CharField('Телефон', max_length=12, unique=True)
    github_url = models.URLField('Github', blank=True)
    about = models.TextField('О себе', blank=True, max_length=256)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
        verbose_name='Избранные проекты',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def save(self, *args, **kwargs):
        
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_full_name(self):
        return f'{self.name} {self.surname}'

    def get_short_name(self):
        return self.name