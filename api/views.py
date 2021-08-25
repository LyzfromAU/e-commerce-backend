from rest_framework.views import APIView
from .serializers import OrderItemSerializer, UserSerializer, ItemSerializer, OrderSerializer, MessageSerializer
from rest_framework.response import Response
from .models import User, Item
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from operator import itemgetter
from rest_framework import filters, generics


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token, 'username': username, 'id': user.id}
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'Logout success!'}
        return response

class GetItemView(APIView):
    def get(self, request):
        id = request.query_params['id']
        item = Item.objects.all().filter(id=id).first()
        serializer = ItemSerializer(item, context={'request': request})
        return Response(serializer.data)

class GetMonthlyView(APIView):
    def get(self, request):
        monthlies = Item.objects.all().filter(isOnPromotion=True)
        serializer = ItemSerializer(monthlies, context={'request': request}, many=True)
        return Response(serializer.data)

class GetPopularView(APIView):
    def get(self, request):
        populars = Item.objects.all().filter(isPopular=True)
        serializer = ItemSerializer(populars, context={'request': request}, many=True)
        return Response(serializer.data)

class GetCarView(APIView):
    def get(self, request):
        chassis = request.query_params['chassis']
        if chassis == 'ALL':
            cars = Item.objects.all().filter(category='Mini4wds')
        else:
            cars = Item.objects.all().filter(chassis=chassis)
        serializer = ItemSerializer(cars, context={'request': request}, many=True)
        return Response(serializer.data)

class GetMotorView(APIView):
    def get(self, request):
        order = request.query_params['order']
        motors = Item.objects.all().filter(category='Motors')
        serializer = ItemSerializer(motors, context={'request': request}, many=True)
        if order == 'ascending':
            data = sorted(serializer.data, key=itemgetter('rpm'))
        elif order == 'descending':
            data = sorted(serializer.data, key=itemgetter('rpm'), reverse=True)
        else:
            data = serializer.data
        return Response(data)

class GetOtherView(APIView):
    def get(self, request):
        category = request.query_params['category']
        items = Item.objects.all().filter(category=category)
        serializer = ItemSerializer(items, context={'request': request}, many=True)
        return Response(serializer.data)

class CreateOrderView(APIView):
    def post(self, request):
        data = request.data
        data['create_time'] = datetime.datetime.now()
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class CreateOrderItemsView(APIView):
    def post(self, request):
        for item in request.data:
            serializer = OrderItemSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

class MessageView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']    
