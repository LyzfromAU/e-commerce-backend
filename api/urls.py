from django.urls import path
from .views import CreateOrderItemsView, ItemListView, RegisterView, LoginView, UserView, LogoutView, CreateOrderView, GetItemView, GetMonthlyView, GetPopularView, \
GetCarView, GetMotorView, GetOtherView, MessageView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('order/', CreateOrderView.as_view()),
    path('item/', GetItemView.as_view()),
    path('monthly/', GetMonthlyView.as_view()),
    path('popular/', GetPopularView.as_view()),
    path('car/', GetCarView.as_view()),
    path('motor/', GetMotorView.as_view()),
    path('other/', GetOtherView.as_view()),
    path('orderitem/', CreateOrderItemsView.as_view()),
    path('message/', MessageView.as_view()),
    path('search/', ItemListView.as_view()),

]