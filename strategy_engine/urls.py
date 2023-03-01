"""strategy_engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from instance import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('strategy/', views.Strategy_api.as_view()),
    path('strategy/<str:pk>', views.Strategy_api.as_view()),
    path('parameter',views.Parameter_api.as_view()),
    path('parameter/<str:pk>',views.Parameter_api.as_view()),
    path('instance',views.Instance_api.as_view()),
    path('instance/<str:pk>',views.Instance_api.as_view()),
    path('Strategy_type',views.Strategy_type_api.as_view()),
    path('Time_frame',views.Time_frame_api.as_view()),
    path('gettocken/', TokenObtainPairView.as_view(), name='tocken_obtain_pair'),
    path('refreshtocken/', TokenRefreshView.as_view(), name='refresh_tocken'),
    path('verifytocken/', TokenVerifyView.as_view(), name='verify_tocken'),
    path('get_strategy/', views.get_strategy),
    path('get_parameter/', views.get_parameter),
    path('post_instance/', views.post_instance),
    path('get_instance/', views.get_instance),
    path('get_instance_parameter/', views.get_instance_parameter),
    path('put_instance_parameter/<str:name>', views.put_instance_parameter),
    path('instances/', views.InstanceCreateView.as_view(), name='instance-create'),
    path('get_strategy1/', views.Strategy_create_view.as_view(), name='strategy-create')
    #path('', views.hello_reader,name="hello_reader"),
]
