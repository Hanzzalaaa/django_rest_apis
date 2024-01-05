from django.contrib import admin

# Register your models here.
from .models import App, Plan, Subscription

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'description')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('app', 'plan', 'active', 'subscribed_on')
