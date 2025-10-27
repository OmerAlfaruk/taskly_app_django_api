from rest_framework import viewsets,mixins
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer,ProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly, IsProfileOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    permission_classes=[IsUserOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ProfileViewSet(viewsets.ModelViewSet,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    permission_classes=[IsProfileOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer