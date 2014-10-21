from rest_framework import serializers
from models import Record,Client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client

class RecordSerializer(serializers.ModelSerializer):

    date =serializers.SerializerMethodField('extract_date')
    time =serializers.SerializerMethodField('extract_time')

    def extract_date(self, obj):
        return obj.phone_sold_date.date()
    def extract_time(self, obj):
        return obj.phone_sold_date.time()
    class Meta:
        model=Record
        fields=('person_selling_name','person_selling_cnic','person_selling_address','person_selling_phone','phone_make','phone_model','imei_no','date','time','price_sold','cnic_front','cnic_back')



class UserRecordSerializer(serializers.ModelSerializer):
    record = RecordSerializer(many=True)

    class Meta:
        model = Client

        #fields=('client.person_selling_name','person_selling_cnic','person_selling_address','person_selling_phone','phone_make','phone_model','imei_no','phone_sold_date','user_id')

