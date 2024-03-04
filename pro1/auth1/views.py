from rest_framework.decorators import api_view
from .serializer import UserSerializer,User
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
import logging
from .tokens import  account_activation_token
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from app1.utils import EmailThread
from django.conf import settings

# Create your views here.


loggers = logging.getLogger('mylogger')
@api_view(http_method_names=(['POST']))
def user(request):
    if request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            obj.is_active = False
            obj.save()
            domain = get_current_site(request=request).domain
            token = account_activation_token.make_token(obj)
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            relative_url = reverse('activate',kwargs={'uid': uid, 'token':token})
            absolute_url = f'http://%s'%(domain+relative_url,)
            message = "Hello %s,\n\tThank you for creating account with us. please click on the link below"\
                "to activate your account\n %s"%(obj.username,absolute_url,)
            subject = "Account Activation Email"
            EmailThread(subject=subject, message=message, recipient_list=[obj.email], from_email=settings.EMAIL_HOST_USER).start()
            return Response({"Message":"Please check your email to activate your account"},status=201)
        except Exception as e :
            print(e)
            loggers.error("Error in Creating the Student")
            return Response(data=serializer.errors, status=404)
        

@api_view()
def useraccountActivate(request,uid,token):
    if request.method == 'GET':
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk= user_id)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist)as e:
            return Response(data={'details':'there is an Error'},status=400)
        if account_activation_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            return Response(data={'details':'Account Activated SuccesFully'},status=200)
        return Response(data={'details':'Account link Invalid'},status=400)