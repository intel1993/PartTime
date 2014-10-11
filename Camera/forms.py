import xadmin
from django import forms
from models import Client,Record
from django.utils import timezone


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Client
        fields=['name','address','ph_no','shop_name','username','password','cnic_no','latt_val', 'long_val']

    def save(self ,commit=True):
        try:
            user=super(RegistrationForm,self).save(commit=False)
            user.set_password(self.cleaned_data['password'])
            user.email='dummy@gmail.com'
            user.is_active=True
            user.save()

        except Exception as e:
            print e



class RecordForm(forms.ModelForm):
    class Meta:
        model=Record
        # fields=['person_selling_name','person_selling_cnic','person_selling_address','person_selling_phone','phone_make','phone_model','imei_no']
        exclude=['user_id']
    def save(self,user ,commit=True):
        try:
            record=super(RecordForm,self).save(commit=False)
            record.user_id=user
            record.phone_sold_date=timezone.now()
            record.save()
            return record.id
        except Exception as e:
            print e


