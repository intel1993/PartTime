from django import forms
from models import Client,Record
from django.utils import timezone
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ('email','cnic_no',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

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

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields=['name','address','ph_no','shop_name','username','password','cnic_no','latt_val', 'long_val']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



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


