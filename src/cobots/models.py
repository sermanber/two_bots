from django.db import models

# Create your models here.
class Cobots(models.Model):
    event = models.CharField(max_length=255, verbose_name='Название')
    place = models.CharField(max_length=500, verbose_name='Ссылка')
    name = models.CharField(max_length=255, verbose_name='Ведущий')
    time_create = models.TimeField(auto_now_add=True)
    time_update = models.TimeField(auto_now=True)
    is_approved = models.CharField(max_length=255, default=None, blank=True, verbose_name='Статус')
    user_chat_id = models.IntegerField(null=True, blank=True)


    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

