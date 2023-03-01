from django.db import models
from multiselectfield import MultiSelectField
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['strategy_engine2']
my_collection = db['instance_strategy_parameter']
my_collection2 = db['instance_parameter']
collection = db['instance_instance']

# Create your models here.

class StrategyIdField(models.CharField):
    def pre_save(self, model_instance, add):
        if add:
            try:
                latest_strategy = model_instance.__class__.objects.latest('strategy_id')
                strategy_id = int(latest_strategy.strategy_id.split('_')[1]) + 1
            except model_instance.__class__.DoesNotExist:
                strategy_id = 1
            model_instance.strategy_id = 's_{:02d}'.format(strategy_id)
        return model_instance.strategy_id

class ParameterIdField(models.CharField):
    def pre_save(self, model_instance, add):
        if add:
            try:
                letest_parameter = model_instance.__class__.objects.latest('parameter_id')
                parameter_id = int(letest_parameter.parameter_id.split('_')[1])+1
            except model_instance.__class__.DoesNotExist:
                parameter_id = 1
            model_instance.parameter_id = 'p_{:02d}'.format(parameter_id)
        return model_instance.parameter_id

class Parameter(models.Model):
    parameter_id = ParameterIdField(max_length=8, unique=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    variable = models.CharField(max_length=100)
    add_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(auto_now=True)

    def __unicode__(self):
        return self.variable

class Strategy(models.Model):
    strategy_id = StrategyIdField(max_length=8, unique=True, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100,primary_key=True)
    type = models.CharField(max_length=100)
    script = models.CharField(max_length=100)
    parameter = models.ManyToManyField(Parameter)
    add_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(auto_now=True)

    def __unicode__(self):
        return self.code


try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

class Instance(models.Model):
    Days = [
        ['0', 'Monday'],
        ['1', 'Tuesday'],
        ['2', 'Wednesday'],
        ['3', 'Thursday'],
        ['4', 'Friday']
    ]

    symbol = models.CharField(max_length=100)
    initialize_day = MultiSelectField(max_length=100, choices=Days)
    initialize_time = models.TimeField()
    terminate_time = models.TimeField()
    add_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(auto_now=True)
    strategy_fk = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def save(self, *args, **kwargs):
        fk = str(self.strategy_fk.code)
        para = self.strategy_fk.parameter
        id = self.id
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        for document in my_collection.find({'strategy_id': fk}):
            l1.append(document)
        for doc in my_collection2.find():
            l2.append(doc)
        for strategy_record in l1:
            for parameter_record in l2:
                if strategy_record['parameter_id'] == parameter_record['id']:
                    l3.append(parameter_record)
        new_list = [d['variable'] for d in l3]
        l4.append(new_list)
        if not self.pk:
            instances = []
            for day in self.initialize_day:
                in_day = str(day)
                id = self.id
                query = {'id': id}
                new_values = {"$set": {"entry time": 9}}
                collection.update_many(query, new_values)
                instance = self.__class__(
                    name=fk + '_' + self.symbol + '_' + in_day,
                    symbol=self.symbol,
                    initialize_day=[day],
                    initialize_time=self.initialize_time,
                    terminate_time=self.terminate_time,
                    add_time=self.add_time,
                    update_time=self.update_time,
                    strategy_fk=self.strategy_fk,

                )

                instances.append(instance)

            self.__class__.objects.bulk_create(instances)
        super().save(*args, **kwargs)
        a= str(self.strategy_fk.code)
        for sub_list in l4:
            for element in sub_list:
                query = {"strategy_fk_id": a}
                new_values = {"$set": {element: ""}}
                collection.update_many(query, new_values)

class Strategy_type(models.Model):
    strategy_type = models.CharField(max_length=100)

class Time_frame(models.Model):
    time_frame = models.CharField(max_length=100)