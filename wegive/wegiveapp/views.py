from django.shortcuts import render
from . import models
from . import forms

# Create your views here.

def match_charity(name="", tags=[], location_x=0.0, location_y=0.0, radius=0.0):
    """
    Usage: match_charity(name="", tags="", location_x=0.0, location_y=0.0)
    Searches for charities with the given search terms.

    Note that for a location based search location_x, location_y, and radius
    must ALL be set.

    Parameters:
    string name: name of the charity
    string[] tags: List of strings (as would be returned from a form) of tags
                   to match.
    float location_x: origin x coordinate for a location based search
    float location_y: origin y coordinate for a location based search
    float radius: radius for a location based search.

    Returns:
    The resulting query set.
    """
    results_qset = models.Charity.objects.filter()
    # construct kwargs
    kwargs = {}
    if name != "":
        results_qset = results_qset.filter(name__contains=name)
    if tags != "":
        for tag in tags:
            results_qset = results_qset.filter(tags_csv__contains=tag)
    # parentheses here for implicit line completion
    if (location_x != 0 and location_y != 0 and radius != 0 and
        location_x != "" and location_y != "" and radius != ""):
        max_y = float(location_y) + float(radius)
        min_x = float(location_x) - float(radius)
        min_y = float(location_y) - float(radius)
        max_x = float(location_x) + float(radius)

        results_qset = results_qset.filter(location_x__gte=min_x, location_x_lte=max_x,
                            location_y__gte=min_y, location_y__lte=max_y)

    return results_qset

def search(request):
    """
    Search for charities.
    When accessed through GET, gives a search form.
    When accessed through POST, gives a table with search results. Each result
    will link to a select request.
    """
    if request.method == "POST":
        # TODO: near me test
        kwargs = {}
        for item in request.POST:
            if item in ("name", "location_x", "location_y", "radius", "tags"):
                kwargs[item] = request.POST[item]

        res = match_charity(**kwargs)
        return render(request, "html/search-results.html", {"res": res})
    else:
        form = forms.SearchForm()
        return render(request, "html/search.html", {"form": form})

def select(request):
    pass

def pay(request):
    pass
