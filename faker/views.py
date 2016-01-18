import datetime
from django.shortcuts import render, get_object_or_404
from .models import Image
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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

def images(request):
	context = {
		'img_list': Image.objects.all()
	}
	return render(request, 'faker/images.html', context)

def image(request, image_id):
	img = get_object_or_404(Image, pk=image_id)
	context = {
		'image': img,
		'rate_range': range(1,6)
	}
	return render(request, 'faker/image.html', context)

def vote(request, image_id):
	img = get_object_or_404(Image, pk=image_id)
	rate = request.POST['rate']
	print(rate)
	print(type(rate))
	# try:
	# 	selected_choice = question.choice_set.get(pk=request.POST['choice'])
	# except (KeyError, Choice.DoesNotExist):
	# 	return render(request, 'polls/details.html', {
	# 		'question':question,
	# 		'error_message':'You didn\'t select a choice.'
	# 		})
	# else:
	# 	selected_choice.votes += 1
	# 	selected_choice.save()
	## return under else
	return HttpResponseRedirect(reverse('faker:image', args=(image_id,)))