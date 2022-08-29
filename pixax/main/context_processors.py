import datetime

from .models import Slideshow


def intro_slideshow(request):
    intro_slideshow = Slideshow.objects.filter(name="introduction_slideshow").first()
    if intro_slideshow != None:
        slideshow_timer = intro_slideshow.timer
        amount_of_slides = intro_slideshow.slides.all().count()
        current_slide_number = get_slide_number(slideshow_timer, amount_of_slides)
        return {"intro_slideshow": intro_slideshow, "current_slide_number": current_slide_number, "slideshow_timer":slideshow_timer}
    else:
        return {"intro_slideshow": None, "current_slide_number": 0, "slideshow_timer":5}


def get_slide_number(slideshow_timer, amount_of_slides):
    counter = round((datetime.datetime.now() - datetime.datetime(2022,8,10)).total_seconds() / slideshow_timer)
    current_slide_number = counter % amount_of_slides + 1
    return current_slide_number