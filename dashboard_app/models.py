from django.db import models
from  django.contrib.auth.models import User

# Create your models here.

class Plan(models.Model):
    FREE = 'Free'
    STANDARD = 'Standard'
    PRO = 'Pro'

    PLAN_CHOICES = [
        (FREE, 'Free'),
        (STANDARD, 'Standard'),
        (PRO, 'Pro'),
    ]
    name = models.CharField(max_length=10, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name




class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='apps', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(App, self).save(*args, **kwargs)
        if is_new:
            free_plan = Plan.objects.get(name=Plan.FREE)
            Subscription.objects.create(app=self, plan=free_plan)
    




class Subscription(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.app.name} - {self.plan.name}"
