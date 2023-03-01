class Instance_api(APIView):
    def get(self, request, pk=None):
        name = pk
        try:
            if name is not None:
                get_parameter_by_id = Instance.objects.get(name=name)
                # Extract additional fields from MongoDB
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["mydatabase"]
                instance_instance = db["instance_instance"]
                additional_fields = instance_instance.find_one({"name": name})
                if additional_fields is not None:
                    # Loop through all the fields in the MongoDB document
                    for field in additional_fields:
                        # Check if the field is not present in the Django model
                        if field not in get_parameter_by_id.__dict__:
                            setattr(get_parameter_by_id, field, additional_fields[field])
                serializer = Instance_serializer(get_parameter_by_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                get_all_instance = Instance.objects.all()
                serializer_of_all_instance = Instance_serializer(get_all_instance, many=True)
                return Response(serializer_of_all_instance.data, status=status.HTTP_200_OK)
        except Instance.DoesNotExist:
            return JsonResponse({'msg': 'Instance Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'msg': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
