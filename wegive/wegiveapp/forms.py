from django import forms
from . import tags

class SearchForm(forms.Form):
    name = forms.CharField(label="Charity name", max_length=2000, required=False)
    # TODO: tags
    # IDEA: get the x and y from the user's address, check OSM Nominatim
    near_me = forms.BooleanField(label="Near Me", required=False)
    location_x = forms.FloatField(label="Location (x)", required=False)
    location_y = forms.FloatField(label="Location(y)", required=False)
    radius = forms.FloatField(label="Radius", required=False)
    tags = forms.MultipleChoiceField(label="Tags", required=False,
                                     widget=forms.CheckboxSelectMultiple,
                                     choices=[(i, i) for i in tags.tags])

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=2000)
	password = forms.CharField(label="Password", max_length=2000)

class SignUpForm(forms.Form):
	First_name = forms.CharField(label="Name", max_length=2000)
	username = forms.CharField(label="Username", max_length=2000)
	password = forms.CharField(label="Password", max_length=2000)
	phone = forms.CharField(label="Phone", max_length=2000)
	address = forms.CharField(label="Address", max_length=2000)
	email = forms.CharField(label="Email", max_length=2000)
	donor_or_Charity = forms.CharField(label="Charity/Donor", max_length=2000)

class SurveyForm(forms.Form):
	pass