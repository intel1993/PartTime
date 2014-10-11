from rest_framework import serializers
from models import Record,Client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client

class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model=Record

class UserRecordSerializer(serializers.ModelSerializer):
    record = RecordSerializer(many=True)

    class Meta:
        model = Client

        #fields=('client.person_selling_name','person_selling_cnic','person_selling_address','person_selling_phone','phone_make','phone_model','imei_no','phone_sold_date','user_id')

