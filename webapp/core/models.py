from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.CharField(max_length=20)
    language = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.telegram_id)


class Activity(models.Model):
    telegram_id = models.BigIntegerField()
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text