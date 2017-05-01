from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from . import models
from . import forms
from .models import Charity
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
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
        print(request.POST)
        for item in request.POST:
            if item in ("name", "location_x", "location_y", "radius", "tags"):
                kwargs[item] = request.POST[item]

        res = match_charity(**kwargs)
        return render(request, "html/search-results.html", {"res": res})
    else:
        form = forms.SearchForm()
        return render(request, "html/search.html", {"form": form})

def select(request, id):
    """
    Select charities in order to view their personal page and information.
    """
    instance = get_object_or_404(Charity, id=id)
    context = {"Name": instance.name, "instance": instance, }
    return render(request, 'html/select-result.html', context)

def pay(request):
    pass

def loginat(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        #return render(request,...)
        return render(request, "html/homepage.html", {})
    else:
        form = forms.LoginForm()
        return render(request, "html/loginat.html", {"form": form})

def logoutat(request):
    logout(request)
    form = forms.LoginForm()
    return render(request, "html/homepage.html", {"form": form}) 

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get("address")
        user = User.objects.create_user(usename=usename, password=password)
    else:
        form = forms.SignUpForm()
        #render the template that has the sign up form        
        return render(request, "html/homepage.html",{"form": form} )


@login_required
def view_records(request, json=False):
    """
    View financial records for the current user.
    Requires authentication.
    Parameters:
    request: supplied by Django.
    json: boolean value to indicate if this should return JsonResponse.

    Returns:
    A rendering of the page showing results if json is False. Else, a 
    JsonResponse containing the data.
    """
    donors = models.Donor.objects.filter(user=request.user.id)
    charities = models.Charity.objects.filter(user=request.user.id)
    records = []

    print(request.user.id)
    print(donors)
    print(charities)

    for donor in donors:
        donor_records = models.Donation.objects.filter(donor=donor)
        for record in donor_records:
            records.append({"type": "donor", "data": record})

    for charity in charities:
        charity_records = models.Donation.objects.filter(charity=charity)
        for record in charity_records:
            records.append({"type": "charity", "data": record})

    if json:
        return JsonResponse({"results": records})

    return render(request, "html/records.html", {"res": records})

def webhook_endpoint(request):
    """
    Endpoint for webhooks from payment services. This is likely how we would
    generate payment records.
    NOT IMPLEMENTED
    """
    return HttpResponse(status=501)

def api(request):
    """
    JSON RESTful API to deliver information to the front-end.
    POST -> data goes in
    GET -> data goes out

    GET Parameters:
    type: One of records, info or charity. records returns financial records
          using view_records(), and info returns info about the user as a list
          of dictionaries with values from our database.

    The user must be logged in to use this API.

    requests:
    user info
    user records
    """
    if request.method == "POST":
        return HttpResponse(status=501)
    elif request.method == "GET":
        if not request.user.is_authenticated and request.GET["type"] != "charity":
            return HttpResponse(status=401)

        if request.GET["type"] == "record":
            return view_records(request, True)

        if request.GET["type"] == "info":
            rv = {"charity": [], "donor": []}
            donors = models.Donor.objects.filter(user=request.user)
            charities = models.Charity.objects.filter(id=request.user)
            
            for entry in donors:
                rv["donor"].append({
                    "name": entry.name, "address": entry.address,
                    "phone": entry.phone, "date_of_birth": entry.date_of_birth,
                    "tags": entry.tags})

            for entry in charities:
                rv["charity"].append({
                    "name": entry.name, "address": entry.address,
                    "phone": entry.phone, "cause": entry.cause,
                    "tags": entry.tags_csv})

            return JsonResponse(rv)

        if request.GET["type"] == "charity":
            kwargs = {}
            for item in request.GET:
                if item in ("name", "location_x", "location_y", "radius", "tags"):
                    kwargs[item] = request.GET[item]

            res = match_charity(**kwargs)
            rv = {"charity": []}

            for charity in res:
                rv["charity"].append({
                    "name": charity.name,"address": charity.address,
                    "phone": charity.phone, "cause": charity.cause, 
                    "tags": charity.tags_csv})

            return JsonResponse(rv)

        return HttpResponse(status=400)

    else:
        return HttpResponse(status=405)

def survey(request):
    if request.method == "POST":
        question_one = request.POST.get('username')
        question_two = request.POST.get('password')
        question_three = request.POST.get('name')
    else:
        form = forms.SurveyForm()        
        return render(request, "html/survey.html",{"form": form} )
        
def about(request):
    return render(request, "html/about.html", {})
    
def contact(request):
    form = forms.ContactForm()
    if request.method == 'POST':
        form1 = forms.ContactForm(data=request.POST)
        if form1.is_valid():
            contact_name = request.POST.get( 'contact_name', '' )
            contact_email = request.POST.get( 'contact_email', '' )
            form_content = request.POST.get('content', '')

            #Email stuff

            template = get_template('contact_temp.txt')
            
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
                })
            content = template.render(context)

            # send_mail(
            #     'test ',
            #     'Here is the message.',
            #     'from@example.com',
            #     ['contact_email'],
            #     fail_silently= False,
            #     )
            email = EmailMessage(
                "New Contact",
                content,
                "WeGive"+"", ['wegiveunh@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            #return redirect('contact') 

   
    return render(request, "html/contact.html", {'form': form})