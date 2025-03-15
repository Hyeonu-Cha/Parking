from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Property
from .models import User as members


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True, max_length=20)
	last_name = forms.CharField(required=True, max_length=20)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "first_name", "last_name")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.f_name = self.cleaned_data['first_name']
		user.l_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user

class NewListingForm(forms.ModelForm):

	name = forms.CharField(required=True, max_length=20)
	providerid = forms.ModelChoiceField(queryset=User.objects.all())
	suburb = forms.CharField(required=True, max_length=20)
	state = forms.CharField(required=True, max_length=20)
	street = forms.CharField(required=True, max_length=50)
	postal = forms.IntegerField(required=True)
	parking_allign = forms.CharField(required=True, max_length=20)
	parking_type = forms.CharField(required=True, max_length=20)
	description = forms.CharField(required=True, max_length=200)
	ev = forms.BooleanField(required=False)
	handicap = forms.BooleanField(required=False)
	price_weekday = forms.FloatField()
	price_weekend = forms.FloatField()
	status = forms.CharField(max_length=20)
	deleted = forms.BooleanField(required=False, initial=False)
	property_image = forms.ImageField()

	class Meta:
		model = Property
		fields = '__all__'

	def save(self, commit=True):
		property = super(NewListingForm, self).save(commit=False)
		property.suburb = self.cleaned_data['suburb']
		property.state = self.cleaned_data['state']
		property.street = self.cleaned_data['street']
		property.postal = self.cleaned_data['postal']
		property.parking_allign = self.cleaned_data['parking_allign']
		property.parking_type = self.cleaned_data['parking_type']
		property.description = self.cleaned_data['description']
		property.ev = self.cleaned_data['ev']
		property.handicap = self.cleaned_data['handicap']
		property.price_weekday = self.cleaned_data['price_weekday']
		property.price_weekend = self.cleaned_data['price_weekend']
		property.status = self.cleaned_data['status']
		property.deleted = self.cleaned_data['deleted']
		property.property_image = self.cleaned_data['property_image']
		if commit:
			property.save()
		return property