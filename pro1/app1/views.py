from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializer import BookSerializer 
from auth1.serializer import User
from rest_framework.response import Response
from .models import Book
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from .utils import EmailThread
from django.conf import settings

# Create your views here.

loggers = logging.getLogger('mylogger')


@api_view(http_method_names=(['GET', 'POST']))
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def BookView(request, format = None):
    if request.method == 'POST':
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info('Book Created SuccesFylly')
            user_email = request.user.email
            subject = 'Registration Successful'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                    subject =subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details:Email Sent Succesfully'})
            return Response(data=serializer.data, status=201)
        except:
            loggers.error("Error in Creating the Book")
            return Response(data=serializer.errors, status=404)
        
    if request.method=='GET':
        try:
            obj = Book.objects.all()
            serializer = BookSerializer(obj, many=True)
            loggers.info('Book Data Featched Succesfully')
            return Response(data=serializer.data, status=200)
        except:
            loggers.error(data=serializer.errors, status = 404)
            
@api_view(http_method_names=(['GET','PUT','PATCH','DELTE']))
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def details_api(request, pk):
    obj = get_object_or_404(Book,pk=pk)
    if request.method == 'GET':
        try:
            serializer = BookSerializer(obj)
            loggers.info('Book Featched Successfully')
            return Response(data=serializer.data,status=200)
        except:
            loggers.error('Failed to retrieve data')
            return Response(data={'details:Data Not Found'}, status=404)
        
    if request.method == 'PUT':
        try:
            serializer =BookSerializer(data=request.data, instance =obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info("Data Updated!!")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                    subject =subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details:Email Send SuccesFully'})
            return Response(data=serializer.data, status=205)
        except:
            loggers.error("Updation Failed!!!")
            return Response(data=serializer.errors, status=404)
    
    if request.method == 'PATCH':
        try:
            serializer =BookSerializer(data=request.data, instance =obj, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info("Data Updated!!")
            return Response(data=serializer.data, status=205)
        except:
            loggers.error("Updation Failed!!!")
            return Response(data=serializer.errors, status=400)    
    
    if request.method == 'DELETE':
        try:
            obj.delete()
            loggers.info("Deleted Sucessfully")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                    subject =subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details:Email Send SuccesFully'})
            return Response(data="Delete Successful", status=210)
        except:
            loggers.error("Delete failed")
            return Response(data='Error in Delete',status=406)
        
        