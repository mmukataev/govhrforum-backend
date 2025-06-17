from django.db import models

class Speaker(models.Model):
    ROLE_CHOICES = [
        ('moderator', 'Moderator'),
        ('speaker', 'Speaker'),
    ]

    name_kz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    description_kz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()

    photo = models.ImageField(upload_to='speakers/', null=True, blank=True)

    priority = models.IntegerField(default=0) 

    def __str__(self):
        return self.name_en  # Или name_ru / name_kz по желанию

class News(models.Model):
    title_kz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)

    description_kz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()

    url_kz = models.URLField()
    url_ru = models.URLField()
    url_en = models.URLField()

    img = models.ImageField(upload_to='news/', null=True, blank=True)

    def __str__(self):
        return self.title_en

class Registration(models.Model):
    SESSION_CHOICES = [
        ('aiIntegration', 'Integration of Artificial Intelligence in Public Service'),
        ('fishbowlSession', 'Fishbowl Session - Development of Unified Personnel Management Systems'),
        ('foresightSession', 'Foresight Session - Proactive, Data-Driven HR Strategies and Strategic Workforce Planning'),
        ('trainingDevelopment', 'Training and Competency Development for Civil Servants'),
    ]

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    session = models.CharField(max_length=20, choices=SESSION_CHOICES)
    photo = models.ImageField(upload_to='registrations/', null=True, blank=True)
    consent = models.BooleanField(default=False)

    iin = models.TextField(blank=True, null=True)

    # You can add more fields for each session topic if needed, for example:
    foresight_topics = models.JSONField(blank=True, null=True)  # To store topics for foresight session

    def __str__(self):
        return f'{self.name} {self.surname} - {self.session}'