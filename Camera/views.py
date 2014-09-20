from django.shortcuts import render
from django.shortcuts import render, redirect,render_to_response
from models import Client,Record
import json
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from forms import RecordForm,RegistrationForm
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from serializers import UserRecordSerializer,UserSerializer


class SignUp(APIView):
    permission_classes = (AllowAny,)
    @method_decorator( csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignUp,self).dispatch(request,*args,**kwargs)

    @method_decorator( csrf_exempt)
    def post(self,request):
        data=request.DATA
        form=RegistrationForm(request.DATA)
        if form.is_valid():
            form.save()
            return Response ({"success":True,"message":"Success"}, status.HTTP_200_OK)
        else:
            return Response({"success":False, "message":"Information Not Valid"}, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    @method_decorator( csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView,self).dispatch(request,*args,**kwargs)

    @method_decorator( csrf_exempt)
    def post(self,request):
        user=authenticate(username=request.DATA['username'],password=request.DATA['password'])
        if user is None:
            return Response({"success":False,"message":"Invalid Username or Password"}, status.HTTP_401_UNAUTHORIZED)


        token = Token.objects.create(user=user)
        return Response ({"success":True,"token":token.key}, status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request.auth.delete()
            return Response({"success":True,"message":"Success"}, status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({"success":False,"message":"Something Went Wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateRecord(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        form=RecordForm(request.DATA)
        if form.is_valid():
            form.save(user=request.user)
            return Response ({"success":True,"message":"Success"}, status.HTTP_200_OK)
        else:
            return Response ({"success":False,"message":"Invalid Data"}, status.HTTP_406_NOT_ACCEPTABLE)

class FetchUserRecords(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        serializer=UserRecordSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)
