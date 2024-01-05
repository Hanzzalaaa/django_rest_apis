from rest_framework import serializers
from .models import App, Plan, Subscription

class AppSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Make owner read-only
    class Meta:
        model = App
        fields = '__all__'

        

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'



class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_id = serializers.IntegerField(source='id')  # Rename 'id' to 'subscription_id'
    app = AppSerializer()
    plan = PlanSerializer()


    class Meta:
        model = Subscription
        # fields = '__all__'
        fields = ['subscription_id','active','plan','app']
