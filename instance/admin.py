from django.contrib import admin
from .models import Strategy, Parameter, Instance, Strategy_type, Time_frame
# Register your models here.

class Strategy_admin(admin.ModelAdmin):
    fields = ['name', 'code', 'type', 'script','parameter']
    model = Strategy

admin.site.register(Strategy,Strategy_admin)

class Parameter_admin(admin.ModelAdmin):
    fields = ['name','description','variable']
    model = Parameter

admin.site.register(Parameter, Parameter_admin)

class Instance_admin(admin.ModelAdmin):
    fields = ['strategy_fk','symbol','initialize_day','initialize_time','terminate_time']
    moddel = Instance

admin.site.register(Instance, Instance_admin)

class Strategy_type_admin(admin.ModelAdmin):
    fields = ['strategy_type']
    model = Strategy_type

admin.site.register(Strategy_type, Strategy_type_admin)


class Time_frame_admin(admin.ModelAdmin):
    fields = ['time_frame','strategy_type']
    model = Time_frame

admin.site.register(Time_frame, Time_frame_admin)