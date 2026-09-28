from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import CustomUser
from django.db import models

class Recipient(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['last_name']

class Message(models.Model):
    theme = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

class Messenger(models.Model):
    CREATED = "created"
    LAUNCHED = "launched"
    FINISHED = "finished"

    MESSENGER_STATUS = [
        (CREATED,"Создана"),
        (LAUNCHED, "Запущена"),
        (FINISHED,"Завершена")
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=8, choices=MESSENGER_STATUS, default=CREATED)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.start_time < timezone.now():
            raise ValidationError('Дата начала не может быть в прошлом')
        if self.start_time >= self.end_time:
            raise ValidationError('Дата начала должна быть раньше даты окончания')

    def update_status(self):
        current_date = timezone.now()
        old_status = self.status
        if current_date < self.start_time:
            new_status = self.CREATED
        elif self.start_time <= current_date <= self.end_time:
            new_status = self.LAUNCHED
        else:
            new_status = self.FINISHED
        if new_status != old_status:
            self.status = new_status
            self.save()


class Attempt(models.Model):
    SUCCESS = "success"
    FAIL = "fail"

    ATTEMPT_STATUS = [
        (SUCCESS, "Успешно"),
        (FAIL, "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ATTEMPT_STATUS)
    server_response = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Messenger, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.mailing} — {self.status} — {self.attempt_time}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
