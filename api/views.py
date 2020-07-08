import re

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from api.filter import LimitFilter, ComputerFilterSet
from api.models import User, Computer
from api.paginations import MyPageNumberPagination, MyLimitPagination, MyCoursePagination
from api.serializers import UserModelSerializer, ComputerModelSerializer
from utils.response import APIResponse
from api.authentication import JWTAuthentication


class UserDetailAPIView(APIView):
    """
    只能登陆后才可以访问
    """
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        return APIResponse(results={"username": request.user.username})


class LoginAPIView(APIView):
    """
     实现多方式登录签发token：账号  手机  邮箱等登录
     #1. 禁用权限与认证组件
     #2. 获取前端发送的参数
     #3. 校验参数得到对应的用户
     #4. 签发token并返回
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 账号使用account  密码使用pwd
        # account = request.data.get("account")
        # pwd = request.data.get("pwd")
        user_ser = UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)

        return APIResponse(data_message="ok", token=user_ser.token, results=UserModelSerializer(user_ser.obj).data)

    # 典型的面向过程的写法  高耦合  无法复用 代码逻辑复杂  维护成本极高
    def demo_post(self, request, *args, **kwargs):
        account = request.data.get("account")
        pwd = request.data.get("pwd")

        # 对于各种登录方式做处理  账号  邮箱  手机号
        if re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        elif re.match(r'1[3-9][0-9]{9}', account):
            user_obj = User.objects.filter(phone=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()

        # 判断用户是否存在 且用户密码是否正确
        if user_obj and user_obj.check_password(pwd):
            # 签发token
            payload = jwt_payload_handler(user_obj)  # 生成载荷信息
            token = jwt_encode_handler(payload)  # 生成token
            return APIResponse(results={"username": user_obj.username}, token=token)

        return APIResponse(data_message="错误了")


# 游标分页
class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerModelSerializer

    # 通过此参数配置过滤的器类
    filter_backends = [SearchFilter, OrderingFilter, LimitFilter, DjangoFilterBackend]
    # 指定当前搜索条件
    search_fields = ["name", "price"]
    # 指定排序的条件
    ordering = ["price"]

    # 指定分页器   不能使用列表 或 元祖指定
    # pagination_class = MyPageNumberPagination
    # pagination_class = MyLimitPagination
    # 127.0.0.1:8000/api/computers/?ordering=price&page_size=1&name=小米
    # pagination_class = MyCoursePagination

    # 查询价格大于3000  小于 5000  电脑
    # django-filter 查询   通过filter_class指定过滤器
    filter_class = ComputerFilterSet
