from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework import status
from . import models ,serializer
from django.http import HttpResponse
from django.contrib import auth  
from django.db.models import Q
from django.conf import settings
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

class UserListView(APIView):
	def get(self , request): # list of users 
		users = models.User.objects.all()
		ser = serializer.UserSerializer(users , many=True)
		return Response(ser.data , status=status.HTTP_200_OK)
	def post(self , request): # create the user
		ser = serializer.UserSerializer(data =  request.data)
		if ser.is_valid():
			ser.save()
			demo = models.User.objects.get(username=request.data["username"])
			demo.set_password(request.data["password"])
			demo.save()
			return Response(ser.data , status.HTTP_201_CREATED)
		else :
			return Response(ser.errors , status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
	def post(self , request ): # log_in the user and return the detail of user
		user = auth.authenticate(username = request.data["username"] , password=request.data["password"])
		if user is not None :
			ser =  serializer.UserSerializer(user)
			auth.login(request , user)
			refresh = RefreshToken.for_user(user)
			return Response({
				'refresh': str(refresh),
				'access': str(refresh.access_token),
				'user' : ser.data
			})
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
class LogOutAPI(APIView):
	def get(self , request):
		auth.logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)
		
class ForgetPasswordView(APIView):
	def get(self , request): #forget the password
		user = request.user
		if user.check_password(request.data["old_password"]):
			user.set_password(request.data["new_password"])
			user.save()
			return Response(status=status.HTTP_204_NO_CONTENT)
		else :
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		

class UserDetailView(APIView):

	def getUser(self , username): #fetch the deatil of user from db
		try:
			return models.User.objects.get(username = username)
		except:
			return None

	def get(self , request , username): #return the detail of specific user
		user = self.getUser(username)
		
		if user is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		ser = serializer.UserSerializer(user)
		return Response(ser.data , status.HTTP_200_OK)
	
	def patch(self , request , username): #update the detail of user
		user = self.getUser(username)
		ser = serializer.UserSerializer(user , data=request.data , partial=True)
		if ser.is_valid():
			ser.save()
			return Response(ser.data , status = status.HTTP_202_ACCEPTED)
		return Response(ser.errors , status = status.HTTP_400_BAD_REQUEST)

	def delete(self , request , username): #delete the user
		user = self.getUser(username)
		if user is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	
class GetInActiveUser(APIView):
	def get(self , request): #list of inactive user
		users = models.User.objects.filter(is_active = False)
		ser = serializer.UserSerializer(users , many = True)
		return Response(ser.data , status.HTTP_200_OK)
	
class CourseListView(generics.ListCreateAPIView):
	queryset=models.Course.objects.all()
	serializer_class = serializer.CourseSerializer

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Course.objects.all()
	serializer_class = serializer.CourseSerializer

class SubjectListView(generics.ListCreateAPIView):
	queryset=models.Subject.objects.all()
	serializer_class = serializer.SubjectSerializer

class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Subject.objects.all()
	serializer_class = serializer.SubjectSerializer

