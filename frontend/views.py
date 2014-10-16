import os
from django.shortcuts import HttpResponse, render
from .models import User, Skill, Photo, Video
from kedfilms import utils

DIR = os.path.abspath(os.path.dirname(__file__))
IMG_DIR = os.path.join(DIR, "static/frontend/img/")
VID_DIR = os.path.join(DIR, "static/frontend/vid/")

def home(request):
    skills_categories = []
    for item in Skill.objects.all().filter(
        owner='kedfilms-founder'
    ).order_by('category').values('category').distinct():

        skills_categories.append(item['category'])

    return render(request, "frontend/sections/home.html",
    {
        "skills_categories": skills_categories,
        "skills": Skill.objects.all().filter(owner='kedfilms-founder')
    })

def articles(request):
    try:
        last_edited = utils.getMostRecentFileRecursively(
            "frontend/templates/frontend/articles/",
            ".html"
        )
        # drops 'frontend/templates/'
        template = last_edited[last_edited.rfind('frontend'):]

    except ValueError:
        template = "frontend/sections/articles.html"    

    return render(request, template,
    {
        "title": "Articles",
        "subtitle": "Subtitle"
    })

def photos(request):
    if os.path.exists(IMG_DIR):
        return render(request, "frontend/sections/photos.html",
        {
            "title": "Photography",
            "subtitle": "Capture the moment in time",

            "portfolio_title": "Porfolio",
            "portfolio_images": Photo.objects.all().filter(category = Photo.PF),

            "general_title": "General",
            "general_images": Photo.objects.all().filter(category = Photo.GN)
        })

def photos_slideshow(request, category=None):
    photos = None
    previous_location = "/photos/"

    if category == "portfolio":
        category = Photo.PF
        previous_location += "#portfolio"

    elif category == "general":
        category = Photo.GN
        previous_location += "#general"

    else:
        return HttpResponse(status=404)

    photos = Photo.objects.all().filter(category = category)

    if photos:
        return render(request, "frontend/sections/slideshow.html",
        {
            "previous_location": previous_location,
            "photos": photos
        })

def videos(request):
    if os.path.exists(VID_DIR):
        return render(request, "frontend/sections/videos.html",
        {
            "intro_title": "Brief introductory passage",
            "intro_videos": Video.objects.all().filter(
                category = Video.IN).order_by('-date_created'),

            "favorite_title": "Personal Favorites",
            "favorite_videos": Video.objects.all().filter(
                category = Video.FV).order_by('-date_created'),

            "event_title": "A Gathering Of People",
            "event_videos": Video.objects.all().filter(
                category = Video.EV).order_by('-date_created'),

            "dancer_title": "Physical Expression",
            "dancer_videos": Video.objects.all().filter(
                category = Video.DN).order_by('-date_created')
        })
