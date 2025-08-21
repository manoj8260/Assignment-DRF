from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.serializers import (
    UserRegistrationSerializer ,UserAuthenticationSerializer,UserLogoutSerilaizers
    
)
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


class UserRegisterView(GenericAPIView) : 
    serializer_class  =UserRegistrationSerializer
    
    def post(self,request) :
        user_data = request.data
        serializer = self.serializer_class(data = user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            # send_code_to_user(serializer.data.get('email'))
            return Response(
                {
                    'data' : user,
                    'message' : f'hii  thanks for sign up '
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST) 
       
class    UserAuthenticateView(GenericAPIView):
    serializer_class = UserAuthenticationSerializer
    def post(self,request):
        
        serializers = self.serializer_class(data =request.data,context = {'request': request})
        serializers.is_valid(raise_exception=True)
        return Response(
          {
                'message' : "Login sucessfully",
                'user_details' : serializers.data
          }
        )
class UserLogoutView(GenericAPIView):
    serializer_class = UserLogoutSerilaizers
    def post(self,request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception=True) :
            serializer.save()
            return Response(
                {
                   'message' :  'Logout  Sucessfully !'
                }
            )
        return Response(serializer.error_messages)    
