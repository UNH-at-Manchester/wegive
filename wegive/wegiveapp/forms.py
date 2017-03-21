from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label="Charity name", max_length=2000)
    # TODO: tags
    # IDEA: get the x and y from the user's address, check OSM Nominatim
    near_me = forms.BooleanField(label="Near Me", required=False)
    location_x = forms.FloatField(label="Location (x)", required=False)
    location_y = forms.FloatField(label="Location(y)", required=False)
    radius = forms.FloatField(label="Radius", required=False)

