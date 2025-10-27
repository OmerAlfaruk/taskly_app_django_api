from rest_framework import viewsets,mixins,status,filters
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .models import House
from .serializer import HouseSerializer
from .permissions import IsHouseManagerOrNone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes=[IsHouseManagerOrNone]
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends=[filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields=['name','members','manager']
    ordering_fields=['points','completed_tasks']
    search_fields=['name','members','manager']
    @action(detail=True,methods=['post'],name='join',permission_classes=[])
    def join(self,request,pk=None):
        try:
            house=self.get_object()
            user_profile=request.user.profile
            
            if(user_profile.house==None):
                 user_profile.house=house
                 user_profile.save()
                 return Response(status=status.HTTP_204_NO_CONTENT)
            elif(user_profile in house.members.all()):
                return Response({"message":"already member of this house"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"already member of onother house"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=True,methods=['post'],name='leave',permission_classes=[])
    def leave(self,request,pk=None):
        house=self.get_object()
        
        user_profile=request.user.profile
        try:
            if(user_profile in house.members.all()):
                user_profile.house=None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            else:
                return Response({"message":"You are not member of this house"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @action(detail=True, methods=['post'], name='Remove Member', permission_classes=[IsHouseManagerOrNone])
    def remove_member(self, request, pk=None):
        house = self.get_object()
        user_id = request.data.get('user_id') or request.query_params.get('user_id')

        if not user_id:
            return Response({"message": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_profile = User.objects.get(id=user_id).profile
            house_members = house.members
            if user_profile in house_members.all():
                house_members.remove(user_profile)
                house.save()
                
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "user is not member of this house"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Provided user_id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        
       