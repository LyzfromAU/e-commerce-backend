from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    
    REQUIRED_FIELDS = []
    def __str__(self):
        return str(self.username)

class Item(models.Model):
    CATE = [
        ('Mini4wds', 'Mini4wds'),
        ('Motors', 'Motors'),
        ('Hubs', 'Hubs'),
        ('Racing Circuits', 'Racing Circuits'),
    ]
    CHASSIS_TYPE = [
        ('AR', 'AR'),
        ('S2', 'S2'),
        ('FMA', 'FMA'),
        ('S1', 'S1'),
        ('SFM', 'SFM'),
        ('MS', 'MS'),
        ('VS', 'VS'),
        ('MA', 'MA'),
        ('NA', 'not applicable')
    ]

    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='uploads/')
    category = models.CharField(max_length=50, choices=CATE)
    chassis = models.CharField(max_length=20, choices=CHASSIS_TYPE)
    rpm = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    isOnPromotion = models.BooleanField(default=False)
    isPopular = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Payment Received', 'Payment Received'),
        ('Dispatched', 'Dispatched'),
        ('Fulfilled', 'Fulfilled'),
    ]
    user = ForeignKey(User, on_delete=CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS)

class OrderItem(models.Model):
    order = ForeignKey(Order, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    shaft = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()

class Message(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    message = models.TextField()


