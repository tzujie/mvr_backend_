from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.serializers import AccountSerializer
from django.contrib.auth import authenticate, login

@api_view(['POST'])
def register_account(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

from accounts.models import Account

@api_view(['POST'])
def login_account(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = Account.objects.get(email=email)
        if user.password == password:
            # 登录成功
            return Response({'message': '登录成功'}, status=200)
        else:
            # 密码不匹配
            return Response({'message': '登录失败'}, status=401)
    except Account.DoesNotExist:
        # 用户不存在
        return Response({'message': '登录失败'}, status=401)
    

from accounts.models import Account
from accounts.serializers import AccountSerializer

@api_view(['GET'])
def list_accounts(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True, exclude_fields=['password'])
    return Response(serializer.data, status=200)

