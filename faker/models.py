from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Image(models.Model):
	description = models.CharField(max_length=250)
	imgfile = models.ImageField(upload_to='images/%Y/%m/%d')
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.description

	@classmethod
	def get_top_images(cls, timestamp, limit):
		return cls.objects.filter(created_at__gte=timestamp)\
			.annotate(avg_rate=Avg('vote__rate'))\
			.order_by('-avg_rate')[:limit]

	@property
	def image_avg_rate(self):
		return self.vote_set.aggregate(Avg('rate'))['rate__avg']


class Comment(models.Model):
	comment_text = models.TextField()
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	image = models.ForeignKey(
		'Image',
		on_delete=models.CASCADE,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.comment_text

class Vote(models.Model):
	rate = models.PositiveSmallIntegerField(
		validators=[
			MaxValueValidator(5),
			MinValueValidator(1)
        ]
    )
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	image = models.ForeignKey(
		'Image',
		on_delete=models.CASCADE,
	)

	class Meta:
		unique_together = ('user', 'image')

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['description', 'imgfile']

