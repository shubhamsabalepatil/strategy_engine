"""from django.db import models

# Define a function to create a new model class dynamically
def create_model_class(fields):
    attrs = {'__module__': __name__}
    for field_name, field_type in fields.items():
        field = field_type()
        attrs[field_name] = field
    model = type('MyModel', (models.Model,), attrs)
    return model

# Example usage
dynamic_fields = {
    'age': models.IntegerField,
    'email': models.EmailField,
    # Add more fields here based on user input
}
MyDynamicModel = create_model_class(dynamic_fields)

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
    parameters = DictField(default=dict)

def save(self, *args, **kwargs):
    print('model3', self.symbol)
    fk = str(self.strategy_fk.code)
    print('fk code is', fk)
    para = self.strategy_fk.parameter
    print('fk para is', para)
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
                print(l3)
    for i in l3:
        new_list = [i[k] for k in ('name', 'description', 'variable')]
        l4.append(new_list)
        print(l4)

    if not self.pk:
        instances = []
        for day in self.initialize_day:
            in_day = str(day)
            id = self.id
            print('id is', id)
            instance = self.__class__(
                name=fk + '_' + self.symbol + '_' + in_day,
                symbol=self.symbol,
                initialize_day=[day],
                initialize_time=self.initialize_time,
                terminate_time=self.terminate_time,
                add_time=self.add_time,
                update_time=self.update_time,
                strategy_fk=self.strategy_fk,
                parameters=l4
            )
            instances.append(instance)
        # Bulk create the instances
        self.__class__.objects.bulk_create(instances)
    super().save(*args, **kwargs)



from djongo import models

class MyModel(models.Model):
    symbol = models.CharField(max_length=50)
    initialize_day = models.CharField(max_length=50)
    initialize_time = models.TimeField()
    terminate_time = models.TimeField()
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    strategy_fk_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    parameters = models.DictField()

    def add_dynamic_field(self, field_name, description, value):
        self.parameters[field_name] = {
            'description': description,
            'value': value,
        }
        self.save()


my_model = MyModel.objects.create(
    symbol='nifty',
    initialize_day='0',
    initialize_time=datetime.time(17, 23, 53),
    terminate_time=datetime.time(17, 23, 54),
    strategy_fk_id='wall_1',
    name='wall_1_nifty_0',
    parameters={}
)

my_model.add_dynamic_field('field1', 'Description of field1', 'value1')

"""

"""from django.db import models

class MyModel(models.Model):
    field_names = ['field1', 'field2', 'field3']

    # create the fields dynamically using the field names list
    fields = {name: models.CharField(max_length=100) for name in field_names}

    # include only the fields in the include_fields list
    include_fields = ['field1', 'field3']
    for name, field in fields.items():
        if name not in include_fields:
            fields.pop(name)

    # add the fields to the model
    for name, field in fields.items():
        locals()[name] = field
"""
"""
import pymongo

# Replace the following with your MongoDB server details
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["strategy_engine"]
collection = db["instance_instance"]

#new_document = {"entry time": "9"}

query = { "id": 137 }
new_values = { "$push": { "entry time": 11 } }


collection.update_one(query, new_values)
"""
"""db.collection.updateOne(
   { "_id": ObjectId("63f31286fa4ca022bb426967") },
   { $push: { "entry time": [9] } }
)"""

"""db.collection.updateMany(
   { },
   { $push: { symbol: 95 } }
)"""
"""from .models import *

obj = Instance.object.get(id = 117)
print(obj)
#obj.add("entry time" == "9" )"""

from pymongo import MongoClient
from django.http import JsonResponse


client = MongoClient("mongodb://localhost:27017/")
db = client["strategy_engine"]


my_collection = db["instance_instance"]
my_document = my_collection.find({})
for doc in my_document:
    print(doc)

"""fields = list(my_document.keys())

 
response_data = {}
for field in fields:
    response_data[field] = my_document[field]
print(response_data)"""


def update_view(request, document_id):
    client = MongoClient('<mongodb_uri>')  # Replace <mongodb_uri> with your MongoDB URI
    db = client['<database_name>']  # Replace <database_name> with your database name
    collection = db['<collection_name>']  # Replace <collection_name> with your collection name

    if request.method == 'POST':
        # Get the update values from the POST data
        update = {}
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                update[key] = value

        # Update the document in the collection
        result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': update})

        if result.modified_count == 1:
            # If the update was successful, redirect to the document view page
            return redirect('document_view', document_id=document_id)
        else:
            # If the update was not successful, display an error message
            messages.error(request, 'Failed to update document')

    # Get the document from the collection
    document = collection.find_one({'_id': ObjectId(document_id)})

    # Create a dictionary of the initial data to pre-populate the update form
    initial_data = {}
    for key, value in document.items():
        if key != '_id':
            initial_data[key] = value

    # Render the update form with the initial data
    return render(request, 'update.html', {'initial_data': initial_data})
