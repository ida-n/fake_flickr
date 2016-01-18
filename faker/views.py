import datetime
from django.shortcuts import render
from .models import Image
from django.utils import timezone

def index(request):
	last_day = timezone.now() - datetime.timedelta(days=1)
	last_week = timezone.now() - datetime.timedelta(days=7)
	last_day_img_list = Image.get_top_images(last_day, 10)
	last_week_img_list = Image.get_top_images(last_week, 10)
	context = {
		'last_day_img_list': last_day_img_list,
		'last_week_img_list': last_day_img_list
	}
	return render(request, 'faker/index.html', context)