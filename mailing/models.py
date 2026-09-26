from datetime import datetime

from django.db import models

class Recipient(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    comment = models.TextField()
    #user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['last_name']

class Message(models.Model):
    theme = models.CharField(max_length=50)
    content = models.TextField()
    #user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

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
    status = models.CharField(max_length=8, choices=MESSENGER_STATUS)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    def update_status(self):
        current_date = datetime.now()
        if current_date <  self.start_time:
            self.status = self.CREATED
        elif self.start_time <= current_date <= self.end_time:
            self.status = self.LAUNCHED
        else:
            self.status = self.FINISHED

