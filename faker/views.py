import datetime
from django.shortcuts import render, get_object_or_404
from .models import Image, ImageForm, CommentForm, Vote
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def index(request):
	last_day = timezone.now() - datetime.timedelta(days=1)
	last_week = timezone.now() - datetime.timedelta(days=7)
	last_day_img_list = Image.get_top_images(last_day, 10)
	last_week_img_list = Image.get_top_images(last_week, 10)
	context = {
		'last_day_img_list': last_day_img_list,
		'last_week_img_list': last_week_img_list
	}
	return render(request, 'faker/index.html', context)

def images(request):
	context = {
		'img_list': Image.objects.all()
	}
	return render(request, 'faker/images.html', context)

def image(request, image_id):
	img = get_object_or_404(Image, pk=image_id)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.user = request.user
			comment.image = img
			comment.save()
			return redirect('faker:image', image_id=image_id)
			# return HttpResponseRedirect(reverse('faker:my_images'))
	else:
		form = CommentForm()
	
	user_has_voted = len(img.vote_set.filter(user=request.user)) > 0
	context = {
		'image': img,
		'rate_range': range(1,6),
		'has_voted': user_has_voted,
		'comment_form': CommentForm
	}
	return render(request, 'faker/image.html', context)

@login_required
def vote(request, image_id):
	img = get_object_or_404(Image, pk=image_id)
	rate = int(request.POST['rate'])
	user_has_voted = len(img.vote_set.filter(user=request.user)) > 0
	if user_has_voted or rate not in range(1,6):
		return redirect('faker:image', image_id=image_id)
	
	v = Vote(rate=rate, user=request.user, image=img)
	v.save()
	return HttpResponseRedirect(reverse('faker:image', args=(image_id,)))

@login_required
def my_images(request):
	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES)
		print(request.FILES)
		if form.is_valid():
			img = form.save(commit=False)
			img.user = request.user
			img.save()
			return redirect('faker:my_images')
			# return HttpResponseRedirect(reverse('faker:my_images'))
	else:
		form = ImageForm()
	context = {
		'img_list': Image.objects.filter(user=request.user),
		'form': form
	}
	return render(request, 'faker/my_images.html', context)

# @login_required
# def upload(request):
# 	form = ImageForm(request.POST, request.FILES)
# 	if form.is_valid():
# 		img = form.save(commit=False)
# 		img.user = request.user
# 		img.save()
# 	return HttpResponseRedirect(reverse('faker:my_images'))