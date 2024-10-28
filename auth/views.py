
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import MyTokenObtainPairSerializer
from .serializers import RegisterSerializer
from .serializers import GetUserSerializer

from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# TODO: non-consistent
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    user = request.user
    serializer = GetUserSerializer(user, many = False)
    return Response(serializer.data)