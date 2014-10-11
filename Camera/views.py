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
from serializers import UserRecordSerializer,UserSerializer,RecordSerializer
from rest_framework import generics
import hashlib

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
            record_id=form.save(user=request.user)
            return Response ({"success":True,"message":"Success", "record-id":record_id}, status.HTTP_200_OK)
        else:
            return Response ({"success":False,"message":"Invalid Data"}, status.HTTP_406_NOT_ACCEPTABLE)

class FetchUserRecords(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        serializer=UserRecordSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class PassChange(APIView):
    permission_classes = (AllowAny,)
    @method_decorator( csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PassChange,self).dispatch(request,*args,**kwargs)

    @method_decorator( csrf_exempt)
    def post(self,request):
        username=request.DATA['username']
        old_password=request.DATA['oldpassword']
        new_password=request.DATA['newpassword']
        try:
            user=Client.objects.get(username=username)
            if user is not None:
                success=user.check_password(old_password)
                if success==True:
                    user.set_password(new_password)
                    user.save()
                    return Response ({"success":True,"message":"Password Changed Successfully"}, status.HTTP_200_OK)
                else:
                    return Response ({"success":False,"message":"Wrong Password"}, status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response ({"success":False,"message":"No Such User Exits"}, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print e
            return Response ({"success":False,"message":"Invalid Username"}, status.HTTP_406_NOT_ACCEPTABLE)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist as e:
            print e
            return Response({"success":False,"message":"Something Went Wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        snippet = self.get_object(request.user.id)
        serializer = UserSerializer(snippet)
        return Response(serializer.data)

    def put(self, request):
        snippet = self.get_object(request.user.id)
        try:
            snippet.set_password(request.DATA['password'])
            snippet.save()
            return Response(status=status.HTTP_200_OK)
        # serializer = UserSerializer(snippet, data=request.DATA)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        snippet = self.get_object(request.user.id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SearchedRecordsList(generics.ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        queryset=Record.objects.filter(user_id=user)
        # searched = self.request.QUERY_PARAMS.get('searched', None)
        # type= self.request.QUERY_PARAMS.get('type', None)
        # if searched is not None:
        #     if type=='name':
        #         queryset = queryset.filter(person_selling_name=searched)
        #     elif type=='model':
        #         queryset = queryset.filter(phone_model=searched)
        #     elif type=='cnic':
        #         queryset = queryset.filter(person_selling_cnic=searched)
        #     elif type=='phone':
        #         queryset = queryset.filter(person_selling_phone=searched)
        #     elif type=='date':
        #         queryset = queryset.filter(phone_sold_date__lte=searched)
        return queryset

