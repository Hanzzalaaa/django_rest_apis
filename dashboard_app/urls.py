from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppViewSet,SubscriptionViewSet,GetPlans,SubcribeOtherSubscription

router = DefaultRouter()

# Explicitly specify the basename
router.register(r'apps', AppViewSet, basename='app')
router.register(r'current_subscription', SubscriptionViewSet, basename='current_subscription')

urlpatterns = [
    path('', include(router.urls)),
    path("all_plans/", GetPlans.as_view(), name="all_plans"),
    path("subscribe_plan_for_app/", SubcribeOtherSubscription.as_view(), name="subscribe_plan_for_app"),

]
