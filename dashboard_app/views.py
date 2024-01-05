from django.forms import model_to_dict
from rest_framework import viewsets
from .models import App, Plan, Subscription
from .serializers import AppSerializer,SubscriptionSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response





class GetPlans(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        resp = {
            'status':True,
            'status_code':status.HTTP_200_OK,
            'message':"Available Plans",
            'data': list(map(lambda x : {
                'plane id':x.pk,
                'plan name':x.name,
                'plane price':x.price
            },Plan.objects.select_related().all()))
        }

        # Plan.objects.select_related().all()
        return Response(resp)

class AppViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AppSerializer

    def get_queryset(self):
        # Return apps only owned by the current user
        print("hello")
        return App.objects.filter(owner=self.request.user.pk)

    def perform_create(self, serializer):
        print("hello2")

        # Automatically set the owner to the current user when creating a new app
        serializer.save(owner=self.request.user)




class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer
    http_method_names = ['get']

    def list(self, request):
        queryset = Subscription.objects.filter(app__owner = request.user,active=True)
        serializer = SubscriptionSerializer(queryset, many=True)
        # print(queryset,"+++")
        # app_details = [{'app_id':i.app.pk,
        #         'app_name':i.app.name,
        #         'app_description':i.app.description,
        #         } for i in queryset]
        
        # plan_detail = [{'plan_id':i.plan.pk,
        #         'plan_name':i.plan.name,
        #         'plan_price':i.plan.price,
        #         } for i in queryset]
        # main_data = [{**item,'plan':plan_detail,'app':app_details} for item in serializer.data]
        return Response({
            'status':True,
            'status_code':status.HTTP_200_OK,
            'message':"current subscription you subscribe",
            'data':serializer.data})
    

class SubcribeOtherSubscription(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        resp = {
            'status':False,
            'status_code':status.HTTP_400_BAD_REQUEST,
            'message':None,
            'data': {}
        }
        user = request.user
        app_id = request.data.get("app_id", None)
        print(app_id,"===")
        plan_id = request.data.get("plan_id", None)
        print(plan_id,"===")

        if plan_id is None or app_id is None:
            print('jaaani')
            resp['message'] = 'plan_id and app_id is required'
            return Response(resp,status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                plan_obj = Plan.objects.get(pk = plan_id)
            except:
                resp['message'] = 'Given plan_id id not found'
                return Response(resp,status=status.HTTP_400_BAD_REQUEST)
            try:
                app_obj = App.objects.get(pk = app_id)
            except:
                resp['message'] = 'Given app_id id not found'
                return Response(resp,status=status.HTTP_400_BAD_REQUEST)
            previous_subs = Subscription.objects.filter(app__owner = user)
            if previous_subs.exists():
                previous_subs_obj = previous_subs.first()
                previous_subs_obj.active = False
                previous_subs_obj.save()

                current_subs = Subscription.objects.create(
                    app = app_obj,
                    plan = plan_obj
                )
                resp['status'] = True
                resp['status_code'] = status.HTTP_200_OK
                resp['message'] = f'you subscribe {plan_obj.name} plan for {app_obj.name} app'
                resp['data'] = model_to_dict(current_subs)

                return Response(resp,status=status.HTTP_201_CREATED)
            else:
                resp['message'] = 'You dont have free subscription'
                return Response(resp,status=status.HTTP_400_BAD_REQUEST)
            

# class UserAppwithSubsription(APIView):
#     def get(self, request, *args, **kwargs):
#         resp = {
#             'status':True,
#             'status_code':status.HTTP_200_OK,
#             'message':"Details of your apps and their current subscription plan",
#             'data':None
#         }

#         subscription = Subscription.objects.filter(app__owner = request.user,active=True)
#         resp['data'] = {'user


